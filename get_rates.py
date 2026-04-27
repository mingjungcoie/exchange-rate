import requests
import json
from datetime import datetime

def fetch_all_rates():
    # 使用穩定且免 Key 的 API 源
    url = "https://open.er-api.com/v6/latest/TWD"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["result"] == "success":
            rates = data["rates"]
            # 整理成：1 外幣 = 多少 TWD (所以是用 1 除以該幣別對 TWD 的匯率)
            processed_rates = {
                "USD": round(1 / rates["USD"], 4),
                "JPY": round(1 / rates["JPY"], 4),
                "EUR": round(1 / rates["EUR"], 4),
                "GBP": round(1 / rates["GBP"], 4),
                "HKD": round(1 / rates["HKD"], 4),
                "KRW": round(1 / rates["KRW"], 4),
                "CNY": round(1 / rates["CNY"], 4)
            }
            
            output = {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rates": processed_rates
            }
            
            # 儲存到本地 rates.json
            with open('rates.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"抓取失敗: {e}")
        return False
    return False

# 讓你在終端機打 python get_rates.py 也能直接測試
if __name__ == "__main__":
    print("正在手動抓取匯率...")
    if fetch_all_rates():
        print("✅ 成功！已更新 rates.json")
    else:
        print("❌ 失敗，請檢查網路")