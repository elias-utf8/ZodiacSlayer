"""
Module de correspondance des symboles pour Zodiac Slayer
Gère la correspondance entre les symboles extraits et la référence
"""

import os
import numpy as np
from scipy import signal

from image_processor import load_image_as_array, resize_image, get_sorted_symbols
from config import SYMBOLS_DIR, SYMBOLS_EXTRACTED_DIR, REFERENCE_DICT

class SymbolMatcher:
    def __init__(self, symbols_dir=SYMBOLS_DIR, symbols_extracted_dir=SYMBOLS_EXTRACTED_DIR):
        self.symbols_dir = symbols_dir
        self.symbols_extracted_dir = symbols_extracted_dir
        self.best_matches = {}
        self.reference_dict = REFERENCE_DICT

    def find_best_matches(self):
        """Trouve les meilleures correspondances entre les symboles et la référence"""
        symbols_images = get_sorted_symbols(self.symbols_dir)
        symbols_extracted_images = [f for f in os.listdir(self.symbols_extracted_dir) if f.endswith(".png")]
        
        for symbol_image in symbols_images:
            image1 = load_image_as_array(os.path.join(self.symbols_dir, symbol_image))
            best_score = 0
            best_match = None
            
            for extracted_image in symbols_extracted_images:
                image2 = load_image_as_array(os.path.join(self.symbols_extracted_dir, extracted_image))
                
                min_shape = (min(image1.shape[0], image2.shape[0]), min(image1.shape[1], image2.shape[1]))
                image1_resized = resize_image(image1, min_shape)
                image2_resized = resize_image(image2, min_shape)
                
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
        
        return self.best_matches
    
    def get_decoded_letters(self):
        """Convertit les correspondances en lettres décodées"""
        if not self.best_matches:
            self.find_best_matches()
        
        symbols_images = get_sorted_symbols(self.symbols_dir)
        decoded_message = []
        matched_count = 0
        
        for symbol_image in symbols_images:
            match, score = self.best_matches[symbol_image]
            print(f"{symbol_image} : {match} | score {score:.4f}")
            
            if match in self.reference_dict:
                letter = self.reference_dict[match]
                decoded_message.append(letter)
                print(f"Symbole : {letter}")
                matched_count += 1
            else:
                print(f"Aucune correspondance trouvée pour {match}")
                decoded_message.append("?")
        
        print(f"Symboles traités avec succès : {matched_count}")
        return "".join(decoded_message)