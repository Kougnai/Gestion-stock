import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner

# Config
st.set_page_config(page_title="Stock Scan PRO", layout="centered")

# CSS pour l'ergonomie mobile
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
    .section-title {
        font-size: 0.85rem;
        font-weight: bold;
        color: #666;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Gestion de Stock")

# --- 1. NAVIGATION PRINCIPALE (TOUT EN HAUT) ---
mode = st.segmented_control(
    "CHOISIR LA FEUILLE", 
    ["FLUX", "INVENTAIRE"], 
    default="FLUX",
    key="nav_principale"
)

st.divider()

if mode == "FLUX":
    # --- RÉGLAGES FLUX ---
    st.markdown('<p class="section-title">Réglages du mouvement</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        type_mouv = st.selectbox("Action", ["SORTIE", "ENTRÉE", "PERTE"])
    with col_b:
        site = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"])

    st.markdown('<p class="section-title">Scanner le produit</p>', unsafe_allow_html=True)
    valeur_qr = qrcode_scanner(key='scanner_flux')

    with st.form("form_flux", clear_on_submit=True):
        produit = st.text_input("📦 Produit détecté", value=valeur_qr if valeur_qr else "")
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0, value=1.0)
        commentaire = st.text_input("Note (optionnel)")
        submit = st.form_submit_button("VALIDER LE FLUX")

    if submit:
        if produit and quantite > 0:
            st.success(f"✅ Flux enregistré : {type_mouv} | {produit} | {site}")
        else:
            st.error("Données manquantes")

else:
    # --- RÉGLAGES INVENTAIRE ---
    st.markdown('<p class="section-title">Réglages Inventaire</p>', unsafe_allow_html=True)
    site_inv = st.selectbox("Site à inventorier", ["LPB", "GUINGUETTE", "FLAMMA"])

    st.markdown('<p class="section-title">Scanner pour inventaire</p>', unsafe_allow_html=True)
    valeur_qr_inv = qrcode_scanner(key='scanner_inv')

    with st.form("form_inv", clear_on_submit=True):
        prod_inv = st.text_input("📦 Produit détecté", value=valeur_qr_inv if valeur_qr_inv else "")
        q_inv = st.number_input("Stock réel total", min_value=0.0, step=1.0)
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

    if submit_inv:
        if prod_inv:
            st.success(f"✅ Inventaire fixé : {prod_inv} à {q_inv} sur {site_inv}")
        else:
            st.error("Scannez un produit")

st.caption(f"LPB Stock System | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
