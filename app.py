import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner

# Config
st.set_page_config(page_title="Stock Scan", layout="centered")

# CSS pour compacter l'interface et fixer le bouton
st.markdown("""
    <style>
    /* Réduit les marges hautes */
    .block-container { padding-top: 1rem; }
    
    /* Style du bouton valider */
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    
    /* Aligne le texte du scanner */
    .stHeader { font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
mode = st.segmented_control("MENU", ["MOUVEMENTS", "INVENTAIRE"], default="MOUVEMENTS")

# --- SCANNER (Toujours en haut et compact) ---
st.write("📸 **Scanner ici :**")
# On réduit la taille du scanner pour qu'il ne prenne pas tout l'écran
valeur_qr = qrcode_scanner(key='global_scanner')

if mode == "MOUVEMENTS":
    with st.form("form_flux", clear_on_submit=True):
        # On met les options sur une seule ligne pour gagner de la place
        c1, c2 = st.columns(2)
        with c1:
            type_mouv = st.selectbox("Action", ["SORTIE", "ENTRÉE", "PERTE"])
        with c2:
            site = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"])
        
        # Le produit détecté est affiché en petit
        produit = st.text_input("📦 Produit", value=valeur_qr if valeur_qr else "", placeholder="En attente de scan...")
        
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0)
        
        submit = st.form_submit_button("VALIDER")

    if submit and produit:
        st.success(f"Enregistré : {produit}")

else:
    with st.form("form_inv", clear_on_submit=True):
        site_inv = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"])
        prod_inv = st.text_input("📦 Produit", value=valeur_qr if valeur_qr else "")
        q_inv = st.number_input("Stock réel", min_value=0.0)
        
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

st.caption(f"v1.0 | {datetime.now().strftime('%H:%M')}")
