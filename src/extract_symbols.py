import cv2
import os
import numpy as np

def extract_symbols(image_input, output_folder='symboles_extraits'):

    """
    Extrait les symboles individuels de l'image du Zodiac et les sauvegarde dans des fichiers séparés.
    
    Entrée:
        image_input (numpy.ndarray): Chemin vers l'image ou image déjà chargée en mémoire
        output_folder (str): Dossier de destination des symboles extraits (par défaut: 'symboles_extraits')
        
    Sortie:
        None: Les symboles sont sauvegardés directement dans le dossier spécifié
        
    Description:
        - Convertit l'image en niveaux de gris
        - Applique un seuillage binaire
        - Détecte les contours des symboles
        - Trie les symboles de haut en bas et de gauche à droite
        - Sauvegarde chaque symbole dans un fichier PNG distinct
    """

    if isinstance(image_input, str):
        image = cv2.imread(image_input)
        if image is None:
            print(f"Erreur: Impossible de charger l'image à partir de {image_input}. Vérifiez le chemin.")
            return
    elif isinstance(image_input, np.ndarray):
        image = image_input
    else:
        print("Erreur: L'entrée doit être un chemin d'image (str) ou une image déjà chargée (numpy.ndarray).")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def sort_contours(contours):
        """
        Trie les contours des symboles par position (lignes puis colonnes).
        
        Entrée:
            contours (list): Liste des contours détectés dans l'image
            
        Sortie:
            tuple contenant:
                - final_contours (list): Liste des contours triés
                - final_boxes (list): Liste des boîtes englobantes correspondantes
                
        Description:
            - Regroupe les contours par ligne selon une tolérance verticale
            - Trie les symboles de gauche à droite dans chaque ligne
            - Retourne les contours triés avec leurs boîtes englobantes
        """
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        y_tolerance = 20
        sorted_with_y = sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1]) 
        lines = []
        current_line = [sorted_with_y[0]]
        
        for item in sorted_with_y[1:]:
            _, (_, y, _, _) = item
            _, (_, prev_y, _, _) = current_line[-1]
            
            if abs(y - prev_y) <= y_tolerance:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]
        
        if current_line:
            lines.append(current_line)
        final_contours = []
        final_boxes = []
        
        for line in lines:
            sorted_line = sorted(line, key=lambda b: b[1][0])     
            for contour, box in sorted_line:
                final_contours.append(contour)
                final_boxes.append(box)
        
        return final_contours, final_boxes

    contours, bounding_boxes = sort_contours(contours)

    os.makedirs(output_folder, exist_ok=True)  

    for i, (contour, (x, y, w, h)) in enumerate(zip(contours, bounding_boxes)):
        symbol = image[y:y+h, x:x+w]
        symbol_path = os.path.join(output_folder, f'symbole_{i + 1}.png')
        cv2.imwrite(symbol_path, symbol)
        
        print(f"Symbole {i + 1} sauvegardé : {symbol_path}")