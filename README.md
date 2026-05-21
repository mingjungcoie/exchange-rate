# 出國試算小幫手

海外刷卡與 ATM 領現的匯率試算工具（純網頁版，不需 Python / Streamlit）。

## 線上網址（GitHub Pages）

佈署完成後：

**https://mingjungcoie.github.io/exchange-rate/**

## 本機預覽

在專案資料夾開一個簡單伺服器（模組化 JS 需要 HTTP，不能直接雙擊 `index.html`）：

```powershell
cd "c:\Users\ah8543\Desktop\exchange_tool"
python -m http.server 8080
```

瀏覽器開啟：http://localhost:8080

## 上傳到 GitHub（覆蓋遠端）

```powershell
cd "c:\Users\ah8543\Desktop\exchange_tool"
git add index.html css js rates.json README.md .gitignore .nojekyll
git commit -m "Migrate to static web app for GitHub Pages"
git push origin main
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
| `index.html` | 主畫面 |
| `css/style.css` | Chiikawa 風格樣式 |
| `js/rates.js` | 從 API 抓匯率（作法 A） |
| `js/app.js` | 試算邏輯與互動 |
| `rates.json` | 首次載入備援（無快取時使用） |

## 舊版 Streamlit（可刪）

若已不再使用，可刪除 `app.py`、`get_rates.py`，以及 Python 佈署設定。
