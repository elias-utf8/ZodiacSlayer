"""
Module de décodage pour Zodiac Slayer
Implémente les algorithmes de décodage du message Z-340
"""

from config import ORIGINAL_INDICES

def formater_message(text):
    """Formate le message en lignes de 17 caractères sans espaces"""
    text = text.replace(" ", "")
    if len(text) != 306:
        print(f"Attention, la chaîne ne fait pas 306 caractères mais {len(text)} caractères")
        
    formatted_lines = [text[i:i+17] for i in range(0, len(text), 17)]
    return formatted_lines

def zodiac_algorithm(text):
    """Applique l'algorithme de déchiffrement du Zodiac"""
    original_indices = ORIGINAL_INDICES
    final = []
    
    for i in range(len(text)):
        temp = f"{str(original_indices[i])}" + f"{text[i]}"
        final.append(temp)
    
    final = sorted(final, key=lambda x: int(''.join(filter(str.isdigit, x))))
    final = [s.lstrip('0123456789') for s in final]
    
    message = "".join(final)
    return message

def decode_zodiac_message(decoded_symbols):
    """Procède au décodage complet du message Zodiac"""
    print("Message décodé:", decoded_symbols)
    print("------------------------------------------------------------------")
    
    formatted_text = formater_message(decoded_symbols)
    for line in formatted_text:
        print(f'"{line}"')
    
    text_sequence = "".join(formatted_text)
    final_message = zodiac_algorithm(text_sequence)
    print(f"Message FINAL : {final_message}")
    
    return final_message