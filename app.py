import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner

# Config
st.set_page_config(page_title="Stock Scan PRO", layout="centered")

# CSS pour compacter et épurer
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    div.stButton > button:first-child {
        height: 3.5em;
        width: 100%;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 12px;
    }
    /* Style pour les titres de section */
    .section-title {
        font-size: 0.9rem;
        font-weight: bold;
        color: #666;
        margin-bottom: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Gestion de Stock")

# --- 1. RÉGLAGES (En haut, hors du formulaire) ---
st.markdown('<p class="section-title">1. RÉGLAGES GÉNÉRAUX</p>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    type_mouv = st.selectbox("Action", ["SORTIE", "ENTRÉE", "PERTE"])
with col_b:
    site = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"])

st.divider()

# --- 2. CAMÉRA ---
st.markdown('<p class="section-title">2. SCANNER LE PRODUIT</p>', unsafe_allow_html=True)
valeur_qr = qrcode_scanner(key='scanner_unique')

st.divider()

# --- 3. FORMULAIRE DE VALIDATION ---
# On garde le formulaire très court pour qu'il tienne sous la caméra
with st.form("form_validation", clear_on_submit=True):
    # Rappel du produit détecté (ou saisie manuelle si le scan rate)
    produit = st.text_input("📦 Produit détecté", value=valeur_qr if valeur_qr else "")
    
    quantite = st.number_input("Quantité", min_value=0.0, step=1.0, value=1.0)
    
    # Bouton de validation
    submit = st.form_submit_button("VALIDER L'ENREGISTREMENT")

# --- LOGIQUE D'ENVOI ---
if submit:
    if produit and quantite > 0:
        # Ici on prépare la ligne pour le Google Sheet
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Enregistré : {type_mouv} | {produit} | Qté: {quantite} | {site}")
        st.balloons()
    else:
        st.error("Données manquantes (produit ou quantité)")

st.caption(f"LPB Stock System | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
