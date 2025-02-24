"""
ZodiacSlayer - Version 1.0.0

Décodage semi-automatisé du Z340 du tueur du Zodiac,
initialement prévu pour la plateforme cyber-learning.fr

Dernière date de mise à jour : 23/02/2025
Auteurs : Elias GAUTHIER, Ethan CLEMENT

Documentation intégrale sur le repo GitHub du projet. 
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import glob
import os
import shutil
from pathlib import Path
from typing import List
import time
from datetime import datetime

from src.symbol_matcher import SymbolMatcher
from src.decoder import decode_zodiac_message
from src.extract_symbols import extract_symbols

EXPECTED_SYMBOLS_CASE1 = 306
EXPECTED_SYMBOLS_CASE2 = 340

SYMBOLS_PER_LINE = 17
TOTAL_LINES = 18
OUTPUT_FOLDER = "symboles_extraits"
ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
DCODE_URL = "https://www.dcode.fr/zodiac-killer-cipher"


def setup_page():
    st.set_page_config(page_title="Zodiac Slayer - Z340", page_icon="assets/logo.png")
    #st.image("assets/logo.png", width=300)
    st.title("Zodiac Slayer - Z340")

    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
    """, unsafe_allow_html=True)

def display_instructions():
    st.markdown(
        """
        Ce programme permet le décodage du message du Zodiaque Z-340 directement depuis une image 
        contenant les symboles du tuteur du Zodiaque. Chaque symbole sera automatiquement isolé puis décodé.
        """
    )
    st.markdown(
        '''
        **Usage :**
        - Téléchargement d'une image contenant 18 OU 20 lignes avec 17 symboles par ligne
        - Détection automatique des symboles (Sensible à la casse)
        - Décodage du message 
        ''',
        unsafe_allow_html=True,
    )
    st.markdown(f"L'image peut être générée sur [dcode]({DCODE_URL}) ou sur ")


def get_symbol_number(filename: str) -> int:
    """
    get_symbol_number

    Entrée : Nom d'un fichier de type string au format 'symbole_XX'
    Sortie : Retourne le numéro 'XX' du fichier concerné
    """
    try:
        return int(Path(filename).stem.split('symbole_')[1])
    except (ValueError, IndexError):
        return 0


def display_extracted_symbols(symbol_files: List[str]) -> int:
    """
    display_extracted_symbols

    Entrée : Liste des chemins des fichiers des symboles extraits
    Sortie : Nombre total de symboles extraits
    """
    with st.sidebar:
        with st.expander("Voir les symboles extraits", expanded=True):
            cols = st.columns(4)
            for idx, symbol_file in enumerate(sorted(symbol_files, key=get_symbol_number)):
                with cols[idx % 4]:
                    symbol_img = Image.open(symbol_file).resize((30, 30))
                    st.image(symbol_img, use_container_width=True)
                    st.caption(f"{get_symbol_number(symbol_file)}")
    return len(symbol_files)

def decode_zodiac(matcher):
    """
    decode_zodiac

    Entrée : Instance de la classe SymbolMatcher
    Sortie : Tuple contenant (mapping des symboles décodés, message décodé)
    """
    start_time = time.time()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_text = st.empty()
    
    total_steps = 100
    for i in range(total_steps):
        progress_bar.progress(i + 1)
        current_time = time.time() - start_time
        status_text.text(f"Décodage en cours... {i+1}%")
        time_text.text(f"Temps écoulé: {current_time:.2f} secondes")
        time.sleep(0.02)
    
    decoded_mapping, matched_count = matcher.get_decoded_letters()
    decoded_message = decode_zodiac_message(''.join(decoded_mapping))
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    progress_bar.empty()
    status_text.empty()
    time_text.empty()
    
    st.info(f"⏱️ Temps d'exécution total: {execution_time:.2f} secondes")
    
    return decoded_mapping, decoded_message

def main():
    """
    Fonction principale qui gère le flux de l'application :
        - Configuration de la page
        - Chargement de l'image contenant les symboles
        - Extraction des symboles
        - Décodage du message
    """
    setup_page()
    display_instructions()
    
    matcher = SymbolMatcher()
    
    if "extraction_done" not in st.session_state:
        st.session_state.extraction_done = False
    if "symbol_files" not in st.session_state:
        st.session_state.symbol_files = []

    uploaded_file = st.file_uploader("Chargez une image", type=ALLOWED_EXTENSIONS)

    if uploaded_file:
        pil_image = Image.open(uploaded_file)
        
        with st.sidebar:
            st.image(pil_image, width=250)
            st.markdown("---")
            st.markdown("### Symboles extraits")
        st.markdown("**✅ | Image chargée**")

        if st.button("Extraire les symboles") or st.session_state.extraction_done:
            if not st.session_state.extraction_done:
                start_time = time.time()
                image_np = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

                if os.path.exists(OUTPUT_FOLDER):
                    shutil.rmtree(OUTPUT_FOLDER)
                os.makedirs(OUTPUT_FOLDER, exist_ok=True)

                extract_symbols(image_np, output_folder=OUTPUT_FOLDER)

                st.session_state.symbol_files = glob.glob(f"{OUTPUT_FOLDER}/symbole_*.png")
                st.session_state.extraction_done = True
                
                end_time = time.time()
                extraction_time = end_time - start_time
                st.info(f"⏱️ Temps d'extraction: {extraction_time:.2f} secondes")

            counter = display_extracted_symbols(st.session_state.symbol_files)

            if counter < EXPECTED_SYMBOLS_CASE1:
                st.warning(
                    f"Attention, moins de 306 symboles on étés extraits. Le texte décodé peut être faux ou erroné.\n"
                    f"Symboles extraits : {counter} / {EXPECTED_SYMBOLS_CASE1}"
                )
            elif counter > EXPECTED_SYMBOLS_CASE2:
                st.warning(
                    f"Attention, plus de 340 symboles on étés extraits. Le texte décodé peut être faux ou erroné.\n"
                    f"Symboles extraits : {counter} / {EXPECTED_SYMBOLS_CASE2}"
                )
            elif counter == 340 or counter == 306:
                st.success("Symboles extraits correctement.")
            else:
                st.warning(
                    f"Attention, certains symboles n'ont pas étés correctement extraits. Le texte décodé peut être faux ou erroné.\n"
                )

            if st.button("Décoder symboles"):
                with st.spinner('Décodage des symboles en cours...'):
                    decoded_mapping, decoded_message = decode_zodiac(matcher)
                    
                    st.text_area("Correspondance des symboles", decoded_mapping, height=200)
                    st.text_area("Message décodé", decoded_message, height=200)
                    st.session_state.extraction_done = False
                    st.success("Programme terminé, décodage réussi.")

if __name__ == "__main__":
    main()
