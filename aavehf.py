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

# ----------- CALCUL -----------
def calculs_liquidation(prix_collat_usd, collateral_usd, dette_usd, seuil_liquidation):
    collatéral_utilisable = collateral_usd * seuil_liquidation
    HF = collatéral_utilisable / dette_usd
    prix_liquidation = (dette_usd * prix_collat_usd) / (collateral_usd * seuil_liquidation)
    baisse_pct = 1 - (prix_liquidation / prix_collat_usd)
    return round(HF, 2), round(prix_liquidation, 2), round(baisse_pct * 100, 2)

# ----------- TITRE -----------
st.title("🪙 Simulateur de Liquidation Multi-Token")
st.markdown("Gérez des scénarios où le **collatéral** et la **dette** sont dans **des tokens différents**.")

# ----------- NOMBRE DE SIMULATIONS -----------
nb_tokens = st.number_input("🔢 Combien de positions voulez-vous simuler ?", min_value=1, max_value=10, value=2, step=1)

token_data = []
with st.form("form_tokens"):
    for i in range(nb_tokens):
        st.markdown(f"### 🧮 Position #{i+1}")

        col1, col2 = st.columns(2)
        with col1:
            collat_token = st.text_input(f"🔐 Token déposé (collatéral)", value="ETH", key=f"collat_token_{i}")
            collat_prix = st.number_input(f"💰 Prix du token {collat_token} (USD)", value=1700.0, step=10.0, key=f"collat_prix_{i}")
            collat_usd = st.number_input(f"💼 Valeur totale déposée en USD", value=850.0, step=10.0, key=f"collat_usd_{i}")
            seuil = st.slider("📊 Seuil de liquidation (%)", 50, 90, 70, 1, key=f"seuil_{i}")

        with col2:
            debt_token = st.text_input(f"💸 Token emprunté", value="USDC", key=f"debt_token_{i}")
            debt_usd = st.number_input(f"💵 Montant emprunté en USD", value=150.0, step=10.0, key=f"debt_usd_{i}")

        token_data.append({
            "collat_token": collat_token,
            "collat_prix": collat_prix,
            "collat_usd": collat_usd,
            "debt_token": debt_token,
            "debt_usd": debt_usd,
            "seuil": seuil / 100
        })

    submitted = st.form_submit_button("🚀 Lancer la simulation")

# ----------- AFFICHAGE DES RÉSULTATS -----------
if submitted:
    st.markdown("## 📊 Résultats de la simulation")
    for token in token_data:
        hf, prix_liquidation, baisse = calculs_liquidation(
            token["collat_prix"],
            token["collat_usd"],
            token["debt_usd"],
            token["seuil"]
        )

        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🔹 {token['collat_token'].upper()} (collatéral) → {token['debt_token'].upper()} (dette)")
        st.markdown(f"🧮 **Health Factor (HF)** : `{hf}`")
        if hf < 1:
            st.error("⚠️ Le Health Factor est < 1 : RISQUE DE LIQUIDATION !")
        elif hf < 1.5:
            st.warning("⚠️ Health Factor faible, restez vigilant.")
        else:
            st.success("✅ Position saine.")

        st.markdown(f"💥 **Prix de liquidation du {token['collat_token'].upper()}** : `${prix_liquidation}`")
        st.markdown(f"📉 **Baisse nécessaire du {token['collat_token'].upper()}** : `{baisse}%`")
        st.markdown(f"📌 **Montant emprunté :** {token['debt_usd']} {token['debt_token'].upper()}")
        st.markdown("</div>", unsafe_allow_html=True)
