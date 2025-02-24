[![streamlit-ext-demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zodiacslayer-cdd7bne9mvfgdsn2uk5gnr.streamlit.app/)

<div align="center">
<img src="assets/logo.png" width="250" height="200" alt="Logo">

  <h1><b>Zodiac Slayer</b></h1>
    <p>
    Ce programme permet le déchiffrement du message du zodiaque Z-340 directement depuis une image 
    contenant les symboles du zodiaques spécifique au Z-340.
  </p>

  ![Logo](assets/screenshot_1.png)


</div>

## Aperçu

Ce programme prend en charge des messages codés basés sur Z-340 de 17 colonnes, 20 lignes mais également 
de 17 colonnes, 18 lignes. Il suffit de charger l'image sur l'interface et de suivre les étapes. 
**Il est possible de faire tourner le projet en local ou d'aller directement sur [la page streamlit](https://zodiacslayer-cdd7bne9mvfgdsn2uk5gnr.streamlit.app/)**

## Installation 
### Installer Python 
Windows
1. **Téléchargement**
   - Visitez [python.org](https://www.python.org/downloads/)
   - Cliquez sur "Download Python X.X.X" (dernière version)

2. **Installation**
   - Lancez l'installateur téléchargé
   - ✅ Cochez "Add Python to PATH"
   - Cliquez sur "Install Now"
---
Linux
```sh
sudo apt update
sudo apt install python3
```
> Même paquet pour dnf, pacman etc

### Cloner le projet et ses dépendances 
```sh
git clone https://github.com/elias-utf8/ZodiacSlayer.git
cd ZodiacSlayer
pip install -r requirements.txt
```
Pour lancer l'application : 
```py
streamlit run ZodiacSlayer.py
```

## Usage 
> [!IMPORTANT]
> Il est important de lire cette section, la détection des images n'est pas encore parfaite.

