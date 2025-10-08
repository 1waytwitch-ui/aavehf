import streamlit as st

# ----------- CONFIG & CSS -----------
st.set_page_config(page_title="📉 Simulateur Multi-Token", page_icon="🪙", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
            color: #ffffff;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stNumberInput > div > div, .stTextInput > div > input {
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

# ----------- FONCTION DE CALCUL -----------
def calculs_liquidation(prix, collateral_usd, dette_usd, seuil_liquidation):
    collatéral_utilisable = collateral_usd * seuil_liquidation
    HF = collatéral_utilisable / dette_usd
    prix_liquidation = (dette_usd * prix) / (collateral_usd * seuil_liquidation)
    baisse_pct = 1 - (prix_liquidation / prix)
    return round(HF, 2), round(prix_liquidation, 2), round(baisse_pct * 100, 2)

# ----------- TITRE -----------
st.title("🪙 Simulateur Multi-Token de Liquidation")
st.markdown("Comparez plusieurs positions crypto et leurs risques de liquidation 🔥")

# ----------- NOMBRE DE TOKENS -----------
nb_tokens = st.number_input("🔢 Combien de tokens voulez-vous simuler ?", min_value=1, max_value=10, value=2, step=1)

# ----------- FORMULAIRES MULTIPLES -----------
token_data = []
with st.form("form_tokens"):
    for i in range(nb_tokens):
        st.markdown(f"### Token #{i+1}")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input(f"🪙 Nom du token #{i+1}", value=f"Token{i+1}", key=f"nom_{i}")
            prix = st.number_input(f"💰 Prix actuel de {nom} (USD)", value=100.0, step=1.0, key=f"prix_{i}")
            seuil_pct = st.slider(f"📊 Seuil de liquidation (%) pour {nom}", 50, 90, 70, 1, key=f"seuil_{i}")
        with col2:
            collat = st.number_input(f"🔐 Collatéral déposé (USD)", value=1000.0, step=50.0, key=f"collat_{i}")
            dette = st.number_input(f"💸 Montant emprunté (USD)", value=300.0, step=10.0, key=f"dette_{i}")

        token_data.append({
            "nom": nom,
            "prix": prix,
            "collateral": collat,
            "dette": dette,
            "seuil": seuil_pct / 100
        })

    submitted = st.form_submit_button("🚀 Lancer la simulation")

# ----------- AFFICHAGE DES RÉSULTATS -----------
if submitted:
    st.markdown("## 📊 Résultats de la simulation")
    for token in token_data:
        hf, prix_liquidation, baisse = calculs_liquidation(
            token["prix"], token["collateral"], token["dette"], token["seuil"]
        )

        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🔹 {token['nom'].upper()}")
        st.markdown(f"🧮 **Health Factor (HF)** : `{hf}`")
        if hf < 1:
            st.error("⚠️ Le Health Factor est < 1 : RISQUE DE LIQUIDATION !")
        elif hf < 1.5:
            st.warning("⚠️ Health Factor faible, restez vigilant.")
        else:
            st.success("✅ Position saine.")

        st.markdown(f"💥 **Prix de liquidation :** `${prix_liquidation}`")
        st.markdown(f"📉 **Baisse nécessaire :** `{baisse}%`")
        st.markdown("</div>", unsafe_allow_html=True)
