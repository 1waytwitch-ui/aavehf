import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="📉 Simulateur DeFi Collateral/Borrow", page_icon="🪙", layout="centered")

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

# ---------------- CALCUL ----------------
def calc_health_factor(collateral_list, borrow_list):
    total_collat_usd = sum([c["amount_usd"] * c["ltv"] for c in collateral_list])
    total_borrow_usd = sum([b["amount_usd"] for b in borrow_list])
    if total_borrow_usd == 0:
        return float('inf'), total_collat_usd, total_borrow_usd
    hf = total_collat_usd / total_borrow_usd
    return round(hf, 2), total_collat_usd, total_borrow_usd

def calc_token_liquidation_price(token):
    try:
        return round((token["amount_usd"] * token["price"]) / (token["amount_usd"] * token["ltv"]), 2)
    except ZeroDivisionError:
        return None

# ---------------- INTERFACE ----------------
st.title("🪙 Simulateur DeFi : Collatéral & Emprunt Multi-token")
st.markdown("Gérez indépendamment vos positions de **lending** et **borrowing**, comme sur Aave, Compound ou Venus.")

# ---------- Lending ----------
st.subheader("🔐 Tokens déposés en collatéral")
nb_collat = st.number_input("Combien de tokens en collatéral ?", min_value=1, max_value=10, value=2, step=1)

collateral_tokens = []
for i in range(nb_collat):
    st.markdown(f"**Token Collatéral #{i+1}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input(f"Nom du token", value=f"ETH", key=f"collat_name_{i}")
        price = st.number_input(f"Prix actuel (USD)", value=1700.0, step=10.0, key=f"collat_price_{i}")
    with col2:
        amount = st.number_input(f"Montant déposé (USD)", value=850.0, step=10.0, key=f"collat_amt_{i}")
        ltv_pct = st.slider(f"Seuil de liquidation (%)", min_value=50, max_value=90, value=70, step=1, key=f"ltv_{i}")
    with col3:
        pass
    collateral_tokens.append({
        "name": name,
        "price": price,
        "amount_usd": amount,
        "ltv": ltv_pct / 100
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

# ---------- Calcul et affichage ----------
if st.button("🚀 Lancer la simulation"):
    hf, total_collat, total_borrow = calc_health_factor(collateral_tokens, borrowed_tokens)

    st.markdown("## 📊 Résultats globaux")
    st.markdown(f"🔐 **Valeur totale du collatéral (ajustée LTV)** : `${total_collat}`")
    st.markdown(f"💸 **Total emprunté** : `${total_borrow}`")
    st.markdown(f"🧮 **Health Factor global** : `{hf}`")

    if hf < 1:
        st.error("⚠️ Health Factor < 1 → liquidation possible imminente !")
    elif hf < 1.5:
        st.warning("⚠️ Health Factor faible → risque modéré")
    else:
        st.success("✅ Position saine → risque faible")

    # Résumé par token
    st.markdown("## 🧾 Détail des tokens déposés")
    for token in collateral_tokens:
        liquidation_price = calc_token_liquidation_price(token)
        baisse_pct = round(100 - (liquidation_price / token["price"] * 100), 2)
        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🪙 {token['name'].upper()}")
        st.markdown(f"💰 Prix actuel : **${token['price']}**")
        st.markdown(f"💥 Prix de liquidation : **${liquidation_price}**")
        st.markdown(f"📉 Baisse nécessaire : **{baisse_pct}%**")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 🧾 Détail des tokens empruntés")
    for token in borrowed_tokens:
        st.markdown(f"🔸 {token['name'].upper()} : **${token['amount_usd']}**")

