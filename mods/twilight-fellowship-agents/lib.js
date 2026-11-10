// 旅人卡片 MOD 的純函式：不碰 herdr / gpui-kit，可以被 node 直接載入測試。
// 這裡只做資料處理；讀快取、畫畫面都在 main.js。

export const JOBS = [
  // the fellowship
  "archer",
  "dwarf",
  "halfling",
  "healer",
  "loremaster",
  "ranger",
  "smith",
  "wizard",
  // the enemy
  "berserker",
  "darklord",
  "goblin",
  "orc",
  "sorcerer",
  "spy",
  "troll",
  "wraith",
];

// 快取超過這麼久就標「舊」：statusLine 每次回應都會重寫，5 分鐘沒動就不算即時。
export const STALE_SECONDS = 300;

const JOB_SET = new Set(JOBS);
const SESSIONS_DIR = "data/traveler/sessions";
const PORTRAITS_DIR = "mods/twilight-fellowship-agents/party-art";
const SPRITES_DIR = "mods/twilight-fellowship-agents/party-sprites";
// 有全身動圖的職業（tools/sprites/build.mjs 產生）；不在清單的職業卡片用肖像。
const SPRITE_JOBS = new Set(JOBS);

// 本機終端機代號：跟 scripts/traveler-statusline.mjs 寫檔名的規則一致，不收路徑字元。
const LOCAL_ID = /^[A-Za-z0-9][A-Za-z0-9_-]*$/;

// 0–100 的有限數才算百分比，其餘（含 null、字串、超出範圍）都當沒有資料。
function pct(value) {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 && value <= 100
    ? value
    : null;
}

// 字串欄位：去掉控制字元與文字方向控制字元、收斂空白、去頭尾，最多 max 字；
// 跟 scripts/traveler-statusline.mjs 同一套規則，讀的時候再擋一次。
function cleanText(value, max) {
  if (typeof value !== "string") return null;
  const s = value.replace(/[\u0000-\u001f\u007f-\u009f\u2028\u2029\u202a-\u202e\u2066-\u2069]/g, "").replace(/\s+/g, " ").trim();
  return s === "" ? null : [...s].slice(0, max).join("");
}

// session 名稱（Claude Code 的 /rename）最多 80 字。
const NAME_MAX = 80;
export function cleanName(value) {
  return cleanText(value, NAME_MAX);
}

// 模型與 effort 名稱比 session 名稱短：卡片上一行放得下就好。
const MODEL_MAX = 40;
function cleanModel(value) {
  return cleanText(value, MODEL_MAX);
}

// One character per agent, kept in shared state so the cards and the tabs agree.
// An agent keeps its character while it lives; live agents don't share one
// until all eight are taken.
export const PARTY_KEY = "twilight-fellowship.party";
const PARTY_MAX = 32;

export function assignParty(addresses, party) {
  const out = {};
  for (const [k, v] of Object.entries(party ?? {})) if (JOB_SET.has(v)) out[k] = v;
  const live = (addresses ?? []).filter((a) => typeof a === "string");
  const used = new Set(live.filter((a) => out[a]).map((a) => out[a]));
  let changed = Object.keys(out).length !== Object.keys(party ?? {}).length;
  for (const address of live) {
    if (out[address]) continue;
    if (used.size >= JOBS.length) used.clear();
    const start = [...address].reduce((n, c) => n + c.codePointAt(0), 0);
    const job = Array.from({ length: JOBS.length }, (_, i) => JOBS[(start + i) % JOBS.length]).find((j) => !used.has(j));
    out[address] = job;
    used.add(job);
    changed = true;
  }
  // Forget agents that are gone once the record grows.
  if (Object.keys(out).length > PARTY_MAX) {
    const keep = new Set(live);
    for (const k of Object.keys(out)) if (!keep.has(k)) delete out[k];
    changed = true;
  }
  return { party: out, changed };
}

// image() 只讀 Herdr 家目錄的相對路徑；只給八個已知職業，避免組出跳脫路徑。
export function portraitPath(job) {
  return typeof job === "string" && JOB_SET.has(job) ? `${PORTRAITS_DIR}/${job}.png` : null;
}

// 全身動圖：working 揮劍、blocked 舉手、其餘狀態（done、idle、沒有狀態）都是休息。
export function spritePath(job, status) {
  if (typeof job !== "string" || !SPRITE_JOBS.has(job)) return null;
  const state = status === "working" || status === "blocked" ? status : "rest";
  return `${SPRITES_DIR}/${job}-${state}.gif`;
}

// 程式標籤：看 agent 自己回報的 app（OSC 7501），只認這三種；builder 沒有 HP/SP 的來源。
const APPS = new Map([
  ["claude-code", { text: "Claude", builder: false }],
  ["codex", { text: "Codex", builder: true }],
  ["opencode", { text: "OpenCode", builder: true }],
]);
export function appLabel(app) {
  const found = typeof app === "string" ? APPS.get(app) : undefined;
  return found ? { ...found } : null;
}

// 快取只給本機終端機；遠端代號（vps/t7）沒有本機檔案。
export function cachePath(appHomeDir, address) {
  if (typeof appHomeDir !== "string") return null;
  const base = appHomeDir.replace(/\/+$/, "");
  if (base === "") return null;
  if (typeof address !== "string" || !LOCAL_ID.test(address)) return null;
  return `${base}/${SESSIONS_DIR}/${address}.json`;
}

// 遠端 agent（imac/t1）：那台自己的 statusLine 寫在它的預設 Herdr 資料夾，
// readTextFile 帶 on 時相對路徑從那台的家目錄算起（2026-11-03 用 hc file read --on 實測）。
const MACHINE = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
export function remoteCachePath(address) {
  if (typeof address !== "string") return null;
  const parts = address.split("/");
  if (parts.length !== 2 || !MACHINE.test(parts[0]) || !LOCAL_ID.test(parts[1])) return null;
  return { on: parts[0], path: `.config/herdr-app/${SESSIONS_DIR}/${parts[1]}.json` };
}

// 快取內容：{ updatedAt, contextRemainingPct, fiveHourRemainingPct, sessionName, model, effort }。
// 單一欄位壞掉只讓該欄位變 null；updatedAt 不合法就整份當作讀不到。
export function parseCache(text) {
  if (typeof text !== "string" || text.trim() === "") return null;
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    return null;
  }
  if (data === null || typeof data !== "object" || Array.isArray(data)) return null;
  const updatedAt = data.updatedAt;
  if (typeof updatedAt !== "number" || !Number.isFinite(updatedAt) || updatedAt < 0) return null;
  return {
    updatedAt,
    hp: pct(data.contextRemainingPct),
    sp: pct(data.fiveHourRemainingPct),
    name: cleanName(data.sessionName),
    model: cleanModel(data.model),
    effort: cleanModel(data.effort),
  };
}

// 卡片上的「模型 · effort」一行：沒有模型就不顯示（effort 單獨出現沒有意義）。
export function modelText(model, effort) {
  const m = cleanModel(model);
  if (m === null) return null;
  const e = cleanModel(effort);
  return e === null ? m : `${m} · ${e}`;
}

// 一條 HP/SP 條要畫的東西：沒有數字（或沒有時間戳）就顯示「—」且不填色；
// 過舊只加標記，數字照實顯示，不改寫成別的值。
export function gauge(value, updatedAt, now) {
  const p = pct(value);
  const at =
    typeof updatedAt === "number" && Number.isFinite(updatedAt) && updatedAt >= 0
      ? updatedAt
      : null;
  if (p === null || at === null) return { text: "—", pct: null, stale: false };
  const stale = typeof now === "number" && Number.isFinite(now) && now - at > STALE_SECONDS;
  return { text: `${p}%`, pct: p, stale };
}
