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

# --- 讀取資料 ---
if os.path.exists('rates.json'):
    with open('rates.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rates = data['rates']
    rates["TWD"] = 1.0
    currencies = sorted(list(rates.keys()))

    tab_card, tab_atm = st.tabs(["💳 海外刷卡 (消費)", "🏧 ATM 取款 (領現)"])

    # --- 分頁 1：海外刷卡 ---
    with tab_card:
        st.subheader("刷卡成本設定")
        c_fee, c_adj = st.columns(2)
        with c_fee:
            card_markup = st.number_input("銀行手續費 (%)", value=1.5, step=0.1, key="c_markup")
        with c_adj:
            # 這裡讓你微調組織匯率與中間價的誤差
            card_adj_val = st.number_input("匯率微調 (%)", value=0.0, step=0.05, help="如果覺得組織匯率較貴，可微調加成", key="c_adj")
        
        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            buy_curr = st.selectbox("商品標價幣別", currencies, index=currencies.index("JPY"), key="bc")
        with c2:
            pay_curr = st.selectbox("結帳扣款幣別", currencies, index=currencies.index("TWD"), key="pc")
            
        # 計算匯率：基礎匯率 * (1 + 銀行手續費 + 匯率調整)
        exchange_rate = rates[buy_curr] / rates[pay_curr]
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
        # 取款通常匯率更差，所以預設微調值給高一點點
        a_fee_pct, a_adj = st.columns(2)
        with a_fee_pct:
            atm_pct = st.number_input("百分比手續費 (%)", value=1.5, step=0.1, key="a_markup")
        with a_adj:
            # 反映「賣出價」比「中間價」貴的部分
            atm_adj_val = st.number_input("現鈔賣出價調整 (%)", value=1.0, step=0.1, help="反映銀行賣出價與中間價的價差", key="a_adj")
        
        atm_fix = st.number_input("固定手續費 (直接加在扣款總額)", value=0.0, step=1.0)
            
        st.divider()
        
        a1, a2 = st.columns(2)
        with a1:
            get_curr = st.selectbox("領出來的幣別", currencies, index=currencies.index("JPY"), key="gc")
        with a2:
            acc_curr = st.selectbox("帳戶扣款幣別", currencies, index=currencies.index("USD"), key="ac")
            
        # 這裡使用單獨的調整值來反映 ATM 更貴的匯率
        atm_base_rate = (rates[get_curr] / rates[acc_curr]) * (1 + atm_adj_val / 100)
        
        ain_col, aout_col = st.columns(2)
        with ain_col:
            amount_get = st.number_input(f"我要領多少 ({get_curr})", min_value=0.0, value=10000.0)
        with aout_col:
            base_acc_amount = amount_get * atm_base_rate
            total_acc_deduct = (base_acc_amount * (1 + atm_pct / 100)) + atm_fix
            st.metric("帳戶扣款總計", f"{total_acc_deduct:,.2f} {acc_curr}")
            
        st.info(f"💡 實際使用的取款匯率：1 {get_curr} ≈ {atm_base_rate * (1+atm_pct/100):.4f} {acc_curr}")

else:
    st.warning("請更新匯率")