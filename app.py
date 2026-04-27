import streamlit as st
import json
import os
from datetime import datetime
import get_rates  # 確保你的 get_rates.py 在同一個資料夾

# 設定網頁標題
st.set_page_config(page_title="我的專屬匯率工具", layout="centered")

st.title("💱 匯率轉換工具")

# --- 手動更新按鈕區塊 ---
# 建立兩欄，讓按鈕放在右邊或置中
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 更新匯率"):
        with st.spinner("更新中..."):
            success = get_rates.fetch_all_rates() # 呼叫你原本抓 API 的函式
            if success:
                st.toast("匯率已更新至最新狀態！", icon="✅")
                st.rerun()
            else:
                st.error("更新失敗")

# --- 讀取資料 ---
def load_rates():
    if os.path.exists('rates.json'):
        with open('rates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

data = load_rates()

if data:
    # 顯示最後更新時間
    st.caption(f"最後更新時間: {data.get('last_updated', '未知')}")
    
    # 這裡放你原本的計算邏輯 (Selectbox, Number Input 等)
    # ... (保留你原本寫好的正向/反向試算程式碼) ...
    
else:
    st.warning("目前沒有匯率資料，請點擊上方更新按鈕。")