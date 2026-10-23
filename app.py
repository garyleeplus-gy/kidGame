import sys
import os
import subprocess

# ==============================================================================
# 自動環境檢查與啟動器：
# 支援直接執行 `python app.py` (自動偵測/安裝 streamlit 並啟動網頁伺服器)
# 亦支援在 GitHub + Streamlit Community Cloud 雲端環境直接部署執行
# ==============================================================================
def ensure_streamlit_and_launch():
    try:
        import streamlit as st
    except ImportError:
        print("🔧 正在自動安裝 streamlit 套件，請稍候...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        import streamlit as st

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            print("🚀 正在啟動《星際邏輯學院》Web 伺服器...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
            sys.exit(0)
    except Exception:
        pass

ensure_streamlit_and_launch()

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="星際邏輯學院 | 105關卡運算思維遊戲",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 極簡化 Streamlit 邊距，讓手機、平板與電腦畫面最大化
st.markdown("""
<style>
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    iframe {border: none !important;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌌 星際邏輯學院 2.0")
    st.markdown("""
    **五大運算思維訓練 × 各 20 關 + 自製沙盒**
    - **1️⃣ 星際編碼號**：序列、迴圈、條件與蟲洞
    - **2️⃣ 光子邏輯閘**：AND / OR / XOR / NAND / NOR
    - **3️⃣ 能量排序室**：選擇、泡泡、奇偶與山峰排序
    - **4️⃣ 星際河內塔**：Stack 堆疊與遞迴拆解
    - **5️⃣ 像素解碼器**：二進位權重與 2D 矩陣推理
    ---
    ### 💡 操作與備份指南
    - **畫面縮放**：點擊頂部 `➖` / `➕` 按鈕，或在手機上直接雙指縮放。
    - **存檔與 Excel 報表**：點擊右上角 **「💾 存檔管理」** 可下載 `.json` 存檔、複製跨裝置通行碼，或一鍵複製成績表貼入 Excel。
    """)

# ==============================================================================
# 內嵌完整響應式 HTML5 + Canvas + WebAudio 遊戲引擎 (105 關卡完整修正版)
# ==============================================================================
GAME_HTML = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style>
    :root {
        --bg-dark: #0b0d17;
        --bg-panel: rgba(20, 24, 38, 0.95);
        --bg-card: #1f2437;
        --accent-blue: #4fc3f7;
        --accent-cyan: #26c6da;
        --accent-green: #69f0ae;
        --accent-gold: #ffd54f;
        --accent-pink: #ff80ab;
        --accent-purple: #b388ff;
        --text-main: #eceff4;
        --text-sub: #b0bec5;
    }
    * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }
    body {
        margin: 0; padding: 6px;
        background: radial-gradient(circle at 30% 15%, #1b2238 0%, #090b12 100%);
        color: var(--text-main);
        font-family: "Microsoft JhengHei", "PingFang TC", "Segoe UI", sans-serif;
        overflow-x: hidden;
    }
    #appWrapper {
        width: 100%;
        max-width: 1280px;
        margin: 0 auto;
        transition: zoom 0.15s ease;
    }

    /* 頂部導覽列 */
    .top-header {
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        background: var(--bg-panel); border: 1px solid rgba(79,195,247,0.3);
        border-radius: 14px; padding: 8px 12px; margin-bottom: 8px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.45); gap: 8px;
    }
    .brand-title {
        font-size: 1.2rem; font-weight: 900;
        background: linear-gradient(90deg, #ffd54f, #4fc3f7, #ff80ab);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        display: flex; align-items: center; gap: 6px; white-space: nowrap;
    }
    .nav-tabs { display: flex; flex-wrap: wrap; gap: 5px; }
    .nav-btn {
        background: var(--bg-card); color: var(--text-main);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 9px;
        padding: 6px 10px; font-size: 0.85rem; font-weight: bold;
        cursor: pointer; transition: all 0.18s;
    }
    .nav-btn:hover { border-color: var(--accent-cyan); transform: translateY(-1px); }
    .nav-btn.active {
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #111; border-color: #fff; box-shadow: 0 0 12px rgba(255,213,79,0.5);
    }
    .header-controls { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
    .star-badge {
        background: rgba(105,240,174,0.15); border: 1px solid var(--accent-green);
        color: var(--accent-green); padding: 4px 10px; border-radius: 18px;
        font-weight: bold; font-size: 0.86rem; white-space: nowrap;
    }
    .tool-btn {
        background: #2c354d; color: #fff; border: 1px solid var(--accent-blue);
        padding: 4px 9px; border-radius: 8px; cursor: pointer; font-size: 0.82rem; font-weight: bold;
    }
    .tool-btn:hover { background: var(--accent-blue); color: #111; }

    /* 20+1 關卡選擇捲軸列 */
    .level-bar {
        display: flex; align-items: center; gap: 5px; overflow-x: auto;
        background: var(--bg-panel); padding: 7px 10px; border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08); margin-bottom: 8px;
        scrollbar-width: thin; -webkit-overflow-scrolling: touch;
    }
    .lvl-btn {
        flex: 0 0 auto; background: var(--bg-card); color: var(--text-sub);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
        padding: 5px 9px; font-size: 0.8rem; font-weight: bold; cursor: pointer;
    }
    .lvl-btn.passed { border-color: rgba(105,240,174,0.5); color: #69f0ae; }
    .lvl-btn.active {
        background: var(--accent-blue); color: #000; border-color: #fff;
        box-shadow: 0 0 10px rgba(79,195,247,0.6);
    }
    .lvl-btn.custom {
        background: linear-gradient(135deg, #ff80ab, #f50057); color: #fff;
    }
    .lvl-btn.custom.active { border: 2px solid #ffd54f; box-shadow: 0 0 12px #ff80ab; }

    /* 主雙欄響應式網格 */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 350px;
        gap: 10px;
    }
    @media (max-width: 920px) {
        .main-grid { grid-template-columns: 1fr; }
    }

    .stage-card, .code-card {
        background: var(--bg-panel); border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1); padding: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.45);
    }
    .lvl-header-title { font-size: 1.15rem; font-weight: bold; color: var(--accent-gold); margin-bottom: 4px; }
    .lvl-header-desc { font-size: 0.9rem; color: var(--text-sub); margin-bottom: 8px; line-height: 1.4; }

    /* 全息提示橫幅 (取代原生 alert) */
    .toast-bar {
        display: none; margin-bottom: 8px; padding: 8px 12px; border-radius: 9px;
        font-weight: bold; font-size: 0.9rem; align-items: center; justify-content: space-between;
        animation: fadeIn 0.2s ease;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

    .game-flex {
        display: flex; flex-wrap: wrap; gap: 12px; align-items: flex-start; justify-content: center;
    }
    canvas {
        background: #080b12; border-radius: 14px;
        border: 2px solid rgba(79,195,247,0.35);
        box-shadow: inset 0 0 25px rgba(0,0,0,0.85), 0 4px 15px rgba(0,0,0,0.5);
        max-width: 100%; height: auto; touch-action: manipulation; display: block; margin: 0 auto;
    }
    .control-box {
        flex: 1 1 250px; background: rgba(12,15,24,0.8);
        border-radius: 12px; padding: 10px; border: 1px solid rgba(255,255,255,0.08);
    }
    .block-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px; }
    .cmd-btn {
        border: none; border-radius: 8px; padding: 8px 8px;
        font-size: 0.88rem; font-weight: bold; cursor: pointer;
        color: #111; transition: transform 0.1s, filter 0.15s;
        display: inline-flex; align-items: center; justify-content: center; gap: 4px;
    }
    .cmd-btn:active { transform: scale(0.95); }
    .cmd-btn:hover { filter: brightness(1.12); }

    .cmd-list {
        background: #07090e; border-radius: 8px; padding: 8px;
        height: 185px; overflow-y: auto; font-family: Consolas, monospace;
        font-size: 0.88rem; border: 1px solid #283046; margin-top: 5px;
    }
    .cmd-item { padding: 3px 6px; border-radius: 4px; margin-bottom: 2px; }
    .cmd-item.running { background: rgba(255, 128, 171, 0.35); border-left: 3px solid var(--accent-pink); color: #fff; }

    .status-banner {
        margin-top: 8px; padding: 7px 11px; border-radius: 8px;
        background: rgba(105,240,174,0.12); border-left: 4px solid var(--accent-green);
        font-weight: bold; font-size: 0.88rem; color: var(--accent-green); text-align: left;
    }

    /* 右側 Python 預覽區 */
    .code-box {
        background: #07090e; color: #69f0ae; font-family: Consolas, monospace;
        font-size: 0.86rem; padding: 10px; border-radius: 10px;
        height: 290px; overflow-y: auto; white-space: pre-wrap;
        border: 1px solid #283046; line-height: 1.42;
    }
    .concept-box {
        margin-top: 8px; background: rgba(255,213,79,0.1);
        border: 1px solid rgba(255,213,79,0.35); border-radius: 10px;
        padding: 9px; font-size: 0.84rem; color: var(--accent-gold); line-height: 1.42;
    }

    /* 彈跳視窗 Modal */
    .modal-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.78); z-index: 999; align-items: center; justify-content: center;
        padding: 14px;
    }
    .modal-box {
        background: #171b2b; border: 2px solid var(--accent-blue);
        border-radius: 16px; max-width: 540px; width: 100%; padding: 18px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.85); text-align: center;
    }
    .brush-bar {
        display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px;
        background: rgba(255,255,255,0.05); padding: 7px; border-radius: 10px; justify-content: center;
    }
    .brush-btn {
        background: #283046; color: #fff; border: 1px solid transparent;
        padding: 5px 8px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; font-weight: bold;
    }
    .brush-btn.active { border-color: var(--accent-gold); background: #3e4a6d; color: var(--accent-gold); }
</style>
</head>
<body>

<div id="appWrapper">
    <!-- 頂部導覽與控制列 -->
    <div class="top-header">
        <div class="brand-title">🚀 星際邏輯學院 <span style="font-size:0.78rem; color:#4fc3f7;">105關旗艦版</span></div>
        <div class="nav-tabs" id="gameTabs">
            <button class="nav-btn active" onclick="switchGame(0)">1️⃣ 星際編碼號</button>
            <button class="nav-btn" onclick="switchGame(1)">2️⃣ 光子邏輯閘</button>
            <button class="nav-btn" onclick="switchGame(2)">3️⃣ 能量排序室</button>
            <button class="nav-btn" onclick="switchGame(3)">4️⃣ 星際河內塔</button>
            <button class="nav-btn" onclick="switchGame(4)">5️⃣ 像素解碼器</button>
        </div>
        <div class="header-controls">
            <button class="tool-btn" onclick="stepZoom(-10)" title="縮小畫面">➖</button>
            <span id="zoomVal" style="font-size:0.8rem; color:#b0bec5; min-width:38px; text-align:center;">100%</span>
            <button class="tool-btn" onclick="stepZoom(10)" title="放大畫面">➕</button>
            <button class="tool-btn" id="soundBtn" onclick="toggleSound()">🔊 音效</button>
            <div class="star-badge" id="totalStarsBadge">🏆 0 / 300 ⭐</div>
            <button class="tool-btn" style="border-color:#69f0ae; color:#69f0ae;" onclick="openSaveModal()">💾 存檔/成績單</button>
        </div>
    </div>

    <!-- 20 關 + 自製關卡選擇列 -->
    <div class="level-bar" id="levelBar"></div>

    <!-- 主工作區 -->
    <div class="main-grid" id="mainGrid">
        <div class="stage-card">
            <div class="lvl-header-title" id="lvlTitle">載入中...</div>
            <div class="lvl-header-desc" id="lvlDesc"></div>
            <div class="toast-bar" id="toastBar"></div>
            <div id="stageContent"></div>
        </div>
        <div class="code-card">
            <div style="font-size:1rem; font-weight:bold; color:#69f0ae; margin-bottom:5px;">
                🐍 即時 Python 演算法透視窗
            </div>
            <div style="font-size:0.8rem; color:#b0bec5; margin-bottom:6px;">
                你在遊戲中的每一步邏輯，對應的真正 Python 程式碼：
            </div>
            <div class="code-box" id="pythonPreview"></div>
            <div class="concept-box" id="conceptBox"></div>
        </div>
    </div>
</div>

<!-- 過關慶祝與存檔管理彈跳視窗 -->
<div class="modal-overlay" id="modalOverlay">
    <div class="modal-box" id="modalContent"></div>
</div>

<!-- 慶祝紙花特效 Canvas -->
<canvas id="confettiCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:998; display:none; border:none; background:transparent; box-shadow:none;"></canvas>

<script>
// ============================================================================
// 跨瀏覽器 Canvas 圓角相容函式 + Web Audio 合成音效引擎
// ============================================================================
function drawRoundRect(ctx, x, y, w, h, r) {
    const radius = typeof r === "number" ? r : 8;
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + w - radius, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + radius);
    ctx.lineTo(x + w, y + h - radius);
    ctx.quadraticCurveTo(x + w, y + h, x + w - radius, y + h);
    ctx.lineTo(x + radius, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

let soundEnabled = true;
let audioCtx = null;

function playTone(freq, type, duration, delay = 0) {
    if (!soundEnabled) return;
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === "suspended") audioCtx.resume();
        setTimeout(() => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type || "sine";
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }, delay);
    } catch (e) {}
}

function sfxClick() { playTone(520, "triangle", 0.07); }
function sfxMove()  { playTone(440, "sine", 0.09); }
function sfxLaser() { playTone(780, "sawtooth", 0.14); }
function sfxError() { playTone(200, "sawtooth", 0.22); playTone(150, "sawtooth", 0.25, 120); }
function sfxWin()   {
    playTone(523.25, "triangle", 0.15, 0);
    playTone(659.25, "triangle", 0.15, 120);
    playTone(783.99, "triangle", 0.15, 240);
    playTone(1046.5, "triangle", 0.35, 360);
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    document.getElementById("soundBtn").innerText = soundEnabled ? "🔊 音效" : "🔇 靜音";
}

// 遊戲內訊息通知 (取代原生 alert)
let toastTimer = null;
function showToast(msg, type = "warn") {
    const el = document.getElementById("toastBar");
    if (!el) return;
    const colors = {
        warn: ["rgba(255, 183, 77, 0.2)", "#ffb74d", "#ffd54f"],
        err:  ["rgba(255, 128, 171, 0.2)", "#ff4081", "#ff80ab"],
        ok:   ["rgba(105, 240, 174, 0.2)", "#00e676", "#69f0ae"]
    }[type] || ["rgba(79,195,247,0.2)", "#4fc3f7", "#4fc3f7"];

    el.style.background = colors[0];
    el.style.borderLeft = `4px solid ${colors[1]}`;
    el.style.color = colors[2];
    el.innerHTML = `<span>${msg}</span><button onclick="this.parentElement.style.display='none'" style="background:transparent;border:none;color:#fff;cursor:pointer;font-weight:bold;">✕</button>`;
    el.style.display = "flex";
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { el.style.display = "none"; }, 4200);
}

// ============================================================================
// 全域狀態、畫面縮放與三重存檔系統 (含 Excel 成績單複製)
// ============================================================================
const STORAGE_KEY = "STAR_LOGIC_ACADEMY_SAVE_V3";
let currentZoom = 100;
let appState = {
    currentGame: 0,
    currentLevel: 0,
    stars: {},        // key: "g_l" -> 1..3
    customLevels: {}  // 儲存玩家自訂的 5 款遊戲沙盒關卡
};

function stepZoom(delta) {
    currentZoom = Math.min(135, Math.max(65, currentZoom + delta));
    document.getElementById("zoomVal").innerText = currentZoom + "%";
    const wrap = document.getElementById("appWrapper");
    wrap.style.zoom = (currentZoom / 100);
}

function encodeSaveObj(obj) {
    const jsonStr = JSON.stringify(obj);
    const bytes = new TextEncoder().encode(jsonStr);
    let bin = "";
    bytes.forEach(b => bin += String.fromCharCode(b));
    return btoa(bin);
}

function decodeSaveStr(b64) {
    const bin = atob(b64.trim());
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return JSON.parse(new TextDecoder().decode(bytes));
}

function loadSaveData() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const parsed = JSON.parse(raw);
            appState.stars = parsed.stars || {};
            appState.customLevels = parsed.customLevels || {};
        }
    } catch (e) {}
    updateTotalStarsUI();
}

function saveProgress() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            stars: appState.stars,
            customLevels: appState.customLevels,
            updatedAt: new Date().toISOString()
        }));
    } catch (e) {}
    updateTotalStarsUI();
    renderLevelBar();
}

function awardStars(g, l, s) {
    sfxWin();
    if (l < 20) {
        const k = `${g}_${l}`;
        appState.stars[k] = Math.max(appState.stars[k] || 0, s);
        saveProgress();
    }
    fireConfetti();
    const starIcons = "⭐".repeat(s);
    const nextBtnHtml = (l < 19)
        ? `<button class="cmd-btn" style="background:#69f0ae; padding:10px 18px; margin:6px;" onclick="closeModal(); loadLevel(${l+1});">⏩ 下一關 (第 ${l+2} 關)</button>`
        : `<button class="cmd-btn" style="background:#ff80ab; padding:10px 18px; margin:6px;" onclick="closeModal(); loadLevel(20);">🛠️ 前往自製創客關卡</button>`;

    showModal(`
        <h2 style="color:#ffd54f; margin:0 0 8px 0;">🎉 任務大成功！</h2>
        <div style="font-size:2.4rem; margin:6px 0;">${starIcons}</div>
        <p style="color:#eceff4; font-size:0.96rem;">恭喜完成 <b>${ l < 20 ? '第 ' + (l+1) + ' 關' : '自製創客關卡' }</b>！紀錄已自動儲存。</p>
        <div style="display:flex; justify-content:center; flex-wrap:wrap; margin-top:12px;">
            <button class="cmd-btn" style="background:#4fc3f7; padding:10px 16px; margin:6px;" onclick="closeModal();">🔄 留在本關</button>
            ${nextBtnHtml}
        </div>
    `);
}

function updateTotalStarsUI() {
    let total = 0;
    for (let g = 0; g < 5; g++) {
        for (let l = 0; l < 20; l++) {
            total += (appState.stars[`${g}_${l}`] || 0);
        }
    }
    document.getElementById("totalStarsBadge").innerText = `🏆 ${total} / 300 ⭐`;
}

// 存檔與 Excel 報表中心
function openSaveModal() {
    const passCode = encodeSaveObj({ stars: appState.stars, customLevels: appState.customLevels });
    showModal(`
        <h3 style="color:#4fc3f7; margin-top:0;">💾 雲端存檔與 Excel 學習報表中心</h3>
        <p style="font-size:0.84rem; color:#b0bec5; text-align:left; line-height:1.45;">
            ✅ <b>自動存檔已啟用</b>：闖關星章與自製關卡會自動保存在瀏覽器中。<br>
            📊 點擊<b>「複製 Excel 成績表」</b>後，打開 Microsoft Excel 按 <code>Ctrl + V</code> 即可直接貼上完整 100 關星章統計表！
        </p>
        <div style="display:flex; gap:6px; justify-content:center; margin:10px 0; flex-wrap:wrap;">
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 12px;" onclick="downloadJsonSave()">⬇️ 下載 .json 存檔</button>
            <label class="cmd-btn" style="background:#4fc3f7; padding:8px 12px; cursor:pointer;">
                📂 讀取 .json 存檔
                <input type="file" accept=".json" style="display:none;" onchange="uploadJsonSave(event)">
            </label>
            <button class="cmd-btn" style="background:#ffd54f; padding:8px 12px;" onclick="copyExcelTable()">📋 複製 Excel 成績表</button>
        </div>
        <div style="text-align:left; font-size:0.8rem; color:#ffd54f; margin-bottom:4px;">🔑 跨裝置存檔通行碼 (可複製到手機或另一台電腦貼上)：</div>
        <textarea id="saveCodeBox" style="width:100%; height:60px; background:#07090e; color:#69f0ae; border:1px solid #37474f; border-radius:6px; font-family:monospace; font-size:0.75rem; padding:6px;">${passCode}</textarea>
        <div id="modalMsg" style="font-size:0.84rem; color:#69f0ae; min-height:20px; margin-top:4px;"></div>
        <div style="display:flex; gap:8px; justify-content:center; margin-top:6px;">
            <button class="cmd-btn" style="background:#b388ff; padding:7px 14px;" onclick="importSaveCode()">📥 載入上方通行碼</button>
            <button class="cmd-btn" style="background:#ff80ab; padding:7px 14px;" onclick="resetAllSave()">🗑️ 清空紀錄</button>
            <button class="cmd-btn" style="background:#90a4ae; padding:7px 14px;" onclick="closeModal()">關閉</button>
        </div>
    `);
}

function copyExcelTable() {
    const gameNames = ["1.星際編碼號", "2.光子邏輯閘", "3.能量排序室", "4.星際河內塔", "5.像素解碼器"];
    let header = ["遊戲名稱"];
    for (let i = 1; i <= 20; i++) header.push(`第${i}關`);
    header.push("總星數(滿分60)");
    let rows = [header.join("\t")];

    for (let g = 0; g < 5; g++) {
        let row = [gameNames[g]];
        let sum = 0;
        for (let l = 0; l < 20; l++) {
            const s = appState.stars[`${g}_${l}`] || 0;
            sum += s;
            row.push(s);
        }
        row.push(sum);
        rows.push(row.join("\t"));
    }
    const tsv = rows.join("\n");
    navigator.clipboard.writeText(tsv).then(() => {
        document.getElementById("modalMsg").innerText = "✅ 已複製成績表！請打開 Excel 直接按 Ctrl + V 貼上。";
    }).catch(() => {
        document.getElementById("saveCodeBox").value = tsv;
        document.getElementById("modalMsg").innerText = "✅ 已將表格顯示於上方文字框，請全選複製並貼入 Excel！";
    });
}

function downloadJsonSave() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
        stars: appState.stars,
        customLevels: appState.customLevels
    }, null, 2));
    const a = document.createElement("a");
    a.setAttribute("href", dataStr);
    a.setAttribute("download", "star_logic_academy_save.json");
    document.body.appendChild(a);
    a.click();
    a.remove();
}

function uploadJsonSave(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data.stars) appState.stars = data.stars;
            if (data.customLevels) appState.customLevels = data.customLevels;
            saveProgress();
            loadLevel(appState.currentLevel);
            closeModal();
            showToast("🎉 存檔檔案讀取成功！", "ok");
        } catch (err) {
            document.getElementById("modalMsg").innerText = "⚠️ 存檔檔案格式不正確！";
        }
    };
    reader.readAsText(file);
}

function importSaveCode() {
    try {
        const raw = document.getElementById("saveCodeBox").value;
        const data = decodeSaveStr(raw);
        if (data.stars) appState.stars = data.stars;
        if (data.customLevels) appState.customLevels = data.customLevels;
        saveProgress();
        loadLevel(appState.currentLevel);
        closeModal();
        showToast("🎉 跨裝置通行碼載入成功！", "ok");
    } catch (e) {
        document.getElementById("modalMsg").innerText = "⚠️ 通行碼格式無效，請確認是否完整複製！";
    }
}

function resetAllSave() {
    appState.stars = {};
    appState.customLevels = {};
    saveProgress();
    loadLevel(appState.currentLevel);
    closeModal();
    showToast("已重置所有星章紀錄。", "warn");
}

function showModal(html) {
    document.getElementById("modalContent").innerHTML = html;
    document.getElementById("modalOverlay").style.display = "flex";
}
function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
}

function fireConfetti() {
    const cvs = document.getElementById("confettiCanvas");
    cvs.style.display = "block";
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    const ctx = cvs.getContext("2d");
    const pieces = Array.from({length: 70}, () => ({
        x: Math.random() * cvs.width,
        y: Math.random() * cvs.height - cvs.height,
        vx: (Math.random() - 0.5) * 6,
        vy: Math.random() * 5 + 4,
        c: ["#ffd54f","#69f0ae","#4fc3f7","#ff80ab","#b388ff"][Math.floor(Math.random()*5)],
        s: Math.random() * 8 + 5
    }));
    let frames = 0;
    function step() {
        ctx.clearRect(0, 0, cvs.width, cvs.height);
        pieces.forEach(p => {
            p.x += p.vx; p.y += p.vy;
            ctx.fillStyle = p.c;
            ctx.fillRect(p.x, p.y, p.s, p.s);
        });
        frames++;
        if (frames < 70) requestAnimationFrame(step);
        else cvs.style.display = "none";
    }
    step();
}

// ============================================================================
// 資料庫：5 款遊戲 × 各 20 關 + 各 1 自製關卡 = 105 關 (全關卡驗證完畢)
// ============================================================================

// --- 遊戲 1：🚀 星際編碼號 (20關 + 1自製) ---
// 7x7 編碼: 0=空地, 1=隕石, 2=水晶, 3=終點, 4=雷射門, 5=雷射開關, 6=蟲洞
const G1_LEVELS = [
    {name:"G1-01 直線啟航", opt:2, start:[1,5,0], desc:"歡迎來到星際編碼號！試著用「🔄重複 4 次」搭配「⬆️前進」直達太空船！", grid:["1111111","1311111","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-02 右轉彎道", opt:5, start:[1,5,0], desc:"先往上走 4 步，向右轉，再往前走 3 步抵達太空船！", grid:["1111111","1222311","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-03 雙重轉角", opt:7, start:[1,5,1], desc:"機器人面向右方！先往右 3 步、左轉往上 4 步、再左轉往左 2 步抵達終點。", grid:["1111111","1132211","1111211","1111211","1111211","1022211","1111111"]},
    {name:"G1-04 星際階梯", opt:5, start:[1,5,0], desc:"觀察規律：把「前進 ➔ 右轉 ➔ 前進 ➔ 左轉」放進重複 3 次迴圈！", grid:["1111111","1111111","1110311","1102111","1021111","1011111","1111111"]},
    {name:"G1-05 四階長梯", opt:5, start:[1,5,0], desc:"更長的階梯！同樣的 4 個動作，這次改用「🔄重複 4 次」一次解決！", grid:["1111111","1111031","1110211","1102111","1021111","1011111","1111111"]},
    {name:"G1-06 環狀巡航", opt:7, start:[1,5,0], desc:"沿著外圍收集所有水晶並抵達右下角太空船，善用迴圈縮短指令！", grid:["1111111","1222221","1211121","1211121","1211121","1011131","1111111"]},
    {name:"G1-07 雷射初體驗", opt:6, start:[1,3,1], desc:"紅色雷射擋路了！先走到「🔘開關
