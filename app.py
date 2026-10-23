import sys
import os
import subprocess

# 自動環境檢查：支援直接執行 python app.py 或雲端 streamlit run app.py
def ensure_streamlit():
    try:
        import streamlit as st
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
            sys.exit(0)
    except Exception:
        pass

ensure_streamlit()

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="星際邏輯學院 | 105關卡運算思維遊戲",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container { padding: 0.4rem 0.5rem 0rem 0.5rem !important; max-width: 100% !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌌 星際邏輯學院 Web 2.0")
    st.markdown("""
    - **5 大運算思維遊戲 × 各 20 關 + 自製沙盒 (共 105 關)**
    - 📱 **手機/平板適應**：可使用頂部「🔍縮放」滑桿調整大小，支援雙指縮放。
    - 💾 **跨裝置存檔**：點擊右上角「存檔管理」可下載 `.json` 存檔或複製通行碼。
    """)

# 使用單引號三引號包覆，並確保結尾清晰無截斷風險
GAME_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style>
    :root {
        --bg-panel: rgba(24, 27, 40, 0.94);
        --bg-card: #23273a;
        --blue: #64b5f6;
        --cyan: #4dd0e1;
        --green: #69f0ae;
        --gold: #ffd54f;
        --pink: #ff80ab;
        --purple: #b388ff;
        --text: #eceff4;
        --sub: #b0bec5;
    }
    * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }
    body {
        margin: 0; padding: 6px;
        background: radial-gradient(circle at 20% 20%, #1a1f35 0%, #0b0d14 100%);
        color: var(--text);
        font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
        overflow-x: hidden;
    }
    .top-header {
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        background: var(--bg-panel); border: 1px solid rgba(100,181,246,0.3);
        border-radius: 14px; padding: 8px 12px; margin-bottom: 8px; gap: 8px;
    }
    .brand {
        font-size: 1.2rem; font-weight: 900;
        background: linear-gradient(90deg, #ffd54f, #4dd0e1, #ff80ab);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .nav-tabs { display: flex; flex-wrap: wrap; gap: 5px; }
    .nav-btn {
        background: var(--bg-card); color: var(--text);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 9px;
        padding: 6px 10px; font-size: 0.85rem; font-weight: bold; cursor: pointer;
    }
    .nav-btn.active {
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #111; border-color: #fff; box-shadow: 0 0 10px rgba(255,213,79,0.5);
    }
    .header-right { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .star-badge {
        background: rgba(105,240,174,0.15); border: 1px solid var(--green);
        color: var(--green); padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.86rem;
    }
    .tool-btn {
        background: #37474f; color: #fff; border: 1px solid var(--cyan);
        padding: 5px 10px; border-radius: 8px; cursor: pointer; font-size: 0.82rem; font-weight: bold;
    }
    .level-bar {
        display: flex; align-items: center; gap: 5px; overflow-x: auto;
        background: var(--bg-panel); padding: 7px 10px; border-radius: 11px;
        border: 1px solid rgba(255,255,255,0.08); margin-bottom: 8px;
    }
    .lvl-btn {
        flex: 0 0 auto; background: var(--bg-card); color: var(--sub);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 7px;
        padding: 5px 8px; font-size: 0.8rem; font-weight: bold; cursor: pointer;
    }
    .lvl-btn.active { background: var(--blue); color: #000; border-color: #fff; }
    .lvl-btn.custom { background: linear-gradient(135deg, #ff80ab, #f50057); color: #fff; }
    .main-grid {
        display: grid; grid-template-columns: 1fr 340px; gap: 10px;
        transform-origin: top center; transition: transform 0.15s ease;
    }
    @media (max-width: 920px) { .main-grid { grid-template-columns: 1fr; } }
    .card {
        background: var(--bg-panel); border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.1); padding: 12px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
    }
    .lvl-title { font-size: 1.15rem; font-weight: bold; color: var(--gold); margin-bottom: 4px; }
    .lvl-desc { font-size: 0.9rem; color: var(--sub); margin-bottom: 10px; line-height: 1.4; }
    .game-flex { display: flex; flex-wrap: wrap; gap: 12px; align-items: flex-start; justify-content: center; }
    canvas {
        background: #0b0e17; border-radius: 12px; border: 2px solid rgba(100,181,246,0.35);
        max-width: 100%; height: auto; touch-action: manipulation;
    }
    .ctrl-box {
        flex: 1 1 240px; background: rgba(15,17,26,0.8);
        border-radius: 11px; padding: 10px; border: 1px solid rgba(255,255,255,0.08);
    }
    .block-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px; }
    .cmd-btn {
        border: none; border-radius: 8px; padding: 8px 6px;
        font-size: 0.88rem; font-weight: bold; cursor: pointer; color: #111;
    }
    .cmd-btn:active { transform: scale(0.95); }
    .cmd-list {
        background: #090b10; border-radius: 8px; padding: 6px;
        height: 185px; overflow-y: auto; font-family: Consolas, monospace;
        font-size: 0.86rem; border: 1px solid #2c3146; margin-top: 5px;
    }
    .cmd-item { padding: 3px 5px; border-radius: 4px; }
    .cmd-item.running { background: rgba(255,128,171,0.35); border-left: 3px solid var(--pink); color: #fff; }
    .status-bar {
        margin-top: 8px; padding: 7px 10px; border-radius: 8px;
        background: rgba(105,240,174,0.12); border-left: 4px solid var(--green);
        font-weight: bold; font-size: 0.88rem; color: var(--green);
    }
    .code-box {
        background: #090b10; color: #69f0ae; font-family: Consolas, monospace;
        font-size: 0.86rem; padding: 10px; border-radius: 9px;
        height: 290px; overflow-y: auto; white-space: pre-wrap; border: 1px solid #2e354d;
    }
    .concept-box {
        margin-top: 8px; background: rgba(255,213,79,0.1);
        border: 1px solid rgba(255,213,79,0.4); border-radius: 9px;
        padding: 9px; font-size: 0.85rem; color: var(--gold); line-height: 1.4;
    }
    .modal-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.78); z-index: 999; align-items: center; justify-content: center; padding: 14px;
    }
    .modal-box {
        background: #1a1e2e; border: 2px solid var(--cyan); border-radius: 14px;
        max-width: 500px; width: 100%; padding: 18px; text-align: center;
    }
    .brush-bar {
        display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px;
        background: rgba(255,255,255,0.06); padding: 7px; border-radius: 9px; justify-content: center;
    }
    .brush-btn {
        background: #2c3146; color: #fff; border: 1px solid transparent;
        padding: 4px 8px; border-radius: 6px; cursor: pointer; font-size: 0.8rem;
    }
    .brush-btn.active { border-color: var(--gold); background: #3f4765; }
</style>
</head>
<body>

<div class="top-header">
    <div class="brand">🚀 星際邏輯學院 <span style="font-size:0.78rem; color:#4dd0e1;">105關卡旗艦版</span></div>
    <div class="nav-tabs" id="gameTabs">
        <button class="nav-btn active" onclick="switchGame(0)">1️⃣ 星際編碼號</button>
        <button class="nav-btn" onclick="switchGame(1)">2️⃣ 光子邏輯閘</button>
        <button class="nav-btn" onclick="switchGame(2)">3️⃣ 能量排序室</button>
        <button class="nav-btn" onclick="switchGame(3)">4️⃣ 星際河內塔</button>
        <button class="nav-btn" onclick="switchGame(4)">5️⃣ 像素解碼器</button>
    </div>
    <div class="header-right">
        <div style="display:flex; align-items:center; gap:3px; font-size:0.8rem; color:#b0bec5;">
            🔍縮放:<input type="range" min="65" max="135" value="100" style="width:70px;" oninput="applyZoom(this.value)">
            <span id="zoomVal">100%</span>
        </div>
        <div class="star-badge" id="totalStarsBadge">🏆 0 / 300 ⭐</div>
        <button class="tool-btn" onclick="openSaveModal()">💾 存檔管理</button>
    </div>
</div>

<div class="level-bar" id="levelBar"></div>

<div class="main-grid" id="mainGrid">
    <div class="card">
        <div class="lvl-title" id="lvlTitle"></div>
        <div class="lvl-desc" id="lvlDesc"></div>
        <div id="stageContent"></div>
    </div>
    <div class="card">
        <div style="font-size:1rem; font-weight:bold; color:#69f0ae; margin-bottom:5px;">🐍 即時 Python 演算法透視窗</div>
        <div class="code-box" id="pythonPreview"></div>
        <div class="concept-box" id="conceptBox"></div>
    </div>
</div>

<div class="modal-overlay" id="modalOverlay"><div class="modal-box" id="modalContent"></div></div>
<canvas id="confettiCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:998; display:none;"></canvas>

<script>
const STORAGE_KEY = "STAR_LOGIC_ACADEMY_SAVE_V2";
let appState = { currentGame: 0, currentLevel: 0, stars: {}, customLevels: {} };

function loadSaveData() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const p = JSON.parse(raw);
            appState.stars = p.stars || {};
            appState.customLevels = p.customLevels || {};
        }
    } catch (e) {}
    updateTotalStarsUI();
}

function saveProgress() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ stars: appState.stars, customLevels: appState.customLevels }));
    } catch (e) {}
    updateTotalStarsUI();
    renderLevelBar();
}

function awardStars(g, l, s) {
    if (l < 20) {
        const k = g + "_" + l;
        appState.stars[k] = Math.max(appState.stars[k] || 0, s);
        saveProgress();
    }
    fireConfetti();
    const nextBtn = (l < 19)
        ? `<button class="cmd-btn" style="background:#69f0ae; padding:9px 18px; margin:6px;" onclick="closeModal(); loadLevel(${l+1});">⏩ 下一關 (第 ${l+2} 關)</button>`
        : `<button class="cmd-btn" style="background:#ff80ab; padding:9px 18px; margin:6px;" onclick="closeModal(); loadLevel(20);">🛠️ 自製創客關卡</button>`;
    showModal(`
        <h2 style="color:#ffd54f; margin:0;">🎉 闖關成功！</h2>
        <div style="font-size:2.3rem; margin:8px 0;">${"⭐".repeat(s)}</div>
        <p style="color:#eceff4;">恭喜完成 <b>第 ${l+1} 關</b>！進度已自動儲存。</p>
        <div>
            <button class="cmd-btn" style="background:#64b5f6; padding:9px 14px; margin:6px;" onclick="closeModal();">🔄 留在本關</button>
            ${nextBtn}
        </div>
    `);
}

function updateTotalStarsUI() {
    let total = 0;
    for (let g = 0; g < 5; g++) for (let l = 0; l < 20; l++) total += (appState.stars[g + "_" + l] || 0);
    document.getElementById("totalStarsBadge").innerText = `🏆 ${total} / 300 ⭐`;
}

function applyZoom(val) {
    document.getElementById("zoomVal").innerText = val + "%";
    document.getElementById("mainGrid").style.transform = `scale(${val / 100})`;
}

function openSaveModal() {
    const code = btoa(encodeURIComponent(JSON.stringify({ stars: appState.stars, customLevels: appState.customLevels })));
    showModal(`
        <h3 style="color:#4dd0e1; margin-top:0;">💾 雲端與跨裝置存檔中心</h3>
        <div style="display:flex; gap:6px; justify-content:center; margin:10px 0; flex-wrap:wrap;">
            <button class="cmd-btn" style="background:#69f0ae; padding:7px 12px;" onclick="downloadJsonSave()">⬇️ 下載 .json 存檔</button>
            <label class="cmd-btn" style="background:#64b5f6; padding:7px 12px; cursor:pointer;">📂 讀取 .json<input type="file" accept=".json" style="display:none;" onchange="uploadJsonSave(event)"></label>
            <button class="cmd-btn" style="background:#ff80ab; padding:7px 12px;" onclick="resetAllSave()">🗑️ 清空重來</button>
        </div>
        <div style="text-align:left; font-size:0.8rem; color:#ffd54f;">🔑 跨裝置通行碼 (可複製到手機貼上)：</div>
        <textarea id="saveCodeBox" style="width:100%; height:60px; background:#090b10; color:#69f0ae; border:1px solid #455a64; border-radius:6px; font-size:0.75rem; margin-top:4px;">${code}</textarea>
        <div style="margin-top:8px;">
            <button class="cmd-btn" style="background:#ffd54f; padding:6px 12px;" onclick="importSaveCode()">📥 載入通行碼</button>
            <button class="cmd-btn" style="background:#b0bec5; padding:6px 12px;" onclick="closeModal()">關閉</button>
        </div>
    `);
}

function downloadJsonSave() {
    const s = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ stars: appState.stars, customLevels: appState.customLevels }, null, 2));
    const a = document.createElement("a");
    a.href = s; a.download = "star_logic_save.json"; document.body.appendChild(a); a.click(); a.remove();
}

function uploadJsonSave(e) {
    const f = e.target.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = function(ev) {
        try {
            const d = JSON.parse(ev.target.result);
            if (d.stars) appState.stars = d.stars;
            if (d.customLevels) appState.customLevels = d.customLevels;
            saveProgress(); loadLevel(appState.currentLevel); closeModal();
        } catch (err) { alert("存檔格式錯誤！"); }
    };
    r.readAsText(f);
}

function importSaveCode() {
    try {
        const d = JSON.parse(decodeURIComponent(atob(document.getElementById("saveCodeBox").value.trim())));
        if (d.stars) appState.stars = d.stars;
        if (d.customLevels) appState.customLevels = d.customLevels;
        saveProgress(); loadLevel(appState.currentLevel); closeModal();
    } catch (e) { alert("通行碼無效！"); }
}

function resetAllSave() {
    if (confirm("確定要清空所有星章紀錄嗎？")) {
        appState.stars = {}; appState.customLevels = {};
        saveProgress(); loadLevel(appState.currentLevel); closeModal();
    }
}

function showModal(html) { document.getElementById("modalContent").innerHTML = html; document.getElementById("modalOverlay").style.display = "flex"; }
function closeModal() { document.getElementById("modalOverlay").style.display = "none"; }

function fireConfetti() {
    const cvs = document.getElementById("confettiCanvas");
    cvs.style.display = "block"; cvs.width = window.innerWidth; cvs.height = window.innerHeight;
    const ctx = cvs.getContext("2d");
    const ps = Array.from({length: 65}, () => ({
        x: Math.random() * cvs.width, y: -20,
        vx: (Math.random() - 0.5) * 6, vy: Math.random() * 5 + 4,
        c: ["#ffd54f","#69f0ae","#64b5f6","#ff80ab","#b388ff"][Math.floor(Math.random()*5)], s: Math.random() * 7 + 5
    }));
    let f = 0;
    function step() {
        ctx.clearRect(0, 0, cvs.width, cvs.height);
        ps.forEach(p => { p.x += p.vx; p.y += p.vy; ctx.fillStyle = p.c; ctx.fillRect(p.x, p.y, p.s, p.s); });
        if (++f < 70) requestAnimationFrame(step); else cvs.style.display = "none";
    }
    step();
}

// ============================================================================
// 5 款遊戲 × (20 關 + 1 自製關卡) 題庫
// ============================================================================
const G1_LEVELS = [
    {name:"G1-01 直線啟航", opt:2, start:[1,5,0], desc:"用「🔄重複 4 次」搭配「⬆️前進」直達太空船！", grid:["1111111","1311111","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-02 右轉彎道", opt:5, start:[1,5,0], desc:"先往上走 4 步，向右轉，再往前走 3 步抵達太空船！", grid:["1111111","1222311","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-03 雙重轉角", opt:7, start:[1,5,1], desc:"機器人面向右方！先往右、再往上、最後往左抵達終點。", grid:["1111111","1132211","1111211","1111211","1111211","1022211","1111111"]},
    {name:"G1-04 星際階梯", opt:5, start:[1,5,0], desc:"把「前進 ➔ 右轉 ➔ 前進 ➔ 左轉」放進重複 3 次迴圈！", grid:["1111111","1111111","1110311","1102111","1021111","1011111","1111111"]},
    {name:"G1-05 四階長梯", opt:5, start:[1,5,0], desc:"更長的階梯！同樣的 4 個動作改用「🔄重複 4 次」一次解決！", grid:["1111111","1111031","1110211","1102111","1021111","1011111","1111111"]},
    {name:"G1-06 環狀巡航", opt:7, start:[1,5,0], desc:"沿著外圍收集水晶，善用兩段迴圈縮短指令！", grid:["1111111","1222221","1211121","1211121","1211121","1011131","1111111"]},
    {name:"G1-07 雷射初體驗", opt:6, start:[1,3,1], desc:"先走到「🔘開關」格執行「👆開關」，即可解除紅色雷射！", grid:["1111111","1111111","1111111","1025423","1111111","1111111","1111111"]},
    {name:"G1-08 雷射支線", opt:8, start:[1,5,0], desc:"先直走去最上方按下雷射開關，再轉彎通過雷射門！", grid:["1111111","1522431","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-09 折返解鎖", opt:9, start:[1,3,1], desc:"開關在上方小房間，進去按完開關後向後轉出來繼續前進！", grid:["1111111","1115111","1112111","1020423","1111111","1111111","1111111"]},
    {name:"G1-10 雙重防衛網", opt:8, start:[1,5,0], desc:"一個開關可以同時解除地圖上所有的雷射門！", grid:["1111111","1542431","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-11 蟲洞初體驗", opt:4, start:[1,5,1], desc:"走進「🌀蟲洞」會瞬間移動到另一個蟲洞，且面向不變！", grid:["1111111","1622231","1111111","1111111","1111111","1022611","1111111"]},
    {name:"G1-12 蟲洞轉向", opt:6, start:[1,5,0], desc:"從下方往上走進蟲洞，出來後也是朝上喔！記得右轉拿水晶。", grid:["1111111","1111111","1162231","1111111","1611111","1011111","1111111"]},
    {name:"G1-13 蟲洞與雷射", opt:7, start:[1,5,0], desc:"先往上踩開關，再走進蟲洞躍遷到右側通道直達終點！", grid:["1111111","1611131","1511141","1211121","1211161","1011111","1111111"]},
    {name:"G1-14 螺旋向心", opt:9, start:[1,5,0], desc:"順時針螺旋迷宮！算準每一邊的長度推進到中心太空船。", grid:["1111111","1222221","1211121","1213121","1212221","1011111","1111111"]},
    {name:"G1-15 之字形峽谷", opt:8, start:[1,5,0], desc:"連續彎道，考驗左轉與右轉的空間相對方向感！", grid:["1111111","1112231","1112111","1222111","1211111","1011111","1111111"]},
    {name:"G1-16 階梯雷射陣", opt:8, start:[1,5,0], desc:"先用階梯迴圈爬到頂端按下開關，再衝向終點！", grid:["1111111","1111543","1110211","1102111","1021111","1011111","1111111"]},
    {name:"G1-17 雙島躍遷", opt:7, start:[1,5,1], desc:"利用蟲洞在兩座孤島間穿梭，先開開關再前往終點！", grid:["1111111","1116231","1111141","1111121","1111151","1025611","1111111"]},
    {name:"G1-18 迴圈傳送帶", opt:5, start:[1,5,0], desc:"把蟲洞躍遷也算進「🔄重複迴圈」步數裡，3 行指令就能過關！", grid:["1111111","1111311","1111211","1611211","1211611","1011111","1111111"]},
    {name:"G1-19 矩陣巡邏官", opt:9, start:[1,5,0], desc:"收集三條通道的水晶，善用迴圈減少重複的直走指令！", grid:["1111111","1222221","1211121","1213221","1211111","1011111","1111111"]},
    {name:"G1-20 星際總司令", opt:9, start:[1,5,0], desc:"畢業考驗！結合長廊迴圈、雷射開關與蟲洞躍遷拿下三星！", grid:["1111111","1526131","1211141","1211121","1211161","1011111","1111111"]},
    {name:"🛠️ 自製創客迷宮", opt:6, start:[1,5,0], desc:"【創客模式】點擊下方畫筆直接塗改地圖，設計完畢後按執行測試！", grid:["1111111","1000311","1011011","1211011","1011011","1000011","1111111"]}
];

const G2_LEVELS = [
    {name:"G2-01 認識 AND 合力門", ins:2, g1:"AND", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【AND 門】兩個輸入都必須是 1，輸出才會是 1！"},
    {name:"G2-02 認識 OR 任一門", ins:2, g1:"OR", g2:"NONE", g3:"NONE", rule:"EXACT_1", desc:"【OR 門】只要任一個是 1 就會通電！（限制：剛好開 1 個開關）"},
    {name:"G2-03 認識 XOR 獨享門", ins:2, g1:"XOR", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【XOR 門】兩個輸入必須「一亮一暗（不同）」，輸出才會是 1！"},
    {name:"G2-04 認識 NAND 反合力門", ins:2, g1:"NAND", g2:"NONE", g3:"NONE", rule:"AT_LEAST_1", desc:"【NAND 門】只要不全為 1 就輸出 1！（限制：至少開 1 個開關）"},
    {name:"G2-05 認識 NOR 全暗門", ins:2, g1:"NOR", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【NOR 門】只有當兩個輸入都是 0 時，輸出才會是 1！"},
    {name:"G2-06 雙閘合力串聯", ins:4, g1:"AND", g2:"OR", g3:"AND", rule:"MAX_3", desc:"G1(AND) 與 G2(OR) 都要是 1，最終 G3(AND) 才會亮！（最多開 3 個）"},
    {name:"G2-07 獨享與合力交會", ins:4, g1:"XOR", g2:"AND", g3:"AND", rule:"NONE", desc:"G1(XOR) 需一亮一暗，G2(AND) 需全亮，最終匯集點亮核心！"},
    {name:"G2-08 雙重獨享謎題", ins:4, g1:"XOR", g2:"XOR", g3:"XOR", rule:"EXACT_1", desc:"三個都是 XOR 門！限制：【只能開啟剛好 1 個開關】點亮核心！"},
    {name:"G2-09 雙重獨享與合力", ins:4, g1:"XOR", g2:"XOR", g3:"AND", rule:"EXACT_2", desc:"上下兩個 XOR 都必須輸出 1，且【剛好開啟 2 個開關】！"},
    {name:"G2-10 反轉陷阱電路", ins:4, g1:"NAND", g2:"AND", g3:"AND", rule:"EXACT_2", desc:"G1 是 NAND（全亮會斷電），G2 是 AND。請用【剛好 2 個開關】點亮核心！"},
    {name:"G2-11 靜音啟動電路", ins:4, g1:"NOR", g2:"OR", g3:"AND", rule:"EXACT_1", desc:"G1(NOR) 必須全 0 才會輸出 1！請用【剛好 1 個開關】啟動核心。"},
    {name:"G2-12 對稱反轉網路", ins:4, g1:"NAND", g2:"NAND", g3:"XOR", rule:"EXACT_2", desc:"最後是 XOR，代表 G1 與 G2 必須一亮一暗！限制：【剛好開 2 個開關】。"},
    {name:"G2-13 高壓防過載", ins:4, g1:"OR", g2:"NAND", g3:"XOR", rule:"EXACT_3", desc:"限制：【必須開啟剛好 3 個開關】，且讓最終 XOR 輸出 1！"},
    {name:"G2-14 零能量反轉", ins:4, g1:"AND", g2:"OR", g3:"NOR", rule:"EXACT_1", desc:"最終是 NOR 門（G1 與 G2 都必須是 0 才會亮）！限制：【剛好開 1 個開關】。"},
    {name:"G2-15 雙核反合力", ins:4, g1:"XOR", g2:"XOR", g3:"NAND", rule:"EXACT_2", desc:"限制：【剛好開 2 個開關】且『開關 A 必須開啟』，讓最終 NAND 輸出 1！"},
    {name:"G2-16 嚴格奇偶檢驗", ins:4, g1:"AND", g2:"NOR", g3:"OR", rule:"EXACT_2", desc:"限制：【剛好開 2 個開關】，使 G1(AND) 或 G2(NOR) 至少一邊輸出 1！"},
    {name:"G2-17 邏輯鎖定迴路", ins:4, g1:"NOR", g2:"XOR", g3:"AND", rule:"EXACT_1", desc:"G1(NOR) 與 G2(XOR) 必須同時輸出 1！找出唯一符合的開關組合。"},
    {name:"G2-18 反向互斥網路", ins:4, g1:"NAND", g2:"NOR", g3:"XOR", rule:"EXACT_3", desc:"限制：【必須開啟剛好 3 個開關】，並使 G1(NAND) 與 G2(NOR) 結果相異！"},
    {name:"G2-19 雙通道極限", ins:4, g1:"XOR", g2:"NAND", g3:"AND", rule:"EXACT_3", desc:"限制：【必須開啟剛好 3 個開關】，且 G1(XOR) 與 G2(NAND) 同時為 1！"},
    {name:"G2-20 首席晶片架構師", ins:4, g1:"NOR", g2:"NAND", g3:"AND", rule:"EXACT_1", desc:"終極考驗：限制【剛好開啟 1 個開關】，同時滿足 NOR 與 NAND！"},
    {name:"🛠️ 自製數位電路", ins:4, g1:"XOR", g2:"AND", g3:"OR", rule:"NONE", desc:"【創客模式】直接點擊畫布中間的邏輯閘方塊，即可切換 AND/OR/XOR/NAND/NOR！"}
];

const G3_LEVELS = [
    {name:"G3-01 三瓶暖身排序", arr:[30,10,20], mode:"ASC", adj:false, opt:2, desc:"【由小到大】點擊兩瓶能量液交換位置！2 步內排成 [10, 20, 30]。"},
    {name:"G3-02 四瓶首尾對調", arr:[40,30,20,10], mode:"ASC", adj:false, opt:2, desc:"【由小到大】觀察對稱性，只需交換 2 次就能把 4 瓶完全排好！"},
    {name:"G3-03 五瓶選擇排序", arr:[50,20,40,10,30], mode:"ASC", adj:false, opt:3, desc:"【由小到大】先找最小的放左邊，3 次交換內完成排序！"},
    {name:"G3-04 遞減排序挑戰", arr:[15,45,25,35], mode:"DESC", adj:false, opt:2, desc:"【由大到小】這次要把數字最大的排在最左邊 [45, 35, 25, 15]！"},
    {name:"G3-05 五瓶高能遞減", arr:[20,60,10,50,40], mode:"DESC", adj:false, opt:3, desc:"【由大到小】找出可以直接互相歸位的配對，3 步完成！"},
    {name:"G3-06 泡泡限制初體驗", arr:[30,10,40,20], mode:"ASC", adj:true, opt:2, desc:"⚠️【泡泡限制：只能交換相鄰兩瓶】體驗泡泡排序法一步步推移！"},
    {name:"G3-07 四瓶逆序泡泡", arr:[40,30,10,20], mode:"ASC", adj:true, opt:5, desc:"⚠️【只能交換相鄰兩瓶】把最小的 10 與 20 一步步往左推！"},
    {name:"G3-08 五瓶泡泡推移", arr:[20,40,10,50,30], mode:"ASC", adj:true, opt:3, desc:"⚠️【只能交換相鄰兩瓶】觀察誰擋住了誰，3 步完成！"},
    {name:"G3-09 奇偶分流初階", arr:[15,20,35,40], mode:"EVEN_ODD", adj:false, opt:1, desc:"【奇偶分流】左邊排偶數(小到大)，右邊排奇數(小到大) -> [20, 40, 15, 35]！"},
    {name:"G3-10 六瓶奇偶分流", arr:[11,40,33,20,22,15], mode:"EVEN_ODD", adj:false, opt:3, desc:"【奇偶分流】偶數 [20, 22, 40] 排左邊，奇數 [11, 15, 33] 排右邊！"},
    {name:"G3-11 能量山峰陣列", arr:[10,50,20,40,30], mode:"MOUNTAIN", adj:false, opt:2, desc:"【山峰排序】排成中間最高、兩側遞減：[10, 30, 50, 40, 20]！"},
    {name:"G3-12 能量山谷陣列", arr:[30,10,50,20,40], mode:"VALLEY", adj:false, opt:2, desc:"【山谷排序】排成兩側高、中間最低：[50, 30, 10, 20, 40]！"},
    {name:"G3-13 波浪高低交錯", arr:[10,20,30,40,50], mode:"ZIGZAG", adj:false, opt:2, desc:"【波浪排序】排成高低交錯：[20, 10, 40, 30, 50]！"},
    {name:"G3-14 六瓶自由最佳化", arr:[60,50,40,30,20,10], mode:"ASC", adj:false, opt:3, desc:"【由小到大】6 瓶完全反序，對稱交換只需 3 步！"},
    {name:"G3-15 六瓶循環置換", arr:[20,30,40,50,60,10], mode:"ASC", adj:false, opt:5, desc:"【由小到大】全部往左錯位一格！體驗循環置換需 5 步。"},
    {name:"G3-16 五瓶泡泡進階", arr:[50,10,40,20,30], mode:"ASC", adj:true, opt:5, desc:"⚠️【只能交換相鄰兩瓶】5 瓶泡泡排序，黃金目標 5 步！"},
    {name:"G3-17 泡泡遞減挑戰", arr:[10,40,20,50,30], mode:"DESC", adj:true, opt:5, desc:"⚠️【只能交換相鄰兩瓶 + 由大到小】把大數往左浮上去！"},
    {name:"G3-18 七瓶極速歸位", arr:[70,20,50,10,60,40,30], mode:"ASC", adj:false, opt:5, desc:"【由小到大】7 瓶高難度亂序！先找能互相歸位的雙向交換。"},
    {name:"G3-19 八瓶旗艦排序", arr:[80,10,60,30,50,40,70,20], mode:"ASC", adj:false, opt:6, desc:"【由小到大】8 瓶大型陣列！運用選擇排序思維在 6 步內破解！"},
    {name:"G3-20 排序演算法宗師", arr:[50,30,40,10,20], mode:"ASC", adj:true, opt:7, desc:"⚠️【終極泡泡考驗：只能交換相鄰兩瓶】在 7 步內完成由小到大排序！"},
    {name:"🛠️ 自製排序實驗室", arr:[60,10,40,20,50,30], mode:"ASC", adj:false, opt:4, desc:"【創客模式】可在下方輸入自訂數字序列，並切換排序規則！"}
];

const G4_LEVELS = [
    {name:"G4-01 雙環初體驗", pegs:[[2,1],[],[]], target:2, adj:false, opt:3, desc:"把所有能量環移到 C 柱！規則：小環永遠只能疊在大環上面。"},
    {name:"G4-02 指定 B 柱終點", pegs:[[2,1],[],[]], target:1, adj:false, opt:3, desc:"這次目標終點在中間的「B 柱」喔！只需 3 步。"},
    {name:"G4-03 散落雙環集合", pegs:[[],[2],[1]], target:0, adj:false, opt:2, desc:"能量環散開了！請用 2 步將它們全部集中到最左邊的「A 柱」。"},
    {name:"G4-04 經典三環河內塔", pegs:[[3,2,1],[],[]], target:2, adj:false, opt:7, desc:"先把 [2,1] 移到 B 柱，再把大環 3 移到 C 柱。黃金 7 步！"},
    {name:"G4-05 三環移往中柱", pegs:[[3,2,1],[],[]], target:1, adj:false, opt:7, desc:"將 3 個環全部移到中間的「B 柱」！"},
    {name:"G4-06 散落三環重組", pegs:[[3],[2],[1]], target:2, adj:false, opt:3, desc:"三環各據一柱！只需 3 步就能在 C 柱完成合體！"},
    {name:"G4-07 錯位三環救援", pegs:[[3,1],[2],[]], target:2, adj:false, opt:5, desc:"觀察目前狀態，不用重頭搬，5 步內移到 C 柱！"},
    {name:"G4-08 四柱三環極速版", pegs:[[3,2,1],[],[],[]], target:3, adj:false, opt:5, desc:"多了一根 D 柱（共 4 柱）！善用多出來的柱子，3 環只需 5 步！"},
    {name:"G4-09 相鄰限制：雙環", pegs:[[2,1],[],[]], target:2, adj:true, opt:8, desc:"⚠️【相鄰限制：每次只能移到隔壁柱子 (A↔B↔C)】不能直接跨越！"},
    {name:"G4-10 相鄰限制：中柱起點", pegs:[[],[2,1],[]], target:2, adj:true, opt:4, desc:"⚠️【相鄰限制】從中間 B 柱出發，利用 A 柱緩衝移往 C 柱！"},
    {name:"G4-11 四環散落重組", pegs:[[4],[3],[2,1]], target:0, adj:false, opt:5, desc:"最大環 4 號已經在目標 A 柱底下了！只需把剩下 3 環搬過去。"},
    {name:"G4-12 四環雙塔合流", pegs:[[4,3],[2,1],[]], target:2, adj:false, opt:11, desc:"[4,3] 與 [2,1] 分成兩疊，規劃緩衝區移往 C 柱！"},
    {name:"G4-13 四柱四環挑戰", pegs:[[4,3,2,1],[],[],[]], target:3, adj:false, opt:9, desc:"4 根柱子搬運 4 個能量環！黃金步數只要 9 步！"},
    {name:"G4-14 經典三柱四環", pegs:[[4,3,2,1],[],[]], target:2, adj:false, opt:15, desc:"經典 4 環河內塔！運用遞迴思維（7+1+7=15步）完美破解！"},
    {name:"G4-15 四柱散落五環", pegs:[[5,4],[3],[2],[1]], target:0, adj:false, opt:6, desc:"5 個環散落在 4 根柱子，且 5 與 4 已經在目標 A 柱了！"},
    {name:"G4-16 四柱五環星際塔", pegs:[[5,4,3,2,1],[],[],[]], target:3, adj:false, opt:13, desc:"5 個能量環登場！利用 4 根柱子在 13 步內移到 D 柱！"},
    {name:"G4-17 四柱相鄰限制(3環)", pegs:[[3,2,1],[],[],[]], target:3, adj:true, opt:10, desc:"⚠️【4 柱 + 僅限相鄰柱移動】將 3 個環一路往右推進到 D 柱！"},
    {name:"G4-18 逆境五環救援", pegs:[[5],[4,3],[2,1]], target:0, adj:false, opt:11, desc:"5 號大環已在 A 柱，把 [4,3] 與 [2,1] 疊回 A 柱！"},
    {name:"G4-19 經典三柱五環", pegs:[[5,4,3,2,1],[],[]], target:2, adj:false, opt:31, desc:"三柱 5 環大考驗（黃金 31 步）！考驗極致專注力與遞迴節奏。"},
    {name:"G4-20 遞迴宗師：相鄰三環", pegs:[[3,2,1],[],[]], target:2, adj:true, opt:26, desc:"⚠️【終極考驗：3 柱 3 環 + 只能移到相鄰柱子】黃金步數 26 步！"},
    {name:"🛠️ 自製河內塔工坊", pegs:[[3,2,1],[],[]], target:2, adj:false, opt:7, desc:"【創客模式】使用下方工具自由設定環數(2~5)、柱數(3~4)與相鄰限制！"}
];

const G5_LEVELS = [
    {name:"G5-01 太空能量愛心", grid:["011011","111111","111111","011110","001100","000000"]},
    {name:"G5-02 光束十字星", grid:["001100","001100","111111","111111","001100","001100"]},
    {name:"G5-03 微笑機器人", grid:["011110","101101","111111","100001","110011","011110"]},
    {name:"G5-04 衝鋒太空梭", grid:["001100","011110","010010","111111","101101","100001"]},
    {name:"G5-05 星際小怪獸", grid:["100001","011110","110011","111111","010010","100001"]},
    {name:"G5-06 榮耀皇冠", grid:["101101","101101","111111","110011","111111","000000"]},
    {name:"G5-07 雷射鑽石", grid:["001100","011110","110011","110011","011110","001100"]},
    {name:"G5-08 矩陣金鑰", grid:["011100","010100","011100","001000","001110","001010"]},
    {name:"G5-09 防護裝甲盾", grid:["111111","101101","111111","011110","010010","001100"]},
    {name:"G5-10 冠軍聖盃", grid:["111111","101101","011110","001100","011110","111111"]},
    {name:"G5-11 超能閃電", grid:["001110","011100","111111","001110","011000","110000"]},
    {name:"G5-12 星際戰機", grid:["001100","001100","111111","111111","101101","011110"]},
    {name:"G5-13 智慧貓頭鷹", grid:["100001","111111","101101","111111","011110","010010"]},
    {name:"G5-14 幸運四葉草", grid:["010010","111111","011110","011110","111111","010010"]},
    {name:"G5-15 機械音樂耳機", grid:["011110","100001","100001","110011","110011","000000"]},
    {name:"G5-16 深空船錨", grid:["001100","011110","001100","101101","111111","011110"]},
    {name:"G5-17 時光沙漏", grid:["111111","011110","001100","001100","010010","111111"]},
    {name:"G5-18 密碼寶箱", grid:["011110","111111","101101","111111","100001","111111"]},
    {name:"G5-19 雙子星座標", grid:["110000","110011","001111","111100","110011","000011"]},
    {name:"G5-20 銀河無限符號", grid:["000000","011011","100101","101001","110110","000000"]},
    {name:"🛠️ 自製像素謎題", grid:["100001","010010","001100","001100","010010","100001"]}
];

function switchGame(gIdx) {
    g1StopTimer(); appState.currentGame = gIdx;
    document.querySelectorAll("#gameTabs .nav-btn").forEach((b, i) => b.classList.toggle("active", i === gIdx));
    loadLevel(0);
}

function renderLevelBar() {
    let html = "";
    for (let i = 0; i < 21; i++) {
        const isC = (i === 20), isA = (i === appState.currentLevel);
        const st = appState.stars[appState.currentGame + "_" + i] || 0;
        const lbl = isC ? "🛠️ 自製關卡" : `第${i+1}關${st ? " "+"★".repeat(st) : ""}`;
        html += `<button class="lvl-btn ${isC?'custom':''} ${isA?'active':''}" onclick="loadLevel(${i})">${lbl}</button>`;
    }
    document.getElementById("levelBar").innerHTML = html;
}

function loadLevel(lIdx) {
    g1StopTimer(); appState.currentLevel = lIdx; renderLevelBar();
    const g = appState.currentGame;
    if (g === 0) initGame1(lIdx);
    else if (g === 1) initGame2(lIdx);
    else if (g === 2) initGame3(lIdx);
    else if (g === 3) initGame4(lIdx);
    else if (g === 4) initGame5(lIdx);
}

function updatePythonBox(code, tip) {
    document.getElementById("pythonPreview").innerText = code;
    document.getElementById("conceptBox").innerHTML = `💡 <b>運算思維小百科：</b><br>${tip}`;
}

// --- 遊戲 1：星際編碼號 ---
let g1State = { cmds: [], grid: [], rx:1, ry:5, rdir:0, laserOn:true, gotC:0, totalC:0, timer:null, brush:1 };
function g1StopTimer() { if (g1State.timer) { clearTimeout(g1State.timer); g1State.timer = null; } }

function initGame1(lIdx) {
    if (lIdx === 20 && appState.customLevels.g1) G1_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g1));
    const lvl = G1_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🚀 ${lvl.name} 【⭐⭐⭐ 黃金目標：${lvl.opt} 個有效積木】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g1State.cmds = []; g1State.brush = 1;
    const customHtml = (lIdx === 20) ? `<div class="brush-bar" id="g1BrushBar">
        <button class="brush-btn" onclick="g1SetBrush(0,this)">空地</button>
        <button class="brush-btn active" onclick="g1SetBrush(1,this)">🪨隕石</button>
        <button class="brush-btn" onclick="g1SetBrush(2,this)">💎水晶</button>
        <button class="brush-btn" onclick="g1SetBrush(3,this)">🛸終點</button>
        <button class="brush-btn" onclick="g1SetBrush(4,this)">🔴雷射</button>
        <button class="brush-btn" onclick="g1SetBrush(5,this)">🔘開關</button>
        <button class="brush-btn" onclick="g1SetBrush(6,this)">🌀蟲洞</button>
        <button class="brush-btn" onclick="g1SetBrush(99,this)">🤖起點/轉向</button>
    </div>` : "";

    document.getElementById("stageContent").innerHTML = `<div class="game-flex">
        <div>
            <canvas id="g1Canvas" width="420" height="420"></canvas>
            <div class="status-bar" id="g1Status">🤖 機器人就緒！請在右側點擊積木編排程式。</div>
            ${customHtml}
        </div>
        <div class="ctrl-box">
            <div class="block-grid">
                <button class="cmd-btn" style="background:#64b5f6;" onclick="g1Add('MOVE')">⬆️ 前進</button>
                <button class="cmd-btn" style="background:#4dd0e1;" onclick="g1Add('LEFT')">↩️ 左轉</button>
                <button class="cmd-btn" style="background:#4dd0e1;" onclick="g1Add('RIGHT')">↪️ 右轉</button>
                <button class="cmd-btn" style="background:#ffd54f;" onclick="g1Add('SWITCH')">👆 開關</button>
                <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_2')">🔄 重複 2 次</button>
                <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_3')">🔄 重複 3 次</button>
                <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_4')">🔄 重複 4 次</button>
                <button class="cmd-btn" style="background:#ea80fc;" onclick="g1Add('END_LOOP')">🔚 結束重複</button>
            </div>
            <div style="display:flex; gap:5px; margin-bottom:6px;">
                <button class="cmd-btn" style="background:#69f0ae; flex:2;" onclick="g1Run()">▶️ 執行</button>
                <button class="cmd-btn" style="background:#ffb74d; flex:1;" onclick="g1Pop()">⌫ 退回</button>
                <button class="cmd-btn" style="background:#ff80ab; flex:1;" onclick="g1Clear()">🗑️ 清空</button>
            </div>
            <div style="font-size:0.82rem; color:#ffd54f; font-weight:bold;" id="g1CmdHeader"></div>
            <div class="cmd-list" id="g1CmdList"></div>
        </div>
    </div>`;
    document.getElementById("g1Canvas").addEventListener("click", g1CanvasClick);
    g1ResetBoard(); g1RenderCmds(-1);
}

function g1SetBrush(b, el) {
    g1State.brush = b;
    document.querySelectorAll("#g1BrushBar .brush-btn").forEach(x => x.classList.remove("active"));
    el.classList.add("active");
}

function g1CanvasClick(e) {
    if (appState.currentLevel !== 20 || g1State.timer) return;
    const r = e.target.getBoundingClientRect();
    const gx = Math.floor((e.clientX - r.left) * (420 / r.width) / 60);
    const gy = Math.floor((e.clientY - r.top) * (420 / r.height) / 60);
    if (gx >= 0 && gx < 7 && gy >= 0 && gy < 7) {
        const lvl = G1_LEVELS[20];
        let row = lvl.grid[gy].split("");
        if (g1State.brush === 99) {
            if (lvl.start[0] === gx && lvl.start[1] === gy) lvl.start[2] = (lvl.start[2] + 1) % 4;
            else { lvl.start[0] = gx; lvl.start[1] = gy; }
            row[gx] = "0";
        } else row[gx] = String(g1State.brush);
        lvl.grid[gy] = row.join("");
        appState.customLevels.g1 = JSON.parse(JSON.stringify(lvl));
        saveProgress(); g1ResetBoard();
    }
}

function g1ResetBoard() {
    g1StopTimer();
    const lvl = G1_LEVELS[appState.currentLevel];
    g1State.grid = lvl.grid.map(r => r.split("").map(Number));
    [g1State.rx, g1State.ry, g1State.rdir] = lvl.start;
    g1State.laserOn = true; g1State.gotC = 0;
    g1State.totalC = g1State.grid.flat().filter(x => x === 2).length;
    g1Draw();
}

function g1Draw() {
    const cvs = document.getElementById("g1Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"), cs = 60;
    ctx.clearRect(0, 0, 420, 420);
    const icons = {1:"🪨", 2:"💎", 3:"🛸", 5:"🔘", 6:"🌀"};
    for (let y = 0; y < 7; y++) {
        for (let x = 0; x < 7; x++) {
            const x1 = x * cs, y1 = y * cs, cell = g1State.grid[y][x];
            ctx.fillStyle = (cell === 4 && g1State.laserOn) ? "#3b1222" : ((x+y)%2===0 ? "#141827" : "#0e111d");
            ctx.fillRect(x1, y1, cs, cs);
            ctx.strokeStyle = "#232942"; ctx.strokeRect(x1, y1, cs, cs);
            ctx.font = "25px 'Segoe UI Emoji', sans-serif";
            ctx.textAlign = "center"; ctx.textBaseline = "middle";
            if (icons[cell]) ctx.fillText(icons[cell], x1+30, y1+30);
            else if (cell === 4 && g1State.laserOn) ctx.fillText("⚡", x1+30, y1+30);
        }
    }
    const rx = g1State.rx * cs + 30, ry = g1State.ry * cs + 30;
    ctx.beginPath(); ctx.arc(rx, ry, 20, 0, Math.PI*2);
    ctx.fillStyle = "#29b6f6"; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#fff"; ctx.stroke();
    ctx.font = "21px 'Segoe UI Emoji', sans-serif"; ctx.fillText("🤖", rx, ry);
    const dirs = [[0,-1],[1,0],[0,1],[-1,0]], arrs = ["▲","▶","▼","◀"];
    const [dx, dy] = dirs[g1State.rdir];
    ctx.beginPath(); ctx.arc(rx+dx*21, ry+dy*21, 8, 0, Math.PI*2);
    ctx.fillStyle = "#ff4081"; ctx.fill();
    ctx.font = "bold 10px Consolas"; ctx.fillStyle = "#fff";
    ctx.fillText(arrs[g1State.rdir], rx+dx*21, ry+dy*21);
}

function g1Add(c) { if (!g1State.timer && g1State.cmds.length < 24) { g1State.cmds.push(c); g1RenderCmds(-1); } }
function g1Pop() { if (!g1State.timer && g1State.cmds.length > 0) { g1State.cmds.pop(); g1RenderCmds(-1); } }
function g1Clear() { if (!g1State.timer) { g1State.cmds = []; g1ResetBoard(); g1RenderCmds(-1); } }

function g1RenderCmds(actIdx) {
    const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
    const opt = G1_LEVELS[appState.currentLevel].opt;
    document.getElementById("g1CmdHeader").innerText = `📋 有效積木：${eff} 個 (目標：${opt} 個)`;
    let html = "", py = ["# 🚀 星際編碼號 Python 腳本", "import space_bot as bot\n"], ind = 0;
    const m = { MOVE:["⬆️ 前進","bot.move()"], LEFT:["↩️ 左轉","bot.turn_left()"], RIGHT:["↪️ 右轉","bot.turn_right()"], SWITCH:["👆 開關","bot.trigger_switch()"] };
    g1State.cmds.forEach((c, i) => {
        const cls = (i === actIdx) ? "cmd-item running" : "cmd-item";
        if (c === "END_LOOP") { ind = Math.max(0, ind-1); html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}🔚 結束重複</div>`; }
        else if (c.startsWith("LOOP_")) {
            const n = c.split("_")[1];
            html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}🔄 重複 ${n} 次:</div>`;
            py.push(`${"    ".repeat(ind)}for _ in range(${n}):`); ind++;
        } else {
            html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}${m[c][0]}</div>`;
            py.push(`${"    ".repeat(ind)}${m[c][1]}`);
        }
    });
    document.getElementById("g1CmdList").innerHTML = html || "<div style='color:#607d8b;'>尚未加入指令...</div>";
    updatePythonBox(py.join("\n"), "使用 <code>for _ in range(N):</code> 迴圈能把重複的路線濃縮成幾行程式碼，輕鬆拿下 3 星！");
}

function g1Compile(cmds) {
    function parse(i) {
        let out = [];
        while (i < cmds.length) {
            const c = cmds[i];
            if (c === "END_LOOP") return [out, i+1];
            if (c.startsWith("LOOP_")) {
                const n = parseInt(c.split("_")[1]);
                const [sub, nxt] = parse(i+1);
                for (let k = 0; k < n; k++) out.push(...sub);
                i = nxt;
            } else { out.push({act:c, line:i}); i++; }
        }
        return [out, i];
    }
    return parse(0)[0];
}

function g1Run() {
    if (g1State.timer || !g1State.cmds.length) return;
    g1ResetBoard();
    const q = g1Compile(g1State.cmds); if (!q.length) return;
    let idx = 0;
    function step() {
        if (idx >= q.length) {
            g1State.timer = null; g1RenderCmds(-1);
            if (g1State.grid[g1State.ry][g1State.rx] === 3 && g1State.gotC === g1State.totalC) {
                const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
                const opt = G1_LEVELS[appState.currentLevel].opt;
                awardStars(0, appState.currentLevel, eff <= opt ? 3 : (eff <= opt+2 ? 2 : 1));
            } else document.getElementById("g1Status").innerText = "🤔 還沒收集完水晶或還沒抵達終點喔！";
            return;
        }
        const {act, line} = q[idx]; g1RenderCmds(line);
        const dirs = [[0,-1],[1,0],[0,1],[-1,0]];
        if (act === "LEFT") g1State.rdir = (g1State.rdir + 3) % 4;
        else if (act === "RIGHT") g1State.rdir = (g1State.rdir + 1) % 4;
        else if (act === "SWITCH") { if (g1State.grid[g1State.ry][g1State.rx] === 5) g1State.laserOn = !g1State.laserOn; }
        else if (act === "MOVE") {
            const [dx, dy] = dirs[g1State.rdir], nx = g1State.rx + dx, ny = g1State.ry + dy;
            if (nx<0 || nx>=7 || ny<0 || ny>=7 || g1State.grid[ny][nx]===1 || (g1State.grid[ny][nx]===4 && g1State.laserOn)) {
                g1State.timer = null; document.getElementById("g1Status").innerText = "💥 撞上隕石或雷射了！請修改積木。"; return;
            }
            g1State.rx = nx; g1State.ry = ny;
            if (g1State.grid[ny][nx] === 2) { g1State.grid[ny][nx] = 0; g1State.gotC++; }
            else if (g1State.grid[ny][nx] === 6) {
                outer: for (let py=0; py<7; py++) for (let px=0; px<7; px++) {
                    if (g1State.grid[py][px] === 6 && (px !== nx || py !== ny)) { g1State.rx = px; g1State.ry = py; break outer; }
                }
            }
        }
        g1Draw(); idx++; g1State.timer = setTimeout(step, 330);
    }
    step();
}

// --- 遊戲 2：光子邏輯閘 ---
let g2State = { inVals: [0,0,0,0], clicks: 0, finalOut: 0 };

function initGame2(lIdx) {
    if (lIdx === 20 && appState.customLevels.g2) G2_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g2));
    const lvl = G2_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `⚡ ${lvl.name}`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g2State.inVals = [0,0,0,0]; g2State.clicks = 0;
    document.getElementById("stageContent").innerHTML = `<div style="text-align:center;">
        <canvas id="g2Canvas" width="700" height="380"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-top:8px; gap:8px;">
            <div style="font-size:0.84rem; color:#4dd0e1;">💡 【AND】全1才1 ｜ 【OR】有1就1 ｜ 【XOR】不同才1 ｜ 【NAND】不全1就1 ｜ 【NOR】全0才1</div>
            <button class="cmd-btn" style="background:#69f0ae; padding:9px 20px; font-size:0.95rem;" onclick="g2CheckWin()">✅ 驗證並啟動核心</button>
        </div>
    </div>`;
    document.getElementById("g2Canvas").addEventListener("click", g2CanvasClick);
    g2EvalAndDraw();
}

function g2Calc(t, a, b) {
    if (t === "AND") return a & b;
    if (t === "OR") return a | b;
    if (t === "XOR") return a ^ b;
    if (t === "NAND") return 1 - (a & b);
    if (t === "NOR") return (a === 0 && b === 0) ? 1 : 0;
    return a;
}

function g2EvalAndDraw() {
    const lvl = G2_LEVELS[appState.currentLevel], [A,B,C,D] = g2State.inVals;
    const out1 = g2Calc(lvl.g1, A, B);
    const out2 = (lvl.ins === 4) ? g2Calc(lvl.g2, C, D) : 0;
    const finalOut = (lvl.ins === 4) ? g2Calc(lvl.g3, out1, out2) : out1;
    g2State.finalOut = finalOut;

    const cvs = document.getElementById("g2Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"); ctx.clearRect(0, 0, 700, 380);
    const ys = (lvl.ins === 4) ? [70, 150, 235, 315] : [125, 255];

    function wire(x1, y1, x2, y2, v) {
        ctx.strokeStyle = v ? "#69f0ae" : "#37474f"; ctx.lineWidth = v ? 5 : 3;
        const mx = (x1+x2)/2; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(mx,y1); ctx.lineTo(mx,y2); ctx.lineTo(x2,y2); ctx.stroke();
    }
    function gate(x, y, w, h, t, v) {
        ctx.fillStyle = v ? "#1e88e5" : "#263238"; ctx.strokeStyle = v ? "#69f0ae" : "#90a4ae"; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.roundRect(x, y, w, h, 10); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#fff"; ctx.font = "bold 14px 'Microsoft JhengHei'"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(`${t} 閘`, x+w/2, y+h/2-9);
        ctx.fillStyle = v ? "#ffd54f" : "#b0bec5"; ctx.fillText(`OUT=${v}`, x+w/2, y+h/2+11);
    }

    if (lvl.ins === 2) {
        wire(145, 125, 280, 175, A); wire(145, 255, 280, 205, B);
        gate(280, 145, 125, 85, lvl.g1, out1); wire(405, 190, 545, 190, finalOut);
    } else {
        wire(145, 70, 245, 100, A); wire(145, 150, 245, 125, B); gate(245, 70, 115, 75, lvl.g1, out1);
        wire(145, 235, 245, 265, C); wire(145, 315, 245, 290, D); gate(245, 235, 115, 75, lvl.g2, out2);
        wire(360, 108, 435, 175, out1); wire(360, 273, 435, 205, out2); gate(435, 152, 115, 75, lvl.g3, finalOut);
        wire(550, 190, 590, 190, finalOut);
    }

    for (let i = 0; i < lvl.ins; i++) {
        const y = ys[i], v = g2State.inVals[i];
        ctx.fillStyle = v ? "#69f0ae" : "#263238"; ctx.strokeStyle = "#fff"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.roundRect(25, y-22, 120, 44, 9); ctx.fill(); ctx.stroke();
        ctx.fillStyle = v ? "#111" : "#fff"; ctx.font = "bold 14px 'Microsoft JhengHei'";
        ctx.fillText(`開關 ${["A","B","C","D"][i]} = ${v}`, 85, y);
    }

    ctx.beginPath(); ctx.arc(635, 190, 42, 0, Math.PI*2);
    ctx.fillStyle = finalOut ? "#ffd54f" : "#263238"; ctx.fill();
    ctx.lineWidth = 4; ctx.strokeStyle = finalOut ? "#69f0ae" : "#546e7a"; ctx.stroke();
    ctx.fillStyle = finalOut ? "#111" : "#eceff4";
    ctx.fillText("🎯核心", 635, 180); ctx.fillText(`OUT=${finalOut}`, 635, 202);

    updatePythonBox(
        `# ⚡ 布林邏輯電路模擬\nA, B, C, D = ${A}, ${B}, ${C}, ${D}\ngate1 = calc_${lvl.g1}(A, B) # -> ${out1}\n` +
        (lvl.ins===4 ? `gate2 = calc_${lvl.g2}(C, D) # -> ${out2}\ncore  = calc_${lvl.g3}(gate1, gate2) # -> ${finalOut}` : `core  = gate1 # -> ${finalOut}`),
        "學會推演 <code>AND</code>、<code>OR</code>、<code>XOR</code>、<code>NAND</code>、<code>NOR</code> 真值表，能幫你寫出嚴密的程式條件判斷！"
    );
}

function g2CanvasClick(e) {
    const lvl = G2_LEVELS[appState.currentLevel], r = e.target.getBoundingClientRect();
    const x = (e.clientX - r.left) * (700 / r.width), y = (e.clientY - r.top) * (380 / r.height);
    const ys = (lvl.ins === 4) ? [70, 150, 235, 315] : [125, 255];
    for (let i = 0; i < lvl.ins; i++) {
        if (x >= 25 && x <= 145 && y >= ys[i]-22 && y <= ys[i]+22) {
            g2State.inVals[i] = 1 - g2State.inVals[i]; g2State.clicks++; g2EvalAndDraw(); return;
        }
    }
    if (appState.currentLevel === 20) {
        const ts = ["AND","OR","XOR","NAND","NOR"];
        if (x>=245 && x<=360 && y>=70 && y<=145) lvl.g1 = ts[(ts.indexOf(lvl.g1)+1)%5];
        else if (x>=245 && x<=360 && y>=235 && y<=310) lvl.g2 = ts[(ts.indexOf(lvl.g2)+1)%5];
        else if (x>=435 && x<=550 && y>=152 && y<=227) lvl.g3 = ts[(ts.indexOf(lvl.g3)+1)%5];
        appState.customLevels.g2 = JSON.parse(JSON.stringify(lvl)); saveProgress(); g2EvalAndDraw();
    }
}

function g2CheckWin() {
    const lvl = G2_LEVELS[appState.currentLevel];
    if (g2State.finalOut !== 1) return alert("⚠️ 右側的能量核心目前還是 0（未啟動）喔！");
    const cnt = g2State.inVals.slice(0, lvl.ins).reduce((a,b)=>a+b, 0);
    if (lvl.rule === "EXACT_1" && cnt !== 1) return alert(`限制：必須剛好開啟 1 個開關（目前 ${cnt} 個）！`);
    if (lvl.rule === "EXACT_2" && cnt !== 2) return alert(`限制：必須剛好開啟 2 個開關（目前 ${cnt} 個）！`);
    if (lvl.rule === "EXACT_3" && cnt !== 3) return alert(`限制：必須剛好開啟 3 個開關（目前 ${cnt} 個）！`);
    if (lvl.rule === "AT_LEAST_1" && cnt < 1) return alert("限制：至少開啟 1 個開關！");
    if (lvl.rule === "MAX_3" && cnt > 3) return alert("限制：最多開啟 3 個開關！");
    if (appState.currentLevel === 14 && g2State.inVals[0] !== 1) return alert("限制：開關 A 必須開啟！");
    awardStars(1, appState.currentLevel, g2State.clicks <= 4 ? 3 : (g2State.clicks <= 7 ? 2 : 1));
}

// --- 遊戲 3：能量排序室 ---
let g3State = { arr: [], sel: null, swaps: 0 };

function initGame3(lIdx) {
    if (lIdx === 20 && appState.customLevels.g3) G3_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g3));
    const lvl = G3_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `⚖️ ${lvl.name} 【⭐⭐⭐ 黃金目標：${lvl.opt} 次交換內】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g3State.arr = [...lvl.arr]; g3State.sel = null; g3State.swaps = 0;

    const customHtml = (lIdx === 20) ? `<div class="brush-bar">
        <input id="g3CustomIn" value="${lvl.arr.join(' ')}" style="background:#090b10; color:#fff; border:1px solid #4dd0e1; border-radius:6px; padding:4px 8px; width:160px;">
        <button class="brush-btn active" onclick="g3ApplyCustom()">套用數列</button>
        <button class="brush-btn" onclick="g3ToggleAdj()">相鄰限制: ${lvl.adj?'開':'關'}</button>
    </div>` : "";

    document.getElementById("stageContent").innerHTML = `<div style="text-align:center;">
        <canvas id="g3Canvas" width="700" height="340"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
            <div class="status-bar" id="g3Status" style="margin:0;">已交換：0 次 （點擊兩瓶能量管交換位置）</div>
            <button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="initGame3(${lIdx})">🔄 重置</button>
        </div>
        ${customHtml}
    </div>`;
    document.getElementById("g3Canvas").addEventListener("click", g3CanvasClick);
    g3Draw("# 尚未執行交換");
}

function g3ApplyCustom() {
    const raw = document.getElementById("g3CustomIn").value.trim().split(/\s+/).map(Number).filter(n => n>=5 && n<=99).slice(0,8);
    if (raw.length >= 3) { G3_LEVELS[20].arr = raw; appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20])); saveProgress(); initGame3(20); }
}
function g3ToggleAdj() { G3_LEVELS[20].adj = !G3_LEVELS[20].adj; appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20])); saveProgress(); initGame3(20); }

function g3GetTarget() {
    const lvl = G3_LEVELS[appState.currentLevel], b = [...lvl.arr];
    if (lvl.mode === "ASC") return b.sort((x,y)=>x-y);
    if (lvl.mode === "DESC") return b.sort((x,y)=>y-x);
    if (lvl.mode === "EVEN_ODD") return [...b.filter(x=>x%2===0).sort((x,y)=>x-y), ...b.filter(x=>x%2!==0).sort((x,y)=>x-y)];
    if (lvl.mode === "MOUNTAIN") return [10, 30, 50, 40, 20];
    if (lvl.mode === "VALLEY") return [50, 30, 10, 20, 40];
    if (lvl.mode === "ZIGZAG") return [20, 10, 40, 30, 50];
    return b.sort((x,y)=>x-y);
}

function g3Draw(code) {
    const cvs = document.getElementById("g3Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"); ctx.clearRect(0, 0, 700, 340);
    const n = g3State.arr.length, w = Math.floor(620 / n), sx = 40 + Math.floor((620 - w*n)/2);
    const target = g3GetTarget(), maxV = Math.max(...g3State.arr, 1);

    ctx.fillStyle = "#69f0ae"; ctx.font = "bold 14px Consolas"; ctx.textAlign = "center";
    ctx.fillText(`🎯 目標排列：[ ${target.join(", ")} ]`, 350, 24);

    g3State.arr.forEach((v, i) => {
        const x1 = sx + i*w + 10, bw = w - 20, bh = Math.floor((v/maxV)*185) + 35, y2 = 290, y1 = y2 - bh;
        const isSel = (g3State.sel === i), isOk = (v === target[i]);
        ctx.fillStyle = isSel ? "#ffd54f" : (isOk ? "#00e676" : "#29b6f6");
        ctx.strokeStyle = isSel ? "#fff" : "#90caf9"; ctx.lineWidth = isSel ? 3 : 1.5;
        ctx.beginPath(); ctx.roundRect(x1, y1, bw, bh, 8); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#fff"; ctx.font = "bold 15px Consolas"; ctx.fillText(String(v), x1+bw/2, y1-12);
        ctx.fillStyle = "#4dd0e1"; ctx.font = "bold 12px sans-serif"; ctx.fillText(`[${i}]`, x1+bw/2, y2+20);
    });
    updatePythonBox(`# ⚖️ 陣列排序演算法\npotions = [${g3State.arr.join(", ")}]\ntarget  = [${target.join(", ")}]\n\n${code}`, "Python 交換陣列元素只需一行：<code>a[i], a[j] = a[j], a[i]</code>！");
}

function g3CanvasClick(e) {
    const r = e.target.getBoundingClientRect(), x = (e.clientX - r.left) * (700 / r.width);
    const n = g3State.arr.length, w = Math.floor(620 / n), sx = 40 + Math.floor((620 - w*n)/2);
    const idx = Math.floor((x - sx) / w); if (idx < 0 || idx >= n) return;
    if (g3State.sel === null) { g3State.sel = idx; g3Draw(`# 選取 potions[${idx}]`); }
    else if (g3State.sel === idx) { g3State.sel = null; g3Draw("# 取消選取"); }
    else {
        const i = g3State.sel, j = idx, lvl = G3_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(i - j) !== 1) { alert("⚠️ 本關限制只能交換相鄰的兩瓶喔！"); g3State.sel = null; g3Draw("# 違反相鄰限制"); return; }
        const tmp = g3State.arr[i]; g3State.arr[i] = g3State.arr[j]; g3State.arr[j] = tmp;
        g3State.swaps++; g3State.sel = null;
        document.getElementById("g3Status").innerText = `已交換：${g3State.swaps} 次`;
        g3Draw(`potions[${i}], potions[${j}] = potions[${j}], potions[${i}]`);
        const t = g3GetTarget();
        if (g3State.arr.every((v, k) => v === t[k])) awardStars(2, appState.currentLevel, g3State.swaps <= lvl.opt ? 3 : (g3State.swaps <= lvl.opt+2 ? 2 : 1));
    }
}

// --- 遊戲 4：星際河內塔 ---
let g4State = { pegs: [], sel: null, moves: 0, totalDisks: 0 };

function initGame4(lIdx) {
    if (lIdx === 20 && appState.customLevels.g4) G4_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g4));
    const lvl = G4_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🗼 ${lvl.name} 【⭐⭐⭐ 黃金目標：${lvl.opt} 步內】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g4State.pegs = JSON.parse(JSON.stringify(lvl.pegs)); g4State.sel = null; g4State.moves = 0;
    g4State.totalDisks = g4State.pegs.flat().length;

    const customHtml = (lIdx === 20) ? `<div class="brush-bar">
        <button class="brush-btn" onclick="g4Custom(2,null)">2環</button>
        <button class="brush-btn" onclick="g4Custom(3,null)">3環</button>
        <button class="brush-btn" onclick="g4Custom(4,null)">4環</button>
        <button class="brush-btn" onclick="g4Custom(5,null)">5環</button>
        <button class="brush-btn" onclick="g4Custom(null,'PEGS')">3柱/4柱</button>
        <button class="brush-btn" onclick="g4Custom(null,'ADJ')">相鄰限制</button>
    </div>` : "";

    document.getElementById("stageContent").innerHTML = `<div style="text-align:center;">
        <canvas id="g4Canvas" width="700" height="340"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
            <div class="status-bar" id="g4Status" style="margin:0;">步數：0 步 （點擊來源柱取出頂端環，再點目標柱放入）</div>
            <button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="initGame4(${lIdx})">🔄 重置</button>
        </div>
        ${customHtml}
    </div>`;
    document.getElementById("g4Canvas").addEventListener("click", g4CanvasClick);
    g4Draw("# 點擊柱子進行 pop() 與 append()");
}

function g4Custom(nD, tType) {
    const lvl = G4_LEVELS[20];
    let curN = nD || lvl.pegs.flat().length, pC = lvl.pegs.length;
    if (tType === "PEGS") pC = (pC === 3) ? 4 : 3;
    if (tType === "ADJ") lvl.adj = !lvl.adj;
    lvl.pegs = [Array.from({length:curN},(_,i)=>curN-i), ...Array.from({length:pC-1},()=>[])];
    lvl.target = pC - 1; lvl.opt = (pC === 3) ? (Math.pow(2,curN)-1) : (curN*2+1);
    appState.customLevels.g4 = JSON.parse(JSON.stringify(lvl)); saveProgress(); initGame4(20);
}

function g4Draw(code) {
    const cvs = document.getElementById("g4Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"); ctx.clearRect(0, 0, 700, 340);
    const lvl = G4_LEVELS[appState.currentLevel], numP = g4State.pegs.length, sp = Math.floor(700 / numP);
    const cols = ["#ff80ab","#ffb74d","#ffd54f","#69f0ae","#64b5f6","#b388ff"], pN = ["A 柱","B 柱","C 柱","D 柱"];

    g4State.pegs.forEach((st, idx) => {
        const cx = sp * idx + sp / 2, isSel = (g4State.sel === idx), isT = (idx === lvl.target);
        ctx.fillStyle = isT ? "#69f0ae" : "#455a64"; ctx.fillRect(cx-65, 290, 130, 12);
        ctx.fillStyle = isSel ? "#ffd54f" : "#37474f"; ctx.fillRect(cx-6, 90, 12, 200);
        ctx.fillStyle = isT ? "#69f0ae" : "#eceff4"; ctx.font = "bold 13px sans-serif"; ctx.textAlign = "center";
        ctx.fillText(isT ? `🎯 ${pN[idx]}(終點)` : pN[idx], cx, 320);

        st.forEach((d, sPos) => {
            const w = 20 + d * 14, y2 = 288 - sPos * 30 - (isSel && sPos === st.length-1 ? 18 : 0);
            ctx.fillStyle = cols[(d-1)%cols.length]; ctx.strokeStyle = "#fff"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.roundRect(cx-w, y2-26, w*2, 26, 7); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "#111"; ctx.font = "bold 12px sans-serif"; ctx.fillText(`環 ${d}`, cx, y2-13);
        });
    });
    const pV = g4State.pegs.map((s,i)=>`stack_${["A","B","C","D"][i]} = [${s.join(", ")}]`).join("\n");
    updatePythonBox(`# 🗼 堆疊 (Stack) 與遞迴\n${pV}\n\n${code}`, "柱子就是 <b>Stack（後進先出）</b>：只能從頂端 <code>pop()</code> 取出或 <code>append()</code> 放入！");
}

function g4CanvasClick(e) {
    const r = e.target.getBoundingClientRect(), x = (e.clientX - r.left) * (700 / r.width);
    const numP = g4State.pegs.length, idx = Math.floor(x / (700 / numP));
    if (idx < 0 || idx >= numP) return;
    if (g4State.sel === null) { if (g4State.pegs[idx].length) { g4State.sel = idx; g4Draw(`# 選取柱 ${idx}`); } }
    else if (g4State.sel === idx) { g4State.sel = null; g4Draw("# 取消選取"); }
    else {
        const src = g4State.sel, dst = idx, lvl = G4_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(src - dst) !== 1) { alert("⚠️ 本關限制只能移到隔壁相鄰的柱子喔！"); g4State.sel = null; g4Draw("# 違反相鄰限制"); return; }
        const disk = g4State.pegs[src][g4State.pegs[src].length-1], top = g4State.pegs[dst][g4State.pegs[dst].length-1];
        if (top !== undefined && top < disk) { alert("⚠️ 大環不能壓在小環上面喔！"); g4State.sel = null; g4Draw("# 違反大小規則"); return; }
        g4State.pegs[src].pop(); g4State.pegs[dst].push(disk); g4State.moves++; g4State.sel = null;
        document.getElementById("g4Status").innerText = `步數：${g4State.moves} 步`;
        const pL = ["A","B","C","D"]; g4Draw(`d = stack_${pL[src]}.pop()\nstack_${pL[dst]}.append(d)`);
        if (g4State.pegs[lvl.target].length === g4State.totalDisks) awardStars(3, appState.currentLevel, g4State.moves <= lvl.opt ? 3 : (g4State.moves <= lvl.opt+4 ? 2 : 1));
    }
}

// --- 遊戲 5：像素解碼器 ---
let g5State = { target: [], player: [], editTarget: false, mistakes: 0 };

function initGame5(lIdx) {
    if (lIdx === 20 && appState.customLevels.g5) G5_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g5));
    const lvl = G5_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🎨 ${lvl.name} 【二進位權重與 2D 矩陣解碼】`;
    document.getElementById("lvlDesc").innerText = "根據上方「連續亮格數」與右側「二進位加總密碼 (32, 16, 8, 4, 2, 1)」，點擊格子切換 0 與 1！";
    g5State.target = lvl.grid.map(r => r.split("").map(Number));
    g5State.player = Array.from({length:6}, ()=>[0,0,0,0,0,0]);
    g5State.editTarget = false; g5State.mistakes = 0;

    const customBtn = (lIdx === 20) ? `<button class="cmd-btn" id="g5CreatorBtn" style="background:#ff80ab; padding:7px 14px;" onclick="g5ToggleCreator()">🎨 繪製自訂謎題</button>` : "";
    document.getElementById("stageContent").innerHTML = `<div style="text-align:center;">
        <canvas id="g5Canvas" width="700" height="375"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
            <div class="status-bar" style="margin:0;">💡 密碼完全吻合時會變成綠色 ✅！</div>
            <div style="display:flex; gap:6px;">${customBtn}<button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="initGame5(${lIdx})">🗑️ 清空</button></div>
        </div>
    </div>`;
    document.getElementById("g5Canvas").addEventListener("click", g5CanvasClick);
    g5Draw();
}

function g5ToggleCreator() {
    g5State.editTarget = !g5State.editTarget;
    const b = document.getElementById("g5CreatorBtn");
    if (g5State.editTarget) { b.innerText = "🔒 鎖定並開始解謎"; b.style.background = "#69f0ae"; }
    else {
        G5_LEVELS[20].grid = g5State.target.map(r => r.join(""));
        appState.customLevels.g5 = JSON.parse(JSON.stringify(G5_LEVELS[20])); saveProgress();
        g5State.player = Array.from({length:6}, ()=>[0,0,0,0,0,0]);
        b.innerText = "🎨 繪製自訂謎題"; b.style.background = "#ff80ab";
    }
    g5Draw();
}

function g5RLE(arr) {
    let res = [], c = 0;
    arr.forEach(v => { if (v===1) c++; else if (c>0) { res.push(c); c=0; } });
    if (c>0) res.push(c);
    return res.length ? res.join(" ") : "0";
}

function g5Draw() {
    const cvs = document.getElementById("g5Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"); ctx.clearRect(0, 0, 700, 375);
    const ox = 160, oy = 72, cs = 48, board = g5State.editTarget ? g5State.target : g5State.player, wts = [32,16,8,4,2,1];

    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    for (let c = 0; c < 6; c++) {
        const cx = ox + c*cs + cs/2, tC = g5State.target.map(r=>r[c]), pC = board.map(r=>r[c]);
        ctx.fillStyle = tC.every((v,i)=>v===pC[i]) ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 12px sans-serif"; ctx.fillText("連續:"+g5RLE(tC), cx, 24);
        ctx.fillStyle = "#ffd54f"; ctx.font = "bold 12px Consolas"; ctx.fillText(`(${wts[c]})`, cx, 52);
    }

    for (let r = 0; r < 6; r++) {
        const ry = oy + r*cs + cs/2, tR = g5State.target[r], pR = board[r];
        const tD = tR.reduce((a,v,i)=>a+v*wts[i],0), pD = pR.reduce((a,v,i)=>a+v*wts[i],0);
        ctx.textAlign = "right"; ctx.fillStyle = tR.every((v,i)=>v===pR[i]) ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 12px sans-serif"; ctx.fillText(`列[${r}] 連續: ${g5RLE(tR)}`, ox-10, ry);

        ctx.textAlign = "left"; ctx.fillStyle = (tD===pD) ? "#69f0ae" : "#ffd54f";
        ctx.font = "bold 13px Consolas"; ctx.fillText(`${tD===pD?'✅':'👉'} 密碼:${String(tD).padStart(2,' ')} (目前:${String(pD).padStart(2,' ')})`, ox+6*cs+12, ry);

        ctx.textAlign = "center";
        for (let c = 0; c < 6; c++) {
            const x1 = ox + c*cs, y1 = oy + r*cs, v = board[r][c];
            ctx.fillStyle = v ? (g5State.editTarget ? "#ff80ab" : "#29b6f6") : "#161925";
            ctx.strokeStyle = "#37474f"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.roundRect(x1+2, y1+2, cs-4, cs-4, 6); ctx.fill(); ctx.stroke();
            ctx.fillStyle = v ? "#111" : "#546e7a"; ctx.font = "bold 15px Consolas"; ctx.fillText(String(v), x1+cs/2, y1+cs/2);
        }
    }
    const r0 = board[0], d0 = r0.reduce((a,v,i)=>a+v*wts[i],0);
    updatePythonBox(`# 🎨 二維陣列與二進位\nmatrix = [\n${board.map(r=>`  [${r.join(", ")}],`).join("\n")}\n]\nrow0_dec = int("${r0.join("")}", 2) # = ${d0}`, "6 位元二進位權重由左至右為 <code>32, 16, 8, 4, 2, 1</code>，把亮起格子的權重加起來就是十進位密碼！");
}

function g5CanvasClick(e) {
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (700 / rect.width), y = (e.clientY - rect.top) * (375 / rect.height);
    const c = Math.floor((x - 160) / 48), r = Math.floor((y - 72) / 48);
    if (r < 0 || r >= 6 || c < 0 || c >= 6) return;
    if (g5State.editTarget) { g5State.target[r][c] = 1 - g5State.target[r][c]; g5Draw(); return; }
    g5State.player[r][c] = 1 - g5State.player[r][c];
    if (g5State.player[r][c] === 1 && g5State.target[r][c] === 0) g5State.mistakes++;
    g5Draw();
    if (g5State.player.every((row, ri) => row.every((v, ci) => v === g5State.target[ri][ci]))) {
        awardStars(4, appState.currentLevel, g5State.mistakes <= 2 ? 3 : (g5State.mistakes <= 6 ? 2 : 1));
    }
}

loadSaveData();
switchGame(0);
</script>
</body>
</html>'''

components.html(GAME_HTML, height=800, scrolling=True)
# === 檔案結束 (請確認複製到此行) ===
