import streamlit as st

# ---------------------- CSS CUSTOM -----------------------
st.set_page_config(page_title="📉 Crypto Liquidation Calculator", page_icon="🪙", layout="centered")
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

# ---------------------- CALCULS -----------------------
def calculs_liquidation(valeur_token_usd, depot_token_usd, montant_emprunte_usd, seuil_liquidation):
    collatéral_utilisable = depot_token_usd * seuil_liquidation
    HF = collatéral_utilisable / montant_emprunte_usd
    prix_liquidation = (montant_emprunte_usd * valeur_token_usd) / (depot_token_usd * seuil_liquidation)
    baisse_pct = 1 - (prix_liquidation / valeur_token_usd)
    return round(HF, 2), round(prix_liquidation, 2), round(baisse_pct * 100, 2)

# ---------------------- INTERFACE -----------------------

st.title("🪙 Calculateur de Liquidation Crypto (Multi-token)")
st.markdown("Simule la liquidation d’une position **peu importe le token**.")

# Formulaire
with st.form("formulaire"):
    token_nom = st.text_input("💎 Nom du token", value="BTC")
    valeur_token = st.number_input(f"💰 Prix actuel du {token_nom} (USD)", value=100000.0, step=100.0)
    collateral_usd = st.number_input("🔐 Collatéral déposé (en USD)", value=1000.0, step=100.0)
    emprunt = st.number_input("💸 Montant emprunté (en USD)", value=300.0, step=10.0)
    seuil = st.slider("📊 Seuil de liquidation (%)", min_value=50, max_value=90, value=70, step=1)

    submitted = st.form_submit_button("🚀 Lancer le calcul")

# ---------------------- AFFICHAGE -----------------------
if submitted:
    seuil_decimal = seuil / 100
    hf, prix_liquidation, baisse = calculs_liquidation(valeur_token, collateral_usd, emprunt, seuil_decimal)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.markdown(f"🧮 **Health Factor (HF)** : `{hf}`")
    if hf < 1:
        st.error("⚠️ Le Health Factor est inférieur à 1 : votre position est à risque élevé de liquidation !")
    elif hf < 1.5:
        st.warning("⚠️ Le Health Factor est faible, surveillez votre position.")
    else:
        st.success("✅ Le Health Factor est sain.")

    st.markdown(f"💥 **Prix de liquidation du {token_nom}** : `${prix_liquidation}`")
    st.markdown(f"📉 **Baisse nécessaire du {token_nom}** : `{baisse} %`")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    ### 🧾 Résumé :
    - Token : **{token_nom.upper()}**
    - Prix actuel : **${valeur_token}**
    - Collatéral déposé : **${collateral_usd}**
    - Montant emprunté : **${emprunt}**
    - Seuil de liquidation : **{seuil}%**
    
    👉 La liquidation a lieu si **{token_nom.upper()}** tombe à **${prix_liquidation}**,  
    soit une baisse de **{baisse}%**.
    """)

