import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="📉 Simulateur Collateral/Borrow", page_icon="🪙", layout="centered")

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
    h1, h2 {
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

# ---------------- CALCULS ----------------
def calc_health_factor(collateral_list, borrow_list):
    total_borrow_usd = sum([b["amount_usd"] for b in borrow_list])
    total_collat_adjusted = sum([
        c["amount_usd"] * (c["liq_threshold"] / 100) for c in collateral_list
    ])

    if total_borrow_usd == 0:
        return float('inf'), total_collat_adjusted, total_borrow_usd

    hf = total_collat_adjusted / total_borrow_usd
    return round(hf, 2), total_collat_adjusted, total_borrow_usd

def calc_token_liquidation_price(token):
    """
    Calcule le prix de liquidation du token en fonction de son seuil de liquidation.
    """
    prix_spot = token["price"]
    liquidation_threshold = token["liq_threshold"] / 100
    prix_liquidation = prix_spot * (1 - liquidation_threshold)

    baisse_pct = round((1 - prix_liquidation / prix_spot) * 100, 2) if prix_spot > 0 else None

    return round(prix_liquidation, 2), baisse_pct

# ---------------- INTERFACE ----------------
st.title("🪙 Simulateur Collatéral & Emprunt")
st.markdown("Simulez votre position de lending/borrowing comme sur Aave, Compound, etc.")

# ---------- Lending ----------
st.subheader("🔐 Tokens déposés en collatéral")
nb_collat = st.number_input("Combien de tokens en collatéral ?", min_value=1, max_value=10, value=1, step=1)

collateral_tokens = []
for i in range(nb_collat):
    st.markdown(f"**Token Collatéral #{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Nom du token", value=f"ETH", key=f"collat_name_{i}")
        price = st.number_input(f"Prix du marché (USD)", value=1700.0, step=10.0, key=f"collat_price_{i}")
        amount = st.number_input(f"Montant déposé (USD)", value=850.0, step=10.0, key=f"collat_amt_{i}")
    with col2:
        ltv_max = st.number_input(f"LTV max autorisé (%)", min_value=10.0, max_value=95.0, value=75.0, step=0.5, key=f"ltv_max_{i}")
        liq_threshold = st.number_input(f"Seuil de liquidation (%)", min_value=10.0, max_value=100.0, value=80.0, step=0.5, key=f"liq_thresh_{i}")
    collateral_tokens.append({
        "name": name,
        "price": price,
        "amount_usd": amount,
        "ltv_max": ltv_max,
        "liq_threshold": liq_threshold
    })

# ---------- Borrowing ----------
st.subheader("💸 Tokens empruntés")
nb_borrow = st.number_input("Combien de tokens empruntés ?", min_value=1, max_value=10, value=1, step=1)

borrowed_tokens = []
for i in range(nb_borrow):
    st.markdown(f"**Token Emprunté #{i+1}**")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Nom du token", value="USDC", key=f"debt_name_{i}")
    with col2:
        amount = st.number_input(f"Montant emprunté (USD)", value=150.0, step=10.0, key=f"debt_amt_{i}")
    borrowed_tokens.append({
        "name": name,
        "amount_usd": amount
    })

# ---------- Simulation ----------
if st.button("🚀 Lancer la simulation"):
    hf, total_collat_adjusted, total_borrow = calc_health_factor(collateral_tokens, borrowed_tokens)

    total_collat_usd = sum([c["amount_usd"] for c in collateral_tokens])
    ltv_courant = (total_borrow / total_collat_usd) * 100 if total_collat_usd > 0 else 0

    st.markdown("## 📊 Résultats globaux")
    st.markdown(f"🔐 **Valeur totale du collatéral (USD)** : `${total_collat_usd}`")
    st.markdown(f"💸 **Total emprunté** : `${total_borrow}`")
    st.markdown(f"📊 **LTV courant de la position** : `{round(ltv_courant, 2)} %`")
    st.markdown(f"🧮 **Health Factor global** (basé sur seuils de liquidation) : `{hf}`")

    if hf < 1.25:
        st.error("🚨 Health Factor critique (< 1.25) → liquidation possible imminente !")
    elif hf < 2:
        st.warning("⚠️ Health Factor modéré (entre 1.25 et 2) → attention")
    else:
        st.success("✅ Position saine (HF ≥ 2) → risque faible")

    # Résumé par token
    st.markdown("## 📒 Détail des tokens déposés")
    for token in collateral_tokens:
        liquidation_price, baisse_pct = calc_token_liquidation_price(token)
        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🪙 {token['name'].upper()}")
        st.markdown(f"💰 Prix marché : **${token['price']}**")
        st.markdown(f"🔒 LTV max autorisé : **{token['ltv_max']}%**")
        st.markdown(f"💣 Seuil de liquidation : **{token['liq_threshold']}%**")
        st.markdown(f"💥 Prix de liquidation : **${liquidation_price}**")
        st.markdown(f"📉 Baisse nécessaire du prix : **{baisse_pct}%**")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 📒 Détail des tokens empruntés")
    for token in borrowed_tokens:
        st.markdown(f"🔸 {token['name'].upper()} : **${token['amount_usd']}**")
