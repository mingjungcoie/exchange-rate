import streamlit as st
import json
import os
import get_rates

st.set_page_config(page_title="專業出國計算器", page_icon="✈️", layout="centered")

# --- 標題與更新按鈕 ---
col_t, col_b = st.columns([3, 1])
with col_t:
    st.title("✈️ 專業出國計算器")
with col_b:
    if st.button("🔄 更新匯率"):
        with st.spinner("更新中..."):
            if get_rates.fetch_all_rates():
                st.toast("匯率已更新！")
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
    tab_card, tab_atm = st.tabs(["💳 海外刷卡 (消費)", "🏧 ATM 取款 (領現)"])

    # --- 分頁 1：海外刷卡 ---
    with tab_card:
        st.subheader("刷卡成本設定")
        c_fee, c_adj = st.columns(2)
        with c_fee:
            card_markup = st.number_input("銀行手續費 (%)", value=1.5, step=0.1, key="c_markup")
        with c_adj:
            card_adj_val = st.number_input("匯率微調 (%)", value=0.0, step=0.05, key="c_adj")
        
        st.divider()
        
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
        st.subheader("取款成本設定")
        a_fee_pct, a_adj = st.columns(2)
        with a_fee_pct:
            atm_pct = st.number_input("百分比手續費 (%)", value=1.5, step=0.1, key="a_markup")
        with a_adj:
            atm_adj_val = st.number_input("現鈔賣出價調整 (%)", value=1.0, step=0.1, key="a_adj")
        
        atm_fix = st.number_input("固定手續費 (直接加在扣款總額)", value=0.0, step=1.0)
            
        st.divider()
        
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
    with st.expander("📖 欄位詳細說明（點擊展開）"):
        st.markdown("""
        ### 💳 海外刷卡 (消費)
        * **銀行手續費 (%)**：國際信用卡組織與銀行收取的費用，台灣一般卡多為 **1.5%**。
        * **匯率微調 (%)**：API 為市場中間價。組織（VISA/Master）匯率通常略貴，建議可填 **0.1%~0.2%** 增加準確度。
        * **標價金額**：商店標籤上的價格。
        * **預計帳單金額**：您下個月帳單上會出現的台幣金額。

        ### 🏧 ATM 取款 (領現)
        * **百分比手續費 (%)**：國際提款通常會按金額收取的比例費用，常見為 **1.5%**。
        * **現鈔賣出價調整 (%)**：反映銀行「現鈔匯率」比「網路匯率」貴的部分。領現鈔通常較貴，建議填 **1.0%~2.0%**，VISA大約是0.165，MASTERCARD大約是0.185。
        * **固定手續費**：銀行按次收取的固定費用（例如每筆 75 或 100 元），直接計入扣款總額。
        * **帳戶扣款總計**：為了領這筆現鈔，您戶頭裡總共會減少的金額。
        """)
        st.caption(f"數據更新來源：Open Exchange API | 最後更新：{last_update}")

else:
    st.warning("歡迎使用！請先點擊右上角「更新匯率」按鈕。")