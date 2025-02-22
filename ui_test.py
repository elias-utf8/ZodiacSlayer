import streamlit as st
import cv2
import numpy as np
from PIL import Image
import glob
import os
import shutil

from symbol_matcher import SymbolMatcher
from decoder import decode_zodiac_message
from extract_symbols import extract_symbols

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
    pil_image = Image.open(uploaded_file)
    
    with st.sidebar:
        st.image(pil_image, width=250)
        st.markdown("---")
        st.markdown("### Symboles extraits")
    st.markdown("**✅ | Image chargée**")

    if st.button("Extraire les symboles"):
        image_np = np.array(pil_image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        shutil.rmtree('symboles_extraits')

        extract_symbols(image_np, output_folder="symboles_extraits")

        with st.sidebar:
            with st.expander("Voir les symboles extraits", expanded=True):
                symbol_files = glob.glob("symboles_extraits/symbole_*.png")
                
                def get_symbol_number(filename):
                    try:
                        number = int(filename.split('symbole_')[1].replace('.png', ''))
                        return number
                    except:
                        return 0

                symbol_files = sorted(symbol_files, key=get_symbol_number)
                cols = st.columns(4)
                counter = 0
                for idx, symbol_file in enumerate(symbol_files):
                    col_idx = idx % 4
                    counter=counter+1
                    with cols[col_idx]:
                        symbol_img = Image.open(symbol_file)
                        symbol_img = symbol_img.resize((30, 30))
                        st.image(symbol_img, use_container_width=True)
                        numero = get_symbol_number(symbol_file)
                        st.caption(f"{numero}")

                

        if numero < 306 or numero > 306:
            st.markdown(f"**Attention, certains symboles n'ont pas étés correctement extraits.**\n\nSymboles extraits : `{counter}`\nSymbols attendus : `306`")
        else:
            st.markdown("**✅ | Symboles extraits**")
        decrypted_text = "Message partiellement déchiffré : ...XYZ..."   
        st.text_area("Résultat", decrypted_text)
        st.download_button("Télécharger le texte", decrypted_text, file_name="dechiffrement.txt")