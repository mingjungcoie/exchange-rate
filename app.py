import streamlit as st
import json
import os

st.set_page_config(page_title="全球刷卡匯率計算器", page_icon="💳")

st.title("💳 全球刷卡匯率試算工具")

if os.path.exists('rates.json'):
    with open('rates.json', 'r') as f:
        data = json.load(f)
    
    st.info(f"📅 匯率最後更新時間：{data['update_time']}")
    
    # --- 介面佈局 ---
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        # 下拉選單選擇幣別
        currency_list = list(data['rates'].keys())
        selected_currency = st.selectbox("選擇外幣幣別", currency_list)
    
    with col_set2:
        # 輸入金額
        amount = st.number_input(f"輸入金額 ({selected_currency})", min_value=0.0, value=100.0, step=10.0)

    bank_fee_percent = st.slider("銀行海外手續費 (%)", 0.0, 3.0, 1.5, 0.1)

    st.divider()

    # 取得選定幣別的匯率
    v_rate = data['rates'][selected_currency]['visa']
    m_rate = data['rates'][selected_currency]['mastercard']

    # 計算
    def calc(rate, amt, fee):
        raw = rate * amt  # 不含手續費
        final = raw * (1 + fee / 100)  # 含手續費
        return raw, final

    v_raw, v_total = calc(v_rate, amount, bank_fee_percent)
    m_raw, m_total = calc(m_rate, amount, bank_fee_percent)

    # 顯示結果
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟦 VISA")
        # 修改標題與內容
        st.metric("預估扣款 (含手續費) (TWD)", f"{int(v_total):,}")
        st.write(f"預估扣款 (不含手續費): **{int(v_raw):,}** TWD")
        st.caption(f"原始匯率: {v_rate}")
        st.caption(f"手續費 ({bank_fee_percent}%): {int(v_total - v_raw)} TWD")

    with col2:
        st.subheader("🟧 Mastercard")
        # 修改標題與內容
        st.metric("預估扣款 (含手續費) (TWD)", f"{int(m_total):,}")
        st.write(f"預估扣款 (不含手續費): **{int(m_raw):,}** TWD")
        st.caption(f"原始匯率: {m_rate}")
        st.caption(f"手續費 ({bank_fee_percent}%): {int(m_total - m_raw)} TWD")

    # 貼心小提醒
    if selected_currency == "JPY":
        st.warning("💡 日幣匯率變動較大，建議以刷卡當下匯率為準。")

else:
    st.error("找不到匯率資料，請先執行 get_rates.py")
    st.divider()
st.divider()
st.header("🔄 反向試算 (國外取款/購物)")

col_rev1, col_rev2 = st.columns(2)

with col_rev1:
    target_withdraw = st.selectbox("我想要領取/支付的貨幣", ["TWD", "JPY", "USD", "KRW", "EUR", "HKD", "SGD"])
    withdraw_amount = st.number_input(f"想要拿到的金額 ({target_withdraw})", min_value=0.0, value=100.0)

with col_rev2:
    deduct_currency = st.selectbox("我的帳戶扣款幣別 (原幣)", ["USD", "EUR", "SGD"])

# --- 修正邏輯：處理 TWD 的情況 ---

# 1. 取得「領取幣別」對台幣的匯率
if target_withdraw == "TWD":
    rate_target_to_twd = 1.0
else:
    rate_target_to_twd = data['rates'][target_withdraw]['visa']

# 2. 取得「扣款幣別」對台幣的匯率
# 因為扣款幣別我們只選 USD/EUR/SGD，這些在資料庫一定有，所以不用判斷 TWD
rate_deduct_to_twd = data['rates'][deduct_currency]['visa']

# 3. 換算交叉匯率
cross_rate = rate_target_to_twd / rate_deduct_to_twd

# 4. 計算結果
raw_deduct = withdraw_amount * cross_rate
total_deduct = raw_deduct * (1 + bank_fee_percent / 100)

# --- 顯示結果 ---
st.subheader(f"預估扣款結果 ({deduct_currency})")
res1, res2 = st.columns(2)

with res1:
    st.metric(f"預估扣款 (含手續費) ({deduct_currency})", f"{total_deduct:,.2f}")
    st.write(f"匯率參考: 1 {target_withdraw} ≈ **{cross_rate:.4f}** {deduct_currency}")

with res2:
    st.write(f"不含手續費: **{raw_deduct:,.2f}** {deduct_currency}")
    st.caption(f"手續費金額: {(total_deduct - raw_deduct):,.2f} {deduct_currency}")