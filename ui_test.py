import streamlit as st
import cv2
import numpy as np
from PIL import Image

from symbol_matcher import SymbolMatcher
from decoder import decode_zodiac_message
from extract_symbols import extract_symbols

# Affichage du logo et du titre
st.image("repo/logo.png", use_column_width=True)
st.title("Zodiac Slayer - Z340")

url = "https://www.dcode.fr/zodiac-killer-cipher"

# Description
st.markdown("""
Ce programme permet le décodage du message du Zodiaque Z-340 directement depuis une image 
contenant les symboles du tueur du Zodiaque. Chaque symbole sera automatiquement isolé puis décodé.
""")

st.markdown('''
**Usage :**
- Téléchargement d'une image contenant 18 lignes avec 17 symboles par ligne  
- Détection automatique des symboles  
- Décodage du message 
''', unsafe_allow_html=True)

st.markdown("Il est préférable que l'image soit générée sur [dcode](%s)" % url)

uploaded_file = st.file_uploader("Chargez une image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Charger l'image avec PIL
    pil_image = Image.open(uploaded_file)
    
    # Afficher l'image dans la barre latérale
    with st.sidebar:
        st.image(pil_image, width=250)
    st.markdown("**✅ | Image chargée**")

    if st.button("Extraire les symboles"):
        # Convertir l'image PIL en tableau NumPy (format attendu par OpenCV)
        image_np = np.array(pil_image)
        
        # Convertir de RGB à BGR (OpenCV utilise BGR par défaut)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Appeler la fonction extract_symbols avec l'image convertie
        extract_symbols(image_np, output_folder="symboles_extraits")
        
        st.markdown("**✅ | Symboles extraits**")

        # Exemple de texte déchiffré
        decrypted_text = "Message partiellement déchiffré : ...XYZ..."   
        st.text_area("Résultat", decrypted_text)
        st.download_button("Télécharger le texte", decrypted_text, file_name="dechiffrement.txt")