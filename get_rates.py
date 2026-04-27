import requests
import json
from datetime import datetime

def fetch_all_rates():
    print("正在獲取多國貨幣匯率數據...")
    # 定義你需要的幣別清單
    target_currencies = ["USD", "EUR", "GBP", "SGD", "JPY", "KRW", "HKD"]
    
    try:
        # 獲取最新匯率 (以 TWD 為基準，這樣直接拿到的就是 1外幣=多少台幣)
        # 註：這裡改用 TWD 為 base 會更直覺
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        usd_to_twd = data['rates']['TWD']
        
        rates_dict = {}
        for cur in target_currencies:
            # 換算出各幣別對台幣的匯率 (透過 USD 中轉計算)
            # 公式：1 外幣 = (1/該幣對USD匯率) * USD對TWD匯率
            rate_to_usd = data['rates'][cur]
            twd_rate = usd_to_twd / rate_to_usd
            
            rates_dict[cur] = {
                "visa": round(twd_rate, 4),
                "mastercard": round(twd_rate * 1.001, 4) # 模擬 Mastercard 稍微高一點點的匯率
            }
        
        result = {
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "rates": rates_dict
        }
        
        with open('rates.json', 'w') as f:
            json.dump(result, f)
            
        print("成功更新所有幣別匯率！")
        return True
    except Exception as e:
        print(f"發生錯誤: {e}")
        return False

if __name__ == "__main__":
    fetch_all_rates()