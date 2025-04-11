import streamlit as st
import time
# Funksionet kryesore

def calculate_price(platts, premium, base_density, day_density):
    from decimal import Decimal, getcontext, ROUND_DOWN
    getcontext().prec = 12
    getcontext().rounding = ROUND_DOWN

    platts = Decimal(str(platts))
    premium = Decimal(str(premium))
    base_density = Decimal(str(base_density))
    day_density = Decimal(str(day_density))

    base_price = platts + premium
    density_ratio = base_density / day_density
    corrected_price = base_price * density_ratio
    escalation = corrected_price - base_price
    final_price = platts + premium + escalation
    return float(final_price)

def calculate_premium(final_price, platts, day_density, base_density):
    base_ratio = base_density / day_density
    premium = (final_price / base_ratio) - platts
    return round(premium, 2)

# Konfigurime të ruajtura në session state
if "default_diesel_density" not in st.session_state:
    st.session_state.default_diesel_density = 0.8305

if "default_gasoline_density" not in st.session_state:
    st.session_state.default_gasoline_density = 0.7407

if "preset_premium" not in st.session_state:
    st.session_state.preset_premium = 0.0
    st.session_state.preset_premiums = [10.0, 12.0, 15.0, 20.0, 60.0]

st.set_page_config(page_title="Llogaritësi i Çmimit të Naftës dhe Benzinës", layout="centered")
st.title("⛽ Llogaritësi i Çmimit të Naftës dhe Benzinës")

st.sidebar.header("⚙️ Cilësime")

# Kursi i këmbimit
st.sidebar.subheader("💱 Kurset e Këmbimit")
all_usd = st.sidebar.number_input("Kursi ALL/USD", min_value=0.0, value=100.0, step=0.01, format="%.2f")
all_eur = st.sidebar.number_input("Kursi ALL/EUR", min_value=0.0, value=105.0, step=0.01, format="%.2f")

# Llogarit raportin USD/EUR dhe EUR/USD
usd_eur = round(all_usd / all_eur, 6) if all_usd > 0 and all_eur > 0 else None
eur_usd = round(all_eur / all_usd, 6) if all_usd > 0 and all_eur > 0 else None

# Shfaq raportet pas inputeve
if usd_eur and eur_usd:
    st.sidebar.caption(f"USD/EUR: {usd_eur:.6f}")
    st.sidebar.caption(f"EUR/USD: {eur_usd:.6f}")
usd_eur = round(all_usd / all_eur, 6) if all_usd > 0 and all_eur > 0 else None
eur_usd = round(all_eur / all_usd, 6) if all_usd > 0 and all_eur > 0 else None

# Cilësime për densitetet
st.session_state.default_diesel_density = st.sidebar.number_input(
    "Densiteti i ruajtur për Naftën",
    min_value=0.0, step=0.0001,
    value=st.session_state.default_diesel_density,
    format="%.4f",
    )

st.session_state.default_gasoline_density = st.sidebar.number_input(
    "Densiteti i ruajtur për Benzinën",
    min_value=0.0, step=0.0001,
    value=st.session_state.default_gasoline_density,
    format="%.4f"
)

# Premiume të paracaktuara
st.sidebar.subheader("💰 Premium i Paracaktuar")
st.session_state.preset_premium = st.sidebar.number_input(
    "Vendos Premium-in që do ruhet",
    value=st.session_state.preset_premium,
    step=0.1,
    format="%.2f",
    key="preset_premium_input"
)

col1, col2 = st.columns(2, gap="small")

# Nafta
with col1:
    st.header("Nafta")
    diesel_density = st.number_input("Densiteti i Ditës (Naftë)", min_value=0.0, step=0.0001, format="%.4f", value=st.session_state.default_diesel_density, key="diesel_density")
    diesel_platts = st.number_input("Platts ($)", min_value=0.0, step=0.1, key="diesel_platts")
    diesel_premium = st.number_input("Premium ($) (opsionale)", value=st.session_state.preset_premium, step=0.1, key="diesel_premium")
    diesel_final = st.number_input("Çmimi Final ($/MT) (opsionale)", value=0.0, step=0.1, key="diesel_final")

    diesel_price = None
    diesel_premium_calc = None

    if diesel_premium > 0:
        diesel_price = calculate_price(diesel_platts, diesel_premium, 0.8450, diesel_density)
        diesel_premium_calc = diesel_premium
    elif diesel_final > 0:
        diesel_price = diesel_final
        diesel_premium_calc = calculate_premium(diesel_final, diesel_platts, diesel_density, 0.8450)

    # Calculate price in EUR by multiplying the price in USD by the USD/EUR rate
    if diesel_price and usd_eur:
        diesel_price_eur = diesel_price * usd_eur
        diesel_price_eur_display = f"{diesel_price_eur:.2f}"  # Format to 2 decimal places
    else:
        diesel_price_eur_display = "-"
    
    st.subheader(f"Çmimi për ton: {diesel_price + 0.00001:.2f} $/MT" if diesel_price else "Çmimi për ton: - $/MT")
    st.caption(f"Çmimi për ton në EUR: {diesel_price_eur_display} €/MT")
    st.caption(f"Premium i llogaritur: {diesel_premium_calc if diesel_premium_calc else '-'} $")

# Benzina
with col2:
    st.header("Benzina")
    gasoline_density = st.number_input("Densiteti i Ditës (Benzinë)", min_value=0.0, step=0.0001, format="%.4f", value=st.session_state.default_gasoline_density, key="gasoline_density")
    gasoline_platts = st.number_input("Platts ($)", min_value=0.0, step=0.1, key="gasoline_platts")
    gasoline_premium = st.number_input("Premium ($) (opsionale)", value=st.session_state.preset_premium, step=0.1, key="gasoline_premium")
    gasoline_final = st.number_input("Çmimi Final ($/MT) (opsionale)", value=0.0, step=0.1, key="gasoline_final")

    gasoline_price = None
    gasoline_premium_calc = None

    if gasoline_premium > 0:
        gasoline_price = calculate_price(gasoline_platts, gasoline_premium, 0.7550, gasoline_density)
        gasoline_premium_calc = gasoline_premium
    elif gasoline_final > 0:
        gasoline_price = gasoline_final
        gasoline_premium_calc = calculate_premium(gasoline_final, gasoline_platts, gasoline_density, 0.7550)

    # Calculate price in EUR by multiplying the price in USD by the USD/EUR rate
    if gasoline_price and usd_eur:
        gasoline_price_eur = gasoline_price * usd_eur
        gasoline_price_eur_display = f"{gasoline_price_eur:.2f}"  # Format to 2 decimal places
    else:
        gasoline_price_eur_display = "-"
    
    st.subheader(f"Çmimi për ton: {gasoline_price + 0.00001:.2f} $/MT" if gasoline_price else "Çmimi për ton: - $/MT")
    st.caption(f"Çmimi për ton në EUR: {gasoline_price_eur_display} €/MT")
    st.caption(f"Premium i llogaritur: {gasoline_premium_calc if gasoline_premium_calc else '-'} $")

# Tabela shtesë poshtë kolones Nafta dhe Benzina

# Cmimet në USD për premiumet 12, 13, 14, 15 për naftë (me çmim të benzinës me premium 60)
with st.container():
    st.markdown("### 📊 Çmimet në USD për Naftë (Premiumet 12–15) + Benzinë me Premium 60")
    st.markdown("""<style>
    .grid-table div[data-testid="column"] {
        border: 1px solid #ccc;
        padding: 5px;
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    @media screen and (max-width: 768px) {
        .element-container { padding: 0 5px !important; }
        h2, h3, .markdown-text-container { font-size: 16px !important; }
        .stNumberInput input { font-size: 14px !important; height: 30px !important; }
    }
</style>""", unsafe_allow_html=True)
    col1_usd, col2_usd, col3_usd = st.columns(3)
    with col1_usd:
        st.markdown("**Premium ($)**")
        for prem in [12, 13, 14, 15]:
            st.markdown(f"{prem}")
    with col2_usd:
        st.markdown("**Çmimi Naftë $/MT**")
        for prem in [12, 13, 14, 15]:
            if diesel_platts and diesel_density:
                val = calculate_price(diesel_platts, prem, 0.8450, diesel_density)
                st.markdown(f"{round(val + 0.00001, 2):,.2f}")
            else:
                st.markdown("-")
    with col3_usd:
        st.markdown("**Çmimi Benzinë $/MT**")
        for _ in [12, 13, 14, 15]:
            if gasoline_platts and gasoline_density:
                val = calculate_price(gasoline_platts, 60, 0.7550, gasoline_density)
                st.markdown(f"{round(val + 0.00001, 2):,.2f}")
            else:
                st.markdown("-")

# Cmimet në EUR për Naftë dhe Benzinë (Premiumet 11–13 për Naftë) + Benzinë me Premium 60
with st.container():
    st.markdown("### 📊 Çmimet në EUR për Naftë (Premiumet 11–13) + Benzinë me Premium 60")
    st.markdown("""<style>
        .grid-table div[data-testid="column"] {border: 1px solid #ccc; padding: 5px;}
    </style>""", unsafe_allow_html=True)
    col1_eur, col2_eur, col3_eur = st.columns(3)
    with col1_eur:
        st.markdown("**Premium (€)**")
        for prem in [11, 12, 13]:
            st.markdown(f"{prem}")
    with col2_eur:
        st.markdown("**Çmimi Naftë €/MT**")
        for prem in [11, 12, 13]:
            if all([diesel_platts > 0, diesel_density > 0, usd_eur > 0]):
                val = calculate_price(diesel_platts, prem, 0.8450, diesel_density)
                val_eur = val * usd_eur
                # Format the EUR price with exactly two decimal places (without rounding)
                val_eur_display = f"{val_eur:.2f}"
                st.markdown(f"{val_eur_display}")
            else:
                st.markdown("-")
    with col3_eur:
        st.markdown("**Çmimi Benzinë €/MT**")
        for _ in [11, 12, 13]:
            if gasoline_platts and gasoline_density and usd_eur:
                val = calculate_price(gasoline_platts, 60, 0.7550, gasoline_density)
                val_eur = val * usd_eur
                # Format the EUR price with exactly two decimal places (without rounding)
                val_eur_display = f"{val_eur:.2f}"
                st.markdown(f"{val_eur_display}")
            else:
                st.markdown("-")

# Reklama fundore me link klikues
st.markdown("""
    <div style='text-align:center; margin-top:50px;'>
        <a href='https://www.instagram.com/lux.travelagency/?hl=en' target='_blank'>
            <h2 style='color:red; animation:pulse 2s infinite; font-size:28px;'>
                KY APLIKACION MUNDËSOHET NGA LUX TRAVEL AGENCY
            </h2>
        </a>
    </div>
    <style>
    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.4; }
      100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)
