"""
Module de traitement d'image pour Zodiac Slayer
Gère le chargement, le traitement et le redimensionnement des images
"""

import os
import re
from PIL import Image
import numpy as np

def load_image_as_array(image_path):
    """Charge une image et la convertit en tableau binaire numpy"""
    image = Image.open(image_path).convert("RGBA")
    r, g, b, a = image.split()
    
    image_corrected = Image.new("L", image.size, 255)
    image_corrected.paste(Image.merge("RGB", (r, g, b)).convert("L"), mask=a)
    
    img_array = np.array(image_corrected)
    img_array = (img_array < 128).astype(np.uint8)
    
    return img_array

def resize_image(image, size):
    """Redimensionne une image numpy à la taille spécifiée"""
    return np.array(Image.fromarray(image).resize(size, Image.LANCZOS))

def extract_number(filename):
    """Extrait le numéro d'un nom de fichier de symbole"""
    match = re.search(r'symbole_(\d+)\.png', filename)
    if match:
        return int(match.group(1))
    return float('inf')

def get_sorted_symbols(directory):
    """Retourne la liste triée des fichiers de symboles dans un répertoire"""
    symbols_images = [f for f in os.listdir(directory) if f.endswith(".png")]
    symbols_images.sort(key=extract_number)
    return symbols_images