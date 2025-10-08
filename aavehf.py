import streamlit as st

# ---------- THÈME ET STYLE CSS ----------
st.set_page_config(page_title="📉 Crypto Liquidation Calculator", page_icon="🪙", layout="centered")

# Injecter du CSS personnalisé
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
            color: #ffffff;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stNumberInput > div > div {
            background-color: #1f222a;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #10cfc9;
            color: black;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #08b1aa;
            color: white;
        }
        h1 {
            color: #10cfc9;
        }
        .result-box {
            background-color: #1f222a;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- TITRE ----------
st.title("🪙 Crypto Liquidation Calculator")
st.markdown("**Simule le prix de liquidation d’une position crypto 🔥**")

# ---------- FORMULAIRE ----------
with st.form("formulaire"):
    valeur_btc = st.number_input("💰 Prix actuel du BTC (USD)", value=100000.0, step=1000.0)
    collateral_usd = st.number_input("🔐 Collatéral déposé (en USD)", value=1000.0, step=100.0)
    emprunt = st.number_input("💸 Montant emprunté (en USD)", value=300.0, step=10.0)
    seuil = st.slider("📊 Seuil de liquidation (%)", min_value=50, max_value=90, value=70, step=1)

    submitted = st.form_submit_button("🚀 Lancer le calcul")

# ---------- CALCULS ----------
def calculs_liquidation(valeur_btc_usd, depot_btc_usd, montant_emprunte_usd, seuil_liquidation):
    collatéral_utilisable = depot_btc_usd * seuil_liquidation
    HF = collatéral_utilisable / montant_emprunte_usd
    prix_liquidation = (montant_emprunte_usd * valeur_btc_usd) / (depot_btc_usd * seuil_liquidation)
    baisse_pct = 1 - (prix_liquidation / valeur_btc_usd)
    return round(HF, 2), round(prix_liquidation, 2), round(baisse_pct * 100, 2)

# ---------- AFFICHAGE DES RÉSULTATS ----------
if submitted:
    seuil_decimal = seuil / 100
    hf, prix_liquidation, baisse = calculs_liquidation(valeur_btc, collateral_usd, emprunt, seuil_decimal)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.markdown(f"🧮 **Health Factor (HF)** : `{hf}`")
    if hf < 1:
        st.error("⚠️ Le Health Factor est inférieur à 1 : votre position est à risque élevé de liquidation !")
    elif hf < 1.5:
        st.warning("⚠️ Le Health Factor est faible, surveillez votre position.")
    else:
        st.success("✅ Le Health Factor est sain.")

    st.markdown(f"💥 **Prix de liquidation du BTC** : `${prix_liquidation}`")
    st.markdown(f"📉 **Baisse nécessaire du BTC** : `{baisse} %`")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    ### 🧾 Résumé :
    - Si le BTC vaut **${valeur_btc}**,
    - Avec un collatéral de **${collateral_usd}** et une dette de **${emprunt}**,
    - Alors la liquidation aurait lieu si le BTC tombe à **${prix_liquidation}**,  
      soit une **baisse de {baisse} %**.
    """)

