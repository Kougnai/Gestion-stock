import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner

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
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Gestion de Stock")

tab_flux, tab_inv = st.tabs(["🔄 MOUVEMENTS", "📋 INVENTAIRE"])

# --- SECTION FLUX ---
with tab_flux:
    st.subheader("Scanner un produit")
    # Le scanner est placé ici, il écrit dans 'valeur_qr'
    valeur_qr = qrcode_scanner(key='scanner_flux')
    
    with st.form("form_flux", clear_on_submit=True):
        type_mouv = st.segmented_control(
            "Action", ["ENTRÉE", "SORTIE", "PERTE"], default="SORTIE"
        )
        
        site = st.segmented_control(
            "Site concerné", ["LPB", "GUINGUETTE", "FLAMMA"], default="LPB"
        )
        
        st.divider()

        # Le champ produit récupère automatiquement la valeur du scanner
        produit = st.text_input("📦 Produit détecté", value=valeur_qr if valeur_qr else "", key="p_flux")
        
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0)
        commentaire = st.text_input("Note (optionnel)")
        
        submit = st.form_submit_button("VALIDER LE MOUVEMENT")

    if submit:
        if produit and quantite > 0:
            st.success(f"✅ Enregistré : {type_mouv} de {quantite} sur {site}")
        else:
            st.warning("⚠️ Scannez un produit et indiquez une quantité.")

# --- SECTION INVENTAIRE ---
with tab_inv:
    st.subheader("Scanner pour Inventaire")
    valeur_qr_inv = qrcode_scanner(key='scanner_inv')

    with st.form("form_inv", clear_on_submit=True):
        site_inv = st.segmented_control(
            "Site", ["LPB", "GUINGUETTE", "FLAMMA"], default="LPB", key="s_inv"
        )
        
        st.divider()
        
        prod_inv = st.text_input("📦 Produit détecté", value=valeur_qr_inv if valeur_qr_inv else "", key="p_inv")
        q_inv = st.number_input("Stock réel total", min_value=0.0)
            
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

st.caption(f"LPB Stock System | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
