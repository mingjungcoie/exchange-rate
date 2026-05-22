import {
  fetchRatesFromApi,
  fetchRatesFromFile,
  loadCachedRates,
  saveCachedRates,
  sortedCurrencies,
} from "./rates.js";

const DEFAULT_SELECTS = {
  cardBuy: "JPY",
  cardPay: "TWD",
  atmGet: "JPY",
  atmAcc: "USD",
};

const state = {
  rates: null,
  lastUpdate: "",
};

const els = {
  appMain: document.getElementById("app-main"),
  emptyState: document.getElementById("empty-state"),
  lastUpdate: document.getElementById("last-update"),
  btnUpdate: document.getElementById("btn-update"),
  btnReload: document.getElementById("btn-reload"),
  toast: document.getElementById("toast"),
  helpFoot: document.getElementById("help-foot"),
  tabs: document.querySelectorAll(".tab"),
  panels: document.querySelectorAll(".panel"),
  cardBuy: document.getElementById("card-buy"),
  cardPay: document.getElementById("card-pay"),
  cardAmountLabel: document.getElementById("card-amount-label"),
  cardTotal: document.getElementById("card-total"),
  atmGet: document.getElementById("atm-get"),
  atmAcc: document.getElementById("atm-acc"),
  atmAmountLabel: document.getElementById("atm-amount-label"),
  atmTotal: document.getElementById("atm-total"),
};

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.add("show");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => els.toast.classList.remove("show"), 2600);
}

function formatMoney(value, currency) {
  const n = Number(value);
  if (!Number.isFinite(n)) return `— ${currency}`;
  return `${n.toLocaleString("zh-TW", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currency}`;
}

function fillSelect(select, currencies, preferred) {
  select.innerHTML = "";
  for (const code of currencies) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = code;
    select.appendChild(opt);
  }
  if (preferred && currencies.includes(preferred)) {
    select.value = preferred;
  }
}

function setAppVisible(hasRates) {
  els.appMain.classList.toggle("hidden", !hasRates);
  els.emptyState.classList.toggle("hidden", hasRates);
}

function updateMeta() {
  els.lastUpdate.textContent = `匯率基準最後更新：${state.lastUpdate}`;
  if (els.helpFoot) {
    els.helpFoot.textContent = `數據更新來源：Open Exchange API | 最後更新：${state.lastUpdate}`;
  }
}

function applyRates(payload) {
  state.rates = payload.rates;
  state.lastUpdate = payload.last_updated;
  saveCachedRates(payload);
  updateMeta();

  const currencies = sortedCurrencies();
  fillSelect(els.cardBuy, currencies, DEFAULT_SELECTS.cardBuy);
  fillSelect(els.cardPay, currencies, DEFAULT_SELECTS.cardPay);
  fillSelect(els.atmGet, currencies, DEFAULT_SELECTS.atmGet);
  fillSelect(els.atmAcc, currencies, DEFAULT_SELECTS.atmAcc);

  setAppVisible(true);
  recalcAll();
}

function recalcCard() {
  if (!state.rates) return;

  const buy = els.cardBuy.value;
  const pay = els.cardPay.value;
  const markup = Number(document.getElementById("card-markup").value) || 0;
  const adj = Number(document.getElementById("card-adj").value) || 0;
  const amount = Number(document.getElementById("card-amount").value) || 0;

  const rateBuy = state.rates[buy] ?? 1;
  const ratePay = state.rates[pay] ?? 1;
  const exchangeRate = rateBuy / ratePay;
  const finalRate = exchangeRate * (1 + (markup + adj) / 100);
  const total = amount * finalRate;

  els.cardAmountLabel.textContent = `標價金額 (${buy})`;
  els.cardTotal.textContent = formatMoney(total, pay);
}

function recalcAtm() {
  if (!state.rates) return;

  const get = els.atmGet.value;
  const acc = els.atmAcc.value;
  const pct = Number(document.getElementById("atm-pct").value) || 0;
  const adj = Number(document.getElementById("atm-adj").value) || 0;
  const fix = Number(document.getElementById("atm-fix").value) || 0;
  const amount = Number(document.getElementById("atm-amount").value) || 0;

  const rateGet = state.rates[get] ?? 1;
  const rateAcc = state.rates[acc] ?? 1;
  const baseRate = (rateGet / rateAcc) * (1 + adj / 100);
  const baseAcc = amount * baseRate;
  const total = baseAcc * (1 + pct / 100) + fix;

  els.atmAmountLabel.textContent = `我要領多少 (${get})`;
  els.atmTotal.textContent = formatMoney(total, acc);
}

function recalcAll() {
  recalcCard();
  recalcAtm();
}

function initCurrencySelects() {
  const currencies = sortedCurrencies();
  fillSelect(els.cardBuy, currencies, DEFAULT_SELECTS.cardBuy);
  fillSelect(els.cardPay, currencies, DEFAULT_SELECTS.cardPay);
  fillSelect(els.atmGet, currencies, DEFAULT_SELECTS.atmGet);
  fillSelect(els.atmAcc, currencies, DEFAULT_SELECTS.atmAcc);
}

async function loadInitialRates() {
  let fallback = null;
  try {
    fallback = await fetchRatesFromFile();
  } catch {
    /* rates.json 不可用時仍保留選單 */
  }

  const cached = loadCachedRates();
  if (cached) {
    applyRates({
      last_updated: cached.last_updated,
      rates: { ...(fallback?.rates ?? {}), ...cached.rates, TWD: 1.0 },
    });
    return;
  }
  if (fallback) {
    applyRates(fallback);
    return;
  }
  setAppVisible(false);
}

async function updateRatesFromApi() {
  els.btnUpdate.disabled = true;
  const prev = els.btnUpdate.textContent;
  els.btnUpdate.textContent = "等等我喔⋯⋯";
  try {
    const payload = await fetchRatesFromApi();
    applyRates(payload);
    showToast("好囉～匯率更新完成！");
  } catch (err) {
    showToast(`更新失敗：${err.message}`);
  } finally {
    els.btnUpdate.disabled = false;
    els.btnUpdate.textContent = prev;
  }
}

function initTabs() {
  els.tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.tab;
      els.tabs.forEach((t) => t.classList.toggle("active", t === tab));
      els.panels.forEach((p) => p.classList.toggle("active", p.id === `panel-${target}`));
    });
  });
}

function bindInputs() {
  const ids = [
    "card-markup", "card-adj", "card-amount",
    "atm-pct", "atm-adj", "atm-fix", "atm-amount",
  ];
  ids.forEach((id) => {
    document.getElementById(id).addEventListener("input", recalcAll);
  });
  [els.cardBuy, els.cardPay, els.atmGet, els.atmAcc].forEach((el) => {
    el.addEventListener("change", recalcAll);
  });
}

/** 強制重新載入頁面（略過 iOS 主畫面捷徑的快取） */
function reloadPageFresh() {
  const url = new URL(window.location.href);
  url.searchParams.set("_", String(Date.now()));
  window.location.replace(url.href);
}

els.btnUpdate.addEventListener("click", updateRatesFromApi);
els.btnReload.addEventListener("click", reloadPageFresh);
initTabs();
bindInputs();
initCurrencySelects();
loadInitialRates();
