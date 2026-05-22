const RATES_API_URL = "https://open.er-api.com/v6/latest/TWD";
const STORAGE_KEY = "exchange_rate_cache";
export const CURRENCY_CODES = ["USD", "JPY", "EUR", "GBP", "HKD", "SGD", "KRW", "CNY"];
export const SUPPORTED_CURRENCIES = [...CURRENCY_CODES, "TWD"];

export function formatDateTime(date = new Date()) {
  const pad = (n) => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

export function processApiRates(apiRates) {
  const processed = {};
  for (const code of CURRENCY_CODES) {
    if (apiRates[code]) {
      processed[code] = Math.round((1 / apiRates[code]) * 10000) / 10000;
    }
  }
  processed.TWD = 1.0;
  return processed;
}

export function buildPayload(rates) {
  return {
    last_updated: formatDateTime(),
    rates,
  };
}

export async function fetchRatesFromApi() {
  const response = await fetch(RATES_API_URL);
  if (!response.ok) {
    throw new Error(`API 回應異常 (${response.status})`);
  }
  const data = await response.json();
  if (data.result !== "success") {
    throw new Error("API 回傳失敗");
  }
  const rates = processApiRates(data.rates);
  return buildPayload(rates);
}

export async function fetchRatesFromFile() {
  const response = await fetch("rates.json");
  if (!response.ok) {
    throw new Error("無法讀取 rates.json");
  }
  const data = await response.json();
  const rates = { ...data.rates, TWD: 1.0 };
  return {
    last_updated: data.last_updated || "未知",
    rates,
  };
}

export function loadCachedRates() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const data = JSON.parse(raw);
    if (!data?.rates || Object.keys(data.rates).length === 0) return null;
    data.rates.TWD = 1.0;
    return data;
  } catch {
    return null;
  }
}

export function saveCachedRates(payload) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export function sortedCurrencies() {
  return [...SUPPORTED_CURRENCIES].sort();
}
