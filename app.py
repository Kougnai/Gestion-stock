import streamlit as st
import pandas as pd
from datetime import datetime

# Config
st.set_page_config(page_title="Stock Scan PRO", layout="centered")

# Style pour optimiser l'espace et les boutons
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3.5em;
        width: 100%;
        background-color: #28a745;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
    }
    .stHeader { padding-top: 0rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Gestion de Stock")

tab_flux, tab_inv = st.tabs(["🔄 MOUVEMENTS", "📋 INVENTAIRE"])

# --- SECTION FLUX ---
with tab_flux:
    with st.form("form_flux", clear_on_submit=True):
        
        # Sélection du Type en mode boutons
        type_mouv = st.segmented_control(
            "Action", 
            ["ENTRÉE", "SORTIE", "PERTE"], 
            default="SORTIE"
        )
        
        # Sélection du Site en mode boutons
        site = st.segmented_control(
            "Site concerné", 
            ["LPB", "GUINGUETTE", "FLAMMA"], 
            default="LPB"
        )
        
        st.divider()

        # Scan & Quantité
        produit = st.text_input("🔍 Scannez le QR Code", key="p_flux")
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0)
        commentaire = st.text_input("Note (optionnel)")
        
        submit = st.form_submit_button("VALIDER LE MOUVEMENT")

    if submit:
        if produit and quantite > 0:
            st.success(f"✅ {type_mouv} à {site} enregistrée !")
        else:
            st.warning("⚠️ Produit ou quantité manquant.")

# --- SECTION INVENTAIRE ---
with tab_inv:
    with st.form("form_inv", clear_on_submit=True):
        
        site_inv = st.segmented_control(
            "Site à inventorier", 
            ["LPB", "GUINGUETTE", "FLAMMA"], 
            default="LPB",
            key="s_inv"
        )
        
        st.divider()
        
        prod_inv = st.text_input("🔍 Produit compté", key="p_inv")
        q_inv = st.number_input("Stock réel total", min_value=0.0)
            
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

st.caption(f"LPB Stock System | {datetime.now().strftime('%d/%m/%Y %H:%M')}")