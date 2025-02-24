from src.config import ORIGINAL_INDICES, ORIGINAL_INDICES2

def formater_message(text: str) -> tuple[list[str], bool]:
    """
    Formate le texte des correspondances en le découpant en lignes de 17 caractères.
    
    Entrée:
        text (str): Texte à formater
        
    Sortie:
        tuple contenant:
            - formatted_lines (list[str]): Liste des lignes formatées de 17 caractères
            - original (bool): True si le texte fait plus de 306 caractères
    """

    text = text.replace(" ", "")
    if len(text) != 306:
        print(f"La chaine fait {len(text)} caractères")
    original = len(text) > 306
    formatted_lines = [text[i:i+17] for i in range(0, len(text), 17)]
    return formatted_lines, original

def zodiac_algorithm(text: str, original: bool = False) -> str:
    """
    Applique l'algorithme de décodage Zodiac sur le texte.
    
    Entrées:
        text (str): Texte à décoder
        original (bool): Détermine quels indices originaux utiliser
        
    Variables:
        original_indices (list[int]): Liste d'indices de référence depuis config.py
        final (list[str]): Liste temporaire pour stocker les caractères réordonnés
        message (str): Message final décodé
        
    Sortie:
        message (str): Message décodé et réorganisé
    """

    if original:
        original_indices = ORIGINAL_INDICES2
    else:
        original_indices = ORIGINAL_INDICES
    final = []
    
    if len(text) > len(original_indices):
        text = text[:len(original_indices)]
    elif len(text) < len(original_indices):
        original_indices = original_indices[:len(text)]
    
    for i in range(len(text)):
        try:
            temp = f"{str(original_indices[i])}" + f"{text[i]}"
            final.append(temp)
        except IndexError:
            print(f"Index error at position {i}")
            break
    
    final = sorted(final, key=lambda x: int(''.join(filter(str.isdigit, x))))
    final = [s.lstrip('0123456789') for s in final]
    
    message = "".join(final)
    return message

def decode_zodiac_message(decoded_symbols: str) -> str:
    """
    Décode un message Zodiac complet en utilisant zodiac_algorithm()
    
    Entrée:
        decoded_symbols (str): Chaîne de symboles décodés
        
    Variables:
        formatted_text (list[str]): Texte formaté en lignes
        original (bool): Indique si le texte fait plus de 306 caractères
        text_sequence (str): Texte formaté reconstitué
        final_message (str): Message final décodé
        
    Sortie:
        final_message (str): Message décodé final
    """
    print("Message décodé:", decoded_symbols)    
    formatted_text, original = formater_message(decoded_symbols)
    for line in formatted_text:
        print(f'"{line}"')
    
    text_sequence = "".join(formatted_text)
    final_message = zodiac_algorithm(text_sequence, original)
    
    return final_message