import streamlit as st
import json
import os
import get_rates

st.set_page_config(page_title="出國試算小幫手", page_icon="🐰", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap');
    :root {
        --ink: #59463e;
        --ink-muted: #8a766c;
        --cream: #fffaf5;
        --petal: #ffdce8;
        --mint-soft: #d9f5ec;
        --honey: #ffecc9;
        --line-soft: rgba(139, 99, 86, 0.18);
        --radius-xl: 22px;
        --radius-lg: 18px;
        --radius-pill: 999px;
    }
    .stApp {
        font-family: "Zen Maru Gothic", ui-rounded,
            "Hiragino Maru Gothic ProN", "Segoe UI Variable Display",
            "Microsoft JhengHei UI", sans-serif;
        background-color: #fef6ef;
        background-image:
            radial-gradient(760px 480px at 8% -5%, rgba(255, 220, 232, 0.75), transparent 60%),
            radial-gradient(700px 420px at 95% -2%, rgba(210, 244, 230, 0.65), transparent 55%),
            radial-gradient(520px 360px at 50% 104%, rgba(255, 236, 201, 0.55), transparent 55%);
        background-attachment: fixed;
    }
    /* 勿對全域 span 強制字型：會覆蓋 expander 圖示的 icon font，出現字面 "arrow_down" 與中文疊在一起 */
    [data-testid="stMarkdownContainer"],
    .stApp p,
    .stApp label,
    .stApp li {
        font-family: "Zen Maru Gothic", ui-rounded,
            "Hiragino Maru Gothic ProN", "Segoe UI Variable Display",
            "Microsoft JhengHei UI", sans-serif;
    }
    [data-testid="stExpander"] summary {
        display: flex !important;
        align-items: center !important;
        gap: 0.6rem !important;
        flex-wrap: nowrap !important;
    }
    .block-container {
        padding-top: 1.85rem;
        padding-bottom: 3rem;
        max-width: 920px;
    }
    h1 {
        color: var(--ink) !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        line-height: 1.3 !important;
    }
    h2, h3 {
        color: var(--ink) !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stDecoration"] svg path,
    [data-testid="stDecoration"] svg rect { opacity: 0.35 !important; }
    [data-testid="stCaptionContainer"] {
        color: var(--ink-muted) !important;
        font-size: 0.98rem !important;
    }
    hr {
        margin: 1.25rem 0;
        border: none;
        border-top: 2px dashed var(--line-soft);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 253, 0.65);
        padding: 12px;
        border-radius: var(--radius-xl);
        border: 2px dashed var(--line-soft);
        box-shadow: 6px 6px 0 rgba(251, 199, 210, 0.28);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-pill) !important;
        padding: 0.45rem 1.15rem !important;
        font-weight: 700 !important;
        color: var(--ink) !important;
        border: none !important;
        background: rgba(255, 255, 255, 0.75) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(165deg, #ffe6f2 10%, #fff2f7 92%) !important;
        color: var(--ink) !important;
        border: 2px solid rgba(255, 170, 198, 0.55) !important;
        box-shadow: 5px 5px 0 rgba(253, 180, 200, 0.35);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--radius-xl) !important;
        border: 2px dashed var(--line-soft) !important;
        background:
            linear-gradient(160deg, rgba(255, 255, 255, 0.92) 0%, rgba(254, 250, 244, 0.95) 100%) !important;
        box-shadow: 8px 8px 0 rgba(229, 198, 180, 0.24);
    }
    [data-testid="stMetric"] {
        background: linear-gradient(175deg, #fffefc 8%, var(--mint-soft) 92%);
        border-radius: calc(var(--radius-xl) + 4px);
        padding: 1.15rem 1.35rem !important;
        border: 2px solid rgba(141, 210, 191, 0.45);
        box-shadow: 9px 9px 0 rgba(173, 220, 200, 0.28);
    }
    [data-testid="stMetric"] label p {
        color: var(--ink-muted) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-variant-numeric: tabular-nums;
        font-weight: 700 !important;
    }
    .stButton > button {
        border-radius: var(--radius-pill);
        font-weight: 700;
        letter-spacing: 0.02em;
        border: 2px solid rgba(232, 196, 120, 0.75);
        background: linear-gradient(180deg, #fffbf0, var(--honey));
        color: var(--ink);
        box-shadow: 6px 6px 0 rgba(239, 210, 150, 0.55);
        transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
    }
    .stButton > button:hover {
        box-shadow: 4px 4px 0 rgba(239, 210, 150, 0.45);
        color: var(--ink);
        border-color: rgba(232, 196, 120, 0.95);
        filter: saturate(1.05);
        transform: translateY(1px);
    }
    .stButton > button:active {
        box-shadow: 2px 2px 0 rgba(239, 210, 150, 0.35);
        transform: translateY(2px);
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        border-color: rgba(139, 99, 86, 0.16) !important;
        background-color: rgba(255, 255, 255, 0.85) !important;
    }
    [data-testid="stSpinner"] svg { opacity: 0.55 !important; }
    [data-testid="stExpander"] details {
        border-radius: var(--radius-xl);
        border: 2px dashed var(--line-soft);
        background: rgba(255, 253, 250, 0.75);
        box-shadow: 6px 6px 0 rgba(237, 220, 207, 0.35);
    }
    div[data-testid="stAlert"] {
        border-radius: var(--radius-xl);
        border: 2px dashed rgba(180, 150, 120, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 標題與更新按鈕 ---
with st.container(border=True):
    col_t, col_b = st.columns([4, 1])
    with col_t:
        st.title("✈️ 出國試算小幫手")
        st.caption("晃晃悠悠算一下⋯刷卡和領現都變得更清楚，旅途中少一點緊張感。")
    with col_b:
        if st.button("⭐ 更新匯率", use_container_width=True):
            with st.spinner("等等我喔⋯⋯"):
                if get_rates.fetch_all_rates():
                    st.toast("好囉～匯率更新完成！")
                    st.rerun()

# --- 讀取資料與防呆 ---
if os.path.exists('rates.json'):
    try:
        with open('rates.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        rates = data.get('rates', {})
        rates["TWD"] = 1.0
        last_update = data.get('last_updated', '未知')
    except:
        rates = {}
        last_update = '讀取錯誤'
else:
    rates = {}
    last_update = '尚未更新'

if rates:
    currencies = sorted(list(rates.keys()))
    st.caption(f"匯率基準最後更新：{last_update}")
    tab_card, tab_atm = st.tabs(["💳 在海外刷卡 · 吃吃買買", "🏧 ATM 乖乖領現"])

    # --- 分頁 1：海外刷卡 ---
    with tab_card:
        with st.container(border=True):
            st.subheader("刷卡成本設定")
            c_fee, c_adj = st.columns(2)
            with c_fee:
                card_markup = st.number_input("銀行手續費 (%)", value=1.5, step=0.1, key="c_markup")
            with c_adj:
                card_adj_val = st.number_input("匯率微調 (%)", value=0.0, step=0.05, key="c_adj")

        with st.container(border=True):
            st.subheader("開始算算看 ✨")
            c1, c2 = st.columns(2)
            with c1:
                buy_curr = st.selectbox("商品標價幣別", currencies, index=currencies.index("JPY") if "JPY" in currencies else 0, key="bc")
            with c2:
                pay_curr = st.selectbox("結帳扣款幣別", currencies, index=currencies.index("TWD") if "TWD" in currencies else 0, key="pc")

            rate_buy = float(rates.get(buy_curr, 1))
            rate_pay = float(rates.get(pay_curr, 1))
            exchange_rate = rate_buy / rate_pay
            final_card_rate = exchange_rate * (1 + (card_markup + card_adj_val) / 100)

            in_col, out_col = st.columns(2)
            with in_col:
                amount_buy = st.number_input(f"標價金額 ({buy_curr})", min_value=0.0, value=1000.0)
            with out_col:
                total_pay = amount_buy * final_card_rate
                st.metric("預計帳單金額", f"{total_pay:,.2f} {pay_curr}")

    # --- 分頁 2：ATM 取款 ---
    with tab_atm:
        with st.container(border=True):
            st.subheader("取款成本設定")
            a_fee_pct, a_adj = st.columns(2)
            with a_fee_pct:
                atm_pct = st.number_input("百分比手續費 (%)", value=1.5, step=0.1, key="a_markup")
            with a_adj:
                atm_adj_val = st.number_input("現鈔賣出價調整 (%)", value=1.0, step=0.1, key="a_adj")

            atm_fix = st.number_input("固定手續費（直接加在扣款總額）", value=0.0, step=1.0)

        with st.container(border=True):
            st.subheader("開始算算看 ✨")
            a1, a2 = st.columns(2)
            with a1:
                get_curr = st.selectbox("領出來的幣別", currencies, index=currencies.index("JPY") if "JPY" in currencies else 0, key="gc")
            with a2:
                acc_curr = st.selectbox("帳戶扣款幣別", currencies, index=currencies.index("USD") if "USD" in currencies else 0, key="ac")

            rate_get = float(rates.get(get_curr, 1))
            rate_acc = float(rates.get(acc_curr, 1))
            atm_base_rate = (rate_get / rate_acc) * (1 + atm_adj_val / 100)

            ain_col, aout_col = st.columns(2)
            with ain_col:
                amount_get = st.number_input(f"我要領多少 ({get_curr})", min_value=0.0, value=10000.0)
            with aout_col:
                base_acc_amount = amount_get * atm_base_rate
                total_acc_deduct = (base_acc_amount * (1 + atm_pct / 100)) + atm_fix
                st.metric("帳戶扣款總計", f"{total_acc_deduct:,.2f} {acc_curr}")

    # --- 網頁底部備註說明 ---
    st.write("---")
    with st.expander("📖 看不懂欄位？點我打開小抄 ♪"):
        st.markdown("""
        ### 💳 在海外刷卡 · 吃吃買買
        * **銀行手續費 (%)**：國際信用卡組織與銀行收取的費用，台灣一般卡多為 **1.5%**。
        * **匯率微調 (%)**：API 為市場中間價。組織（VISA/Master）匯率通常略貴，建議可填 **0.1%~0.2%** 增加準確度，VISA大約是-0.07，MASTERCARD大約是0.025。
        * **標價金額**：商店標籤上的價格。
        * **預計帳單金額**：您下個月帳單上會出現的台幣金額。

        ### 🏧 ATM 乖乖領現
        * **百分比手續費 (%)**：國際提款通常會按金額收取的比例費用，常見為 **1.5%**。
        * **現鈔賣出價調整 (%)**：反映銀行「現鈔匯率」比「網路匯率」貴的部分。領現鈔通常較貴，建議填 **1.0%~2.0%**，VISA大約是0.165，MASTERCARD大約是0.185。
        * **固定手續費**：銀行按次收取的固定費用（例如每筆 75 或 100 元），直接計入扣款總額。
        * **帳戶扣款總計**：為了領這筆現鈔，您戶頭裡總共會減少的金額。
        """)
        st.caption(f"數據更新來源：Open Exchange API | 最後更新：{last_update}")

else:
    st.warning("你好呀～請先按右上角的「⭐ 更新匯率」，我們再一起試算 ♪")