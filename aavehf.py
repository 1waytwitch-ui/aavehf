# app.py

import streamlit as st

def calculs_liquidation(valeur_btc_usd, depot_btc_usd, montant_emprunte_usd, seuil_liquidation):
    # 1. Health Factor
    collatéral_utilisable = depot_btc_usd * seuil_liquidation
    HF = collatéral_utilisable / montant_emprunte_usd

    # 2. Prix de liquidation
    prix_liquidation = (montant_emprunte_usd * valeur_btc_usd) / (depot_btc_usd * seuil_liquidation)

    # 3. Baisse nécessaire
    baisse_pct = 1 - (prix_liquidation / valeur_btc_usd)

    return round(HF, 2), round(prix_liquidation, 2), round(baisse_pct * 100, 2)


# -------------------
# INTERFACE STREAMLIT
# -------------------

st.set_page_config(page_title="Calculateur de Liquidation Crypto", page_icon="📉")
st.title("📉 Calculateur de Health Factor & Liquidation")
st.markdown("Entrez les données ci-dessous pour simuler la liquidation d'une position crypto.")

# Entrées utilisateur
valeur_btc = st.number_input("💰 Valeur actuelle du BTC (en $)", value=100000.0, step=1000.0)
collateral_usd = st.number_input("🔐 Valeur déposée en BTC (en $)", value=1000.0, step=100.0)
emprunt = st.number_input("💸 Montant emprunté (en $)", value=300.0, step=10.0)
seuil = st.slider("📊 Seuil de liquidation (en %)", min_value=50, max_value=90, value=70, step=1)

# Bouton de calcul
if st.button("📊 Calculer"):
    seuil_decimal = seuil / 100
    hf, prix_liquidation, baisse = calculs_liquidation(valeur_btc, collateral_usd, emprunt, seuil_decimal)

    st.success(f"✅ Health Factor : {hf}")
    st.info(f"💥 Prix de liquidation du BTC ≈ **${prix_liquidation}**")
    st.warning(f"📉 Baisse nécessaire du BTC ≈ **{baisse} %**")

    # Résumé textuel
    st.markdown("---")
    st.markdown(f"""
    **Résumé :**  
    Si le BTC vaut **${valeur_btc}**, que vous avez déposé **${collateral_usd}** en collatéral et emprunté **${emprunt}**,  
    alors votre position sera liquidée si le BTC tombe à environ **${prix_liquidation}**,  
    soit une baisse de **{baisse} %** par rapport au prix initial.
    """)
