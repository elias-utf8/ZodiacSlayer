import os
import re
from PIL import Image
import numpy as np

def load_symbol(image_path: str) -> np.ndarray:
    """
    Charge un symbole et la convertit en tableau numpy binaire.
    
    Entrée:
        image_path (str): Chemin vers le fichier image à charger
        
    Sortie:
        np.ndarray: Tableau numpy binaire où 1 représente les pixels noirs et 0 les pixels blancs
        
    Description:
        - Convertit l'image en RGBA
        - Gère la transparence
        - Convertit en niveaux de gris
        - Binarise l'image avec un seuil de 128
    """
    image = Image.open(image_path).convert("RGBA")
    r, g, b, a = image.split()
    
    image_corrected = Image.new("L", image.size, 255)
    image_corrected.paste(Image.merge("RGB", (r, g, b)).convert("L"), mask=a)
    
    img_array = np.array(image_corrected)
    img_array = (img_array < 128).astype(np.uint8)
    
    return img_array

def resize_symbol(image, size):
    """
    Redimensionne une image à une taille donnée.
    
    Entrée:
        image (np.ndarray): Image source sous forme de tableau numpy
        size (tuple): Dimensions cibles (largeur, hauteur)
        
    Sortie:
        np.ndarray: Image redimensionnée
        
    Description:
        Utilise l'algorithme LANCZOS pour un redimensionnement de haute qualité
    """
    return np.array(Image.fromarray(image).resize(size, Image.LANCZOS))

def extract_number(filename):
    """
    Extrait le numéro d'un fichier de symbole.
    
    Entrée:
        filename (str): Nom du fichier au format 'symbole_XX.png'
        
    Sortie:
        int ou float: Numéro du symbole ou inf si non trouvé
        
    Description:
        Utilise une expression régulière pour extraire le numéro du symbole
    """
    match = re.search(r'symbole_(\d+)\.png', filename)
    if match:
        return int(match.group(1))
    return float('inf')

def get_sorted_symbols(directory):
    """
    Récupère la liste triée des fichiers de symboles dans un répertoire.
    
    Entrée:
        directory (str): Chemin du répertoire contenant les symboles
        
    Sortie:
        list[str]: Liste triée des noms de fichiers des symboles
        
    Description:
        Trie les fichiers PNG selon leur numéro de symbole
    """
    symbols_images = [f for f in os.listdir(directory) if f.endswith(".png")]
    symbols_images.sort(key=extract_number)
    return symbols_images