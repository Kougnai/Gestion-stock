import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
st.set_page_config(page_title="Stock Scan PRO", layout="centered")

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STYLE CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    div.stButton > button:first-child {
        height: 3.5em; width: 100%; background-color: #28a745;
        color: white; font-weight: bold; border-radius: 12px;
    }
    .section-title { font-size: 0.85rem; font-weight: bold; color: #666; margin-bottom: 5px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.title("📲 Gestion de Stock")

# --- NAVIGATION ---
# Note : Vérifie que tes onglets s'appellent bien "Flux" et "Inventaire" (Majuscule au début)
mode = st.segmented_control("CHOISIR LA FEUILLE", ["Sortie", "Inventaire"], default="Sortie")
st.divider()

if mode == "Sortie":
    st.markdown('<p class="section-title">Réglages du mouvement</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        type_mouv = st.pills("Action", ["SORTIE", "PERTE"])
    with col_b:
        site = st.pills("Site", ["LPB", "GUINGUETTE", "FLAMMA"])

    valeur_qr = qrcode_scanner(key='scanner_flux')

    with st.form("form_flux", clear_on_submit=True):
        produit = st.text_input("📦 Produit détecté", value=valeur_qr if valeur_qr else "")
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0, value=1.0)
        commentaire = st.text_input("Note (optionnel)")
        submit = st.form_submit_button("VALIDER LE FLUX")

    if submit:
        if produit and quantite > 0:
            # 1. Lecture sans cache pour éviter les conflits
            df_actuel = conn.read(worksheet="Sortie", ttl=0)
            
            # 2. Création de la ligne (Noms de colonnes alignés sur ton Sheet)
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Type de mouvement": type_mouv,
                "Site": site,
                "Articles": produit,
                "Quantité": quantite,
                "Note": commentaire
            }])
            
            # 3. Fusion
            df_final = pd.concat([df_actuel, new_row], ignore_index=True)
            
            # 4. Mise à jour
            conn.update(worksheet="Sortie", data=df_final)
            
            st.success(f"✅ Sortie enregistré : {produit}")
            
        else:
            st.error("Veuillez remplir le produit et la quantité")

else: # --- MODE INVENTAIRE ---
    st.markdown('<p class="section-title">Réglages Inventaire</p>', unsafe_allow_html=True)
    site_inv = st.pills("Site à inventorier", ["LPB", "GUINGUETTE", "FLAMMA"])
    
    valeur_qr_inv = qrcode_scanner(key='scanner_inv')

    with st.form("form_inv", clear_on_submit=True):
        prod_inv = st.text_input("📦 Produit détecté", value=valeur_qr_inv if valeur_qr_inv else "")
        q_inv = st.number_input("Stock réel total", min_value=0.0, step=1.0)
        submit_inv = st.form_submit_button("FIXER L'INVENTAIRE")

    if submit_inv:
        if prod_inv:
            # 1. Lecture
            df_inv_actuel = conn.read(worksheet="Inventaire", ttl=0)
            
            # 2. Ligne (Ajuste les noms ci-dessous selon ton onglet Inventaire)
            new_inv = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Site": site_inv,
                "Articles": prod_inv,
                "Stock Réel": q_inv
            }])
            
            # 3. Fusion
            df_inv_final = pd.concat([df_inv_actuel, new_inv], ignore_index=True)
            
            # 4. Mise à jour
            conn.update(worksheet="Inventaire", data=df_inv_final)
            
            st.success(f"✅ Inventaire mis à jour pour {prod_inv}")
            
        else:
            st.error("Scannez un produit")

st.caption(f"LPB Stock System | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
