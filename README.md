# 出國試算小幫手

海外刷卡與 ATM 領現的匯率試算工具（純網頁版，不需 Python / Streamlit）。

- 平時用本工具**快速估算**（中間價 API + 可調手續費／匯率微調）
- 要對帳單前，用頁面下方的 **VISA / Mastercard 官方試算**連結精算求證

## 線上網址（GitHub Pages）

**https://mingjungcoie.github.io/exchange-rate/**

## 本機預覽

模組化 JS 需要 HTTP，不能直接雙擊 `index.html` 開啟。

```powershell
cd "c:\Users\ah8543\Desktop\Cursor工具\出國消費換算小幫手"
python -m http.server 8080
```

瀏覽器開啟：http://localhost:8080

## 功能摘要

| 功能 | 說明 |
|------|------|
| 支援幣別 | USD、JPY、EUR、GBP、HKD、**SGD**、KRW、CNY、TWD（進頁面即顯示於選單） |
| 更新匯率 | 從 Open Exchange API 抓最新中間價，並寫入瀏覽器快取 |
| 重新整理 | 強制重載整頁（給 iPhone 主畫面捷徑用，見下方） |
| 精算求證 | 連結 [Visa 台灣試算](https://www.visa.com.tw/support/consumer/travel-support/exchange-rate-calculator.html)、[Mastercard 試算](https://www.mastercard.com/us/en/personal/get-support/currency-exchange-rate-converter.html) |
| 刷卡 / ATM | 分頁試算，手機上兩個分頁同一列顯示 |

## iPhone「加入主畫面」更新說明

主畫面捷徑會**強快取**網頁，關掉再開有時仍是舊版，這是 iOS 正常現象，不是當機。

| 按鈕 | 用途 |
|------|------|
| ⭐ 更新匯率 | 只更新匯率數字 |
| 🔄 重新整理 | 網站改版、版面或功能要變新時使用 |

若按重新整理仍像舊版：刪除主畫面圖示 → 用 Safari 開官網 → 再「加入主畫面」。

### 佈署新版時建議（提高主畫面載入成功率）

1. 上傳變更的檔案到 GitHub  
2. 把 `index.html` 裡 `css/style.css?v=3`、`js/app.js?v=3` 的 **`3` 改成 `4`**（下次再改 `5`…）  
3. 推送後等 1～2 分鐘，在主畫面 App 按 **🔄 重新整理**

沒改版本號**不會當機**，只是主畫面比較容易繼續顯示舊介面。

## 上傳到 GitHub

```powershell
cd "c:\Users\ah8543\Desktop\Cursor工具\出國消費換算小幫手"
git add index.html css/style.css js/app.js js/rates.js rates.json README.md .gitignore
git commit -m "說明你的變更摘要"
git push origin main
```

有使用 `.nojekyll` 時一併加入：

```powershell
git add .nojekyll
```

## 開啟 GitHub Pages（只需做一次）

1. 打開 https://github.com/mingjungcoie/exchange-rate  
2. **Settings** → **Pages**  
3. **Source** 選 **Deploy from a branch**  
4. Branch 選 **main**，資料夾選 **/ (root)**  
5. 儲存後等 1～2 分鐘，網址就會生效  

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `index.html` | 主畫面、分頁、官方連結區、`?v=` 版本參數 |
| `css/style.css` | 版面樣式（含手機分頁、結果區淡藍色） |
| `js/rates.js` | 匯率 API、快取、支援幣別清單 |
| `js/app.js` | 試算邏輯、更新匯率、重新整理 |
| `rates.json` | 首次載入備援；快取缺幣別時補齊 |
| `README.md` | 本說明 |

## 舊版 Streamlit（可刪）

若已不再使用，可刪除 `app.py`、`get_rates.py`，以及 Python 佈署設定。
