"""
Zodiac Slayer - v1.0.0
Auteurs : Ethan CLEMENT, Elias GAUTHIER
Déchiffrement automatique du message du zodiaque Z-340 depuis une image
contenant les symboles sur 17 lignes.

Point d'entrée principal du programme
"""

from symbol_matcher import SymbolMatcher
from decoder import decode_zodiac_message

def main():
    print("Zodiac Slayer - v1.0.0")
    print("Déchiffrement automatique du message du zodiaque Z-340")
    print("------------------------------------------------------------------")
    
    # Étape 1: Faire correspondre les symboles
    matcher = SymbolMatcher()
    decoded_symbols = matcher.get_decoded_letters()
    
    # Étape 2: Décodage du message
    final_message = decode_zodiac_message(decoded_symbols)
    
    print("------------------------------------------------------------------")
    print("Déchiffrement terminé.")
    
    return final_message

if __name__ == "__main__":
    main()