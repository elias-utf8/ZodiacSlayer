"""
Zodiac Slayer - v1.0.0

Auteurs : Ethan CLEMENT, Elias GAUTHIER

Déchiffrement d'une image contenant un message chiffré avec les symboles 
du tueur du zodiaque. Fait pour fonctionner avec https://www.dcode.fr/chiffre-tueur-zodiac 
"""

import os
import re
from PIL import Image
import numpy as np
from scipy import signal

class ZodiacSlayer:
    def __init__(self, symbols_dir="symboles_extraits", symbols_extracted_dir="symboles_2"):
        self.symbols_dir = symbols_dir
        self.symbols_extracted_dir = symbols_extracted_dir
        self.best_matches = {}
        self.reference_dict_corrected = {
            "char(33).png": " ", "char(35).png": "T", "char(37).png": "T", "char(38).png": "S",
            "char(40).png": "T", "char(41).png": "W", "char(42).png": "A", "char(43).png": "H",
            "char(45).png": "S", "char(46).png": "N", "char(47).png": "U", "char(48).png": " ",
            "char(49).png": "R", "char(50).png": "M", "char(51).png": "Y", "char(52).png": "E",
            "char(53).png": "V", "char(54).png": "D", "char(55).png": "L", "char(56).png": "P",
            "char(57).png": "N", "char(58).png": "T", "char(59).png": "T", "char(60).png": "I",
            "char(61).png": "Q", "char(62).png": "N", "char(63).png": "J", "char(64).png": "U",
            "char(65).png": "D", "char(66).png": "E", "char(67).png": "Y", "char(68).png": "N",
            "char(69).png": "R", "char(70).png": "F", "char(71).png": "T", "char(72).png": "I",
            "char(73).png": " ", "char(74).png": "S", "char(75).png": "A", "char(76).png": "G",
            "char(77).png": "O", "char(78).png": "E", "char(79).png": "A", "char(80).png": "I",
            "char(81).png": " ", "char(82).png": "O", "char(83).png": "D", "char(84).png": "R",
            "char(85).png": "S", "char(86).png": "O", "char(87).png": "W", "char(88).png": "R",
            "char(89).png": "N", "char(90).png": "R", "char(91).png": " ", "char(92).png": "K",
            "char(94).png": "O", "char(95).png": "B", "char(98).png": "E", "char(99).png": "E",
            "char(100).png": "L", "char(101).png": "X", "char(102).png": "B", "char(106).png": "P",
            "char(107).png": "I", "char(108).png": "A", "char(112).png": "C", "char(113).png": "U",
            "char(114).png": "Z", "char(116).png": "L", "char(121).png": "I", "char(122).png": "A",
            "char(124).png": "E"
        }
        
    def load_image_as_array(self, image_path):
        image = Image.open(image_path).convert("RGBA")
        r, g, b, a = image.split()
        
        image_corrected = Image.new("L", image.size, 255)
        image_corrected.paste(Image.merge("RGB", (r, g, b)).convert("L"), mask=a)
        
        img_array = np.array(image_corrected)
        img_array = (img_array < 128).astype(np.uint8)
        
        return img_array
    
    def resize_image(self, image, size):
        return np.array(Image.fromarray(image).resize(size, Image.LANCZOS))
    
    def extract_number(self, filename):
        match = re.search(r'symbole_(\d+)\.png', filename)
        if match:
            return int(match.group(1))
        return float('inf')
    
    def formater_message(self, text):
        text = text.replace(" ", "")
        if len(text) != 306:
            print(f"Attention, la chaîne ne fait pas 306 caractères mais {len(text)} caractères")
        formatted_lines = [text[i:i+17] for i in range(0, len(text), 17)]
        return formatted_lines
    
    def zodiac_algorithm(self, text):
        original_indices = [
            1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 91, 100, 109, 118, 127, 136, 145,
            137, 146, 2, 11, 20, 29, 38, 47, 56, 65, 74, 83, 92, 101, 110, 119, 128,
            120, 129, 138, 147, 3, 12, 21, 30, 39, 48, 57, 66, 75, 84, 93, 102, 111,
            103, 112, 121, 130, 139, 148, 4, 13, 22, 31, 40, 49, 58, 67, 76, 85, 94,
            86, 95, 104, 113, 122, 131, 140, 149, 5, 14, 23, 32, 41, 50, 59, 68, 77,
            69, 78, 87, 96, 105, 114, 123, 132, 141, 150, 6, 15, 24, 33, 42, 51, 60,
            52, 61, 70, 79, 88, 97, 106, 115, 124, 133, 142, 151, 7, 16, 25, 34, 43,
            35, 44, 53, 62, 71, 80, 89, 98, 107, 116, 125, 134, 143, 152, 8, 17, 26,
            18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108, 117, 126, 135, 144, 153, 9,
            154, 163, 172, 181, 190, 199, 208, 217, 226, 235, 244, 253, 262, 271, 280, 289, 298,
            290, 299, 155, 164, 173, 182, 191, 200, 209, 218, 227, 236, 245, 254, 263, 272, 281,
            273, 282, 291, 300, 156, 165, 174, 183, 192, 201, 210, 219, 228, 237, 246, 255, 264,
            256, 265, 274, 283, 292, 301, 157, 166, 175, 184, 193, 202, 211, 220, 229, 238, 247,
            239, 248, 257, 266, 275, 284, 293, 302, 158, 167, 176, 185, 194, 203, 212, 221, 230,
            222, 231, 240, 249, 258, 267, 276, 285, 294, 303, 159, 168, 177, 186, 195, 204, 213,
            205, 214, 223, 232, 241, 250, 259, 268, 277, 286, 295, 304, 160, 169, 178, 187, 196,
            188, 197, 206, 215, 224, 233, 242, 251, 260, 269, 278, 287, 296, 305, 161, 170, 179,
            171, 180, 189, 198, 207, 216, 225, 234, 243, 252, 261, 270, 279, 288, 297, 306, 162
        ]

        final = []
        message = ""

        for i in range(len(text)):
            temp = f"{str(original_indices[i])}" + f"{text[i]}"
            final.append(temp)
        final = sorted(final, key=lambda x: int(''.join(filter(str.isdigit, x))))
        final = [re.sub(r'\d+', '', s) for s in final]
        for i in range(len(final)):
            message += (final[i])

        return message
    
    def find_best_matches(self):
        symbols_images = [f for f in os.listdir(self.symbols_dir) if f.endswith(".png")]
        symbols_images.sort(key=self.extract_number)
        
        symbols_extracted_images = [f for f in os.listdir(self.symbols_extracted_dir) if f.endswith(".png")]
        
        for symbol_image in symbols_images:
            image1 = self.load_image_as_array(os.path.join(self.symbols_dir, symbol_image))
            best_score = 0
            best_match = None
            
            for extracted_image in symbols_extracted_images:
                image2 = self.load_image_as_array(os.path.join(self.symbols_extracted_dir, extracted_image))
                
                min_shape = (min(image1.shape[0], image2.shape[0]), min(image1.shape[1], image2.shape[1]))
                image1_resized = self.resize_image(image1, min_shape)
                image2_resized = self.resize_image(image2, min_shape)
                
                cor = signal.correlate2d(image1_resized, image2_resized, mode="valid")
                
                norm_factor = np.linalg.norm(image1_resized) * np.linalg.norm(image2_resized)
                if norm_factor > 0:
                    cor_normalized = cor / norm_factor
                else:
                    cor_normalized = cor
                
                max_cor = np.max(cor_normalized)
                
                if max_cor > best_score:
                    best_score = max_cor
                    best_match = extracted_image
            
            self.best_matches[symbol_image] = (best_match, best_score)
    
    def decode_message(self):
        if not self.best_matches:
            self.find_best_matches()
        
        symbols_images = [f for f in os.listdir(self.symbols_dir) if f.endswith(".png")]
        symbols_images.sort(key=self.extract_number)
        
        decoded_message = []
        
        i = 0
        for symbol_image in symbols_images:
            match, score = self.best_matches[symbol_image]
            print(f"{symbol_image} : {match} | score {score:.4f}")
            
            if match in self.reference_dict_corrected:
                letter = self.reference_dict_corrected[match]
                decoded_message.append(letter)
                print(f"Symbole : {letter}")
                i = i + 1
            else:
                print(f"Aucune correspondance trouvée pour {match}")
                decoded_message.append("?")
        
        print("Message décodé:", "".join(decoded_message))
        print(f"Symboles traités avec succès : {i}")
        print("------------------------------------------------------------------")
        formatted_text = self.formater_message("".join(decoded_message))
        for line in formatted_text:
            print(f'"{line}"')
        text_sequence = "".join(formatted_text)
        final_message = self.zodiac_algorithm(text_sequence)
        print(f"Message FINAL : {final_message}")
        
        return final_message

if __name__ == "__main__":
    slayer = ZodiacSlayer()
    slayer.decode_message()