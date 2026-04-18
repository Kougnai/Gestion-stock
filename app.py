import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from st_gsheets_connection import GSheetsConnection
from streamlit_qrcode_scanner import qrcode_scanner

# Config Page
st.set_page_config(page_title="LPB Stock Scan", layout="centered")

# Connexion Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📲 Gestion de Stock")

# --- NAVIGATION ---
mode = st.segmented_control("CHOISIR LA FEUILLE", ["FLUX", "INVENTAIRE"], default="FLUX")

st.divider()

if mode == "FLUX":
    # 1. Réglages hauts
    col1, col2 = st.columns(2)
    with col1:
        type_mouv = st.selectbox("Action", ["SORTIE", "ENTRÉE", "PERTE"])
    with col2:
        site = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"])

    # 2. Scanner
    valeur_qr = qrcode_scanner(key='scanner_flux')

    # 3. Formulaire
    with st.form("form_flux", clear_on_submit=True):
        produit = st.text_input("📦 Produit détecté", value=valeur_qr if valeur_qr else "")
        quantite = st.number_input("Quantité", min_value=0.1, step=1.0, value=1.0)
        commentaire = st.text_input("Note (optionnel)")
        submit = st.form_submit_button("VALIDER LE FLUX")

    if submit:
        if produit:
            new_data = pd.DataFrame([{
                "ID_mouvement": str(uuid.uuid4())[:8],
                "Date_heure": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Produit": produit,
                "Type": type_mouv,
                "Site": site,
                "Quantité": quantite if type_mouv == "ENTRÉE" else -quantite,
                "Commentaire": commentaire
            }])
            try:
                existing_data = conn.read(worksheet="Flux")
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(worksheet="Flux", data=updated_df)
                st.success("✅ Flux enregistré dans Google Sheets !")
                st.balloons()
            except Exception as e:
                st.error(f"Erreur : {e}")

else:
    # --- MODE INVENTAIRE ---
    site_inv = st.selectbox("Site", ["LPB", "GUINGUETTE", "FLAMMA"], key="s_inv")
    valeur_qr_inv = qrcode_scanner(key='scanner_inv')

    with st.form("form_inv", clear_on_submit=True):
        prod_inv = st.text_input("📦 Produit", value=valeur_qr_inv if valeur_qr_inv else "")
        q_inv = st.number_input("Stock réel compté", min_value=0.0, step=1.0)
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

    if submit_inv:
        if prod_inv:
            new_inv = pd.DataFrame([{
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Produit": prod_inv,
                "Stock_Reel": q_inv,
                "Site": site_inv
            }])
            try:
                data_inv = conn.read(worksheet="Inventaire")
                updated_inv = pd.concat([data_inv, new_inv], ignore_index=True)
                conn.update(worksheet="Inventaire", data=updated_inv)
                st.success("✅ Inventaire mis à jour !")
            except Exception as e:
                st.error(f"Erreur : {e}")

st.caption(f"Connecté à la feuille LPB | {datetime.now().strftime('%H:%M')}")
