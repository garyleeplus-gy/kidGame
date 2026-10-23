import sys
import os
import subprocess

# ==============================================================================
# 自動環境檢查與啟動器：
# 支援直接執行 `python app.py` (自動安裝並啟動 Streamlit) 或 `streamlit run app.py`
# ==============================================================================
def ensure_streamlit_and_launch():
    try:
        import streamlit as st
    except ImportError:
        print("正在為您自動安裝 streamlit 套件，請稍候...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        import streamlit as st

    # 檢查是否已經在 Streamlit 執行環境中
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

# 設定頁面支援寬螢幕與行動裝置自適應
st.set_page_config(
    page_title="星際邏輯學院 | 105關卡運算思維遊戲",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隱藏 Streamlit 預設多餘邊距，讓手機與電腦畫面最大化
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 側邊欄：家長與教師說明及雲端備份指南
with st.sidebar:
    st.markdown("## 🌌 星際邏輯學院 2.0")
    st.markdown("""
    **五大運算思維訓練 × 各 20 關 + 自製沙盒**
    - 🚀 **星際編碼號**：序列、迴圈、條件與蟲洞
    - ⚡ **光子邏輯閘**：AND / OR / XOR / NAND / NOR
    - ⚖️ **能量排序室**：選擇、泡泡、奇偶與山峰排序
    - 🗼 **星際河內塔**：Stack 堆疊與遞迴拆解
    - 🎨 **像素解碼器**：二進位權重與 2D 矩陣推理
    ---
    ### 📱 手機與平板操作提示
    1. 可使用遊戲頂部的 **「🔍 畫面縮放滑桿」** 隨時放大縮小畫布。
    2. 系統會在瀏覽器中 **自動存檔**；若要換手機或電腦玩，請點擊遊戲右上角 **「💾 存檔管理」** 匯出 `.json` 檔案或複製通行碼！
    """)

# ==============================================================================
# 內嵌完整響應式 HTML5 + Canvas + SVG 互動遊戲引擎 (含 105 關卡與三重存檔系統)
# ==============================================================================
GAME_HTML = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style>
    :root {
        --bg-dark: #0f111a;
        --bg-panel: rgba(24, 27, 40, 0.92);
        --bg-card: #23273a;
        --accent-blue: #64b5f6;
        --accent-cyan: #4dd0e1;
        --accent-green: #69f0ae;
        --accent-gold: #ffd54f;
        --accent-pink: #ff80ab;
        --accent-purple: #b388ff;
        --text-main: #eceff4;
        --text-sub: #b0bec5;
    }
    * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }
    body {
        margin: 0; padding: 8px;
        background: radial-gradient(circle at 20% 20%, #1a1f35 0%, #0b0d14 100%);
        color: var(--text-main);
        font-family: "Microsoft JhengHei", "PingFang TC", "Segoe UI", sans-serif;
        overflow-x: hidden;
    }
    /* 頂部主導覽列 */
    .top-header {
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        background: var(--bg-panel); border: 1px solid rgba(100,181,246,0.3);
        border-radius: 14px; padding: 10px 14px; margin-bottom: 8px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.4);
        gap: 8px;
    }
    .brand-title {
        font-size: 1.25rem; font-weight: 900;
        background: linear-gradient(90deg, #ffd54f, #4dd0e1, #ff80ab);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        display: flex; align-items: center; gap: 6px;
    }
    .nav-tabs {
        display: flex; flex-wrap: wrap; gap: 6px;
    }
    .nav-btn {
        background: var(--bg-card); color: var(--text-main);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
        padding: 7px 11px; font-size: 0.88rem; font-weight: bold;
        cursor: pointer; transition: all 0.2s;
    }
    .nav-btn:hover { transform: translateY(-2px); border-color: var(--accent-cyan); }
    .nav-btn.active {
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #111; border-color: #fff; box-shadow: 0 0 12px rgba(255,213,79,0.5);
    }
    .header-controls {
        display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    }
    .star-badge {
        background: rgba(105,240,174,0.15); border: 1px solid var(--accent-green);
        color: var(--accent-green); padding: 5px 12px; border-radius: 20px;
        font-weight: bold; font-size: 0.9rem;
    }
    .tool-btn {
        background: #37474f; color: #fff; border: 1px solid var(--accent-cyan);
        padding: 5px 10px; border-radius: 8px; cursor: pointer; font-size: 0.85rem; font-weight: bold;
    }
    .tool-btn:hover { background: var(--accent-cyan); color: #111; }

    /* 20+1 關卡選擇捲軸列 */
    .level-bar {
        display: flex; align-items: center; gap: 5px; overflow-x: auto;
        background: var(--bg-panel); padding: 8px 12px; border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08); margin-bottom: 10px;
        scrollbar-width: thin;
    }
    .lvl-btn {
        flex: 0 0 auto; background: var(--bg-card); color: var(--text-sub);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
        padding: 5px 9px; font-size: 0.82rem; font-weight: bold; cursor: pointer;
        transition: 0.15s;
    }
    .lvl-btn.active {
        background: var(--accent-blue); color: #000; border-color: #fff;
        box-shadow: 0 0 10px rgba(100,181,246,0.6);
    }
    .lvl-btn.custom {
        background: linear-gradient(135deg, #ff80ab, #f50057); color: #fff;
    }
    .lvl-btn.custom.active {
        border: 2px solid #ffd54f; box-shadow: 0 0 12px #ff80ab;
    }

    /* 主雙欄響應式網格 (電腦左右分欄，手機自動上下堆疊) */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 360px;
        gap: 12px;
        transform-origin: top center;
        transition: transform 0.15s ease;
    }
    @media (max-width: 960px) {
        .main-grid { grid-template-columns: 1fr; }
    }

    .stage-card, .code-card {
        background: var(--bg-panel); border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1); padding: 14px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.45);
    }
    .lvl-header-title {
        font-size: 1.2rem; font-weight: bold; color: var(--accent-gold); margin-bottom: 4px;
    }
    .lvl-header-desc {
        font-size: 0.92rem; color: var(--text-sub); margin-bottom: 10px; line-height: 1.4;
    }

    /* 遊戲畫布與控制區通用樣式 */
    .game-flex {
        display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-start; justify-content: center;
    }
    canvas {
        background: #0b0e17; border-radius: 14px;
        border: 2px solid rgba(100,181,246,0.35);
        box-shadow: inset 0 0 25px rgba(0,0,0,0.8), 0 4px 15px rgba(0,0,0,0.5);
        max-width: 100%; height: auto; touch-action: manipulation;
    }
    .control-box {
        flex: 1 1 250px; background: rgba(15,17,26,0.75);
        border-radius: 12px; padding: 12px; border: 1px solid rgba(255,255,255,0.08);
    }
    .block-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px;
    }
    .cmd-btn {
        border: none; border-radius: 8px; padding: 9px 8px;
        font-size: 0.9rem; font-weight: bold; cursor: pointer;
        color: #111; transition: transform 0.1s, filter 0.15s;
        display: flex; align-items: center; justify-content: center; gap: 4px;
    }
    .cmd-btn:active { transform: scale(0.95); }
    .cmd-btn:hover { filter: brightness(1.12); }

    .cmd-list {
        background: #090b10; border-radius: 8px; padding: 8px;
        height: 195px; overflow-y: auto; font-family: Consolas, monospace;
        font-size: 0.9rem; border: 1px solid #2c3146; margin-top: 6px;
    }
    .cmd-item { padding: 3px 6px; border-radius: 4px; margin-bottom: 2px; }
    .cmd-item.running { background: rgba(255, 128, 171, 0.35); border-left: 3px solid var(--accent-pink); color: #fff; }

    .status-banner {
        margin-top: 8px; padding: 8px 12px; border-radius: 8px;
        background: rgba(105,240,174,0.12); border-left: 4px solid var(--accent-green);
        font-weight: bold; font-size: 0.92rem; color: var(--accent-green);
    }

    /* 右側 Python 程式碼預覽區 */
    .code-box {
        background: #090b10; color: #69f0ae; font-family: "Consolas", monospace;
        font-size: 0.9rem; padding: 12px; border-radius: 10px;
        height: 310px; overflow-y: auto; white-space: pre-wrap;
        border: 1px solid #2e354d; line-height: 1.45;
    }
    .concept-box {
        margin-top: 10px; background: rgba(255,213,79,0.1);
        border: 1px solid rgba(255,213,79,0.4); border-radius: 10px;
        padding: 10px; font-size: 0.88rem; color: var(--accent-gold); line-height: 1.45;
    }

    /* 存檔與彈出視窗 Modal */
    .modal-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.75); z-index: 999; align-items: center; justify-content: center;
        padding: 16px;
    }
    .modal-box {
        background: #1a1e2e; border: 2px solid var(--accent-cyan);
        border-radius: 16px; max-width: 520px; width: 100%; padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8); text-align: center;
    }
    .brush-bar {
        display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px;
        background: rgba(255,255,255,0.06); padding: 8px; border-radius: 10px;
    }
    .brush-btn {
        background: #2c3146; color: #fff; border: 1px solid transparent;
        padding: 5px 8px; border-radius: 6px; cursor: pointer; font-size: 0.82rem;
    }
    .brush-btn.active { border-color: var(--accent-gold); background: #3f4765; }
</style>
</head>
<body>

<!-- 頂部導覽與控制列 -->
<div class="top-header">
    <div class="brand-title">🚀 星際邏輯學院 <span style="font-size:0.8rem; color:#4dd0e1;">Web 旗艦版 (105關)</span></div>
    <div class="nav-tabs" id="gameTabs">
        <button class="nav-btn active" onclick="switchGame(0)">1️⃣ 星際編碼號</button>
        <button class="nav-btn" onclick="switchGame(1)">2️⃣ 光子邏輯閘</button>
        <button class="nav-btn" onclick="switchGame(2)">3️⃣ 能量排序室</button>
        <button class="nav-btn" onclick="switchGame(3)">4️⃣ 星際河內塔</button>
        <button class="nav-btn" onclick="switchGame(4)">5️⃣ 像素解碼器</button>
    </div>
    <div class="header-controls">
        <div style="display:flex; align-items:center; gap:4px; font-size:0.82rem; color:#b0bec5;">
            🔍縮放:
            <input type="range" id="zoomSlider" min="65" max="135" value="100" style="width:75px;" oninput="applyZoom(this.value)">
            <span id="zoomVal">100%</span>
        </div>
        <div class="star-badge" id="totalStarsBadge">🏆 0 / 300 ⭐</div>
        <button class="tool-btn" onclick="openSaveModal()">💾 存檔管理</button>
    </div>
</div>

<!-- 20 關 + 自製關卡選擇列 -->
<div class="level-bar" id="levelBar"></div>

<!-- 主工作區 -->
<div class="main-grid" id="mainGrid">
    <div class="stage-card">
        <div class="lvl-header-title" id="lvlTitle">載入中...</div>
        <div class="lvl-header-desc" id="lvlDesc"></div>
        <div id="stageContent"></div>
    </div>
    <div class="code-card">
        <div style="font-size:1.05rem; font-weight:bold; color:#69f0ae; margin-bottom:6px;">
            🐍 即時 Python 演算法透視窗
        </div>
        <div style="font-size:0.82rem; color:#b0bec5; margin-bottom:8px;">
            你在畫面上的每一步操作，都會即時轉譯為真正的 Python 程式碼：
        </div>
        <div class="code-box" id="pythonPreview"></div>
        <div class="concept-box" id="conceptBox"></div>
    </div>
</div>

<!-- 過關慶祝與存檔管理彈跳視窗 -->
<div class="modal-overlay" id="modalOverlay">
    <div class="modal-box" id="modalContent"></div>
</div>

<!-- 慶祝紙花特效 Canvas -->
<canvas id="confettiCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:998; display:none;"></canvas>

<script>
// ============================================================================
// 全域狀態與三重存檔系統 (localStorage + JSON 下載上傳 + 存檔通行碼)
// ============================================================================
const STORAGE_KEY = "STAR_LOGIC_ACADEMY_SAVE_V2";
let appState = {
    currentGame: 0,
    currentLevel: 0,
    stars: {},        // key: "g_l" -> 1..3
    customLevels: {}  // 儲存玩家自訂的 5 款遊戲沙盒關卡
};

function loadSaveData() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const parsed = JSON.parse(raw);
            appState.stars = parsed.stars || {};
            appState.customLevels = parsed.customLevels || {};
        }
    } catch (e) { console.warn("讀取自動存檔失敗", e); }
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
    if (l < 20) {
        const k = `${g}_${l}`;
        appState.stars[k] = Math.max(appState.stars[k] || 0, s);
        saveProgress();
    }
    fireConfetti();
    const starIcons = "⭐".repeat(s);
    const nextBtnHtml = (l < 19)
        ? `<button class="cmd-btn" style="background:#69f0ae; padding:10px 20px; margin:8px;" onclick="closeModal(); loadLevel(${l+1});">⏩ 挑戰下一關 (第 ${l+2} 關)</button>`
        : `<button class="cmd-btn" style="background:#ff80ab; padding:10px 20px; margin:8px;" onclick="closeModal(); loadLevel(20);">🛠️ 前往自製創客關卡</button>`;

    showModal(`
        <h2 style="color:#ffd54f; margin-top:0;">🎉 任務大成功！</h2>
        <div style="font-size:2.5rem; margin:10px 0;">${starIcons}</div>
        <p style="color:#eceff4; font-size:1rem;">恭喜完成 <b>第 ${l+1} 關</b>！進度已自動儲存。</p>
        <div style="display:flex; justify-content:center; flex-wrap:wrap; margin-top:14px;">
            <button class="cmd-btn" style="background:#64b5f6; padding:10px 16px; margin:8px;" onclick="closeModal();">🔄 留在本關最佳化</button>
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

function applyZoom(val) {
    document.getElementById("zoomVal").innerText = val + "%";
    const grid = document.getElementById("mainGrid");
    grid.style.transform = `scale(${val / 100})`;
}

// ============================================================================
// 存檔管理彈窗 (匯出 JSON / 匯入 JSON / 複製通行碼)
// ============================================================================
function openSaveModal() {
    const saveStr = btoa(encodeURIComponent(JSON.stringify({
        stars: appState.stars,
        customLevels: appState.customLevels
    })));
    showModal(`
        <h3 style="color:#4dd0e1; margin-top:0;">💾 雲端與本地存檔管理中心</h3>
        <p style="font-size:0.88rem; color:#b0bec5; text-align:left;">
            ✅ <b>瀏覽器自動存檔已啟用</b>：你在本機或手機上的過關星章會自動保存。<br>
            📦 若要<b>跨裝置轉移進度</b>（如電腦轉到手機），可下載存檔或複製下方通行碼：
        </p>
        <div style="display:flex; gap:8px; justify-content:center; margin:12px 0; flex-wrap:wrap;">
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 14px;" onclick="downloadJsonSave()">⬇️ 下載 .json 存檔</button>
            <label class="cmd-btn" style="background:#64b5f6; padding:8px 14px; cursor:pointer;">
                📂 讀取 .json 存檔
                <input type="file" accept=".json" style="display:none;" onchange="uploadJsonSave(event)">
            </label>
            <button class="cmd-btn" style="background:#ff80ab; padding:8px 14px;" onclick="resetAllSave()">🗑️ 清空重來</button>
        </div>
        <div style="text-align:left; font-size:0.82rem; color:#ffd54f; margin-bottom:4px;">🔑 跨裝置存檔通行碼 (可複製貼上)：</div>
        <textarea id="saveCodeBox" style="width:100%; height:65px; background:#090b10; color:#69f0ae; border:1px solid #455a64; border-radius:6px; font-family:monospace; font-size:0.78rem; padding:6px;">${saveStr}</textarea>
        <div style="display:flex; gap:8px; justify-content:center; margin-top:10px;">
            <button class="cmd-btn" style="background:#ffd54f; padding:7px 14px;" onclick="importSaveCode()">📥 載入上方通行碼</button>
            <button class="cmd-btn" style="background:#b0bec5; padding:7px 14px;" onclick="closeModal()">關閉視窗</button>
        </div>
    `);
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
            alert("🎉 存檔讀取成功！");
        } catch (err) { alert("存檔格式錯誤！"); }
    };
    reader.readAsText(file);
}

function importSaveCode() {
    try {
        const raw = document.getElementById("saveCodeBox").value.trim();
        const data = JSON.parse(decodeURIComponent(atob(raw)));
        if (data.stars) appState.stars = data.stars;
        if (data.customLevels) appState.customLevels = data.customLevels;
        saveProgress();
        loadLevel(appState.currentLevel);
        closeModal();
        alert("🎉 通行碼載入成功！");
    } catch (e) { alert("通行碼無效，請確認是否完整複製！"); }
}

function resetAllSave() {
    if (confirm("確定要清空所有星章紀錄嗎？")) {
        appState.stars = {};
        appState.customLevels = {};
        saveProgress();
        loadLevel(appState.currentLevel);
        closeModal();
    }
}

function showModal(html) {
    document.getElementById("modalContent").innerHTML = html;
    document.getElementById("modalOverlay").style.display = "flex";
}
function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
}

// 紙花慶祝動畫
function fireConfetti() {
    const cvs = document.getElementById("confettiCanvas");
    cvs.style.display = "block";
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    const ctx = cvs.getContext("2d");
    const pieces = Array.from({length: 75}, () => ({
        x: Math.random() * cvs.width,
        y: Math.random() * cvs.height - cvs.height,
        vx: (Math.random() - 0.5) * 6,
        vy: Math.random() * 5 + 4,
        c: ["#ffd54f","#69f0ae","#64b5f6","#ff80ab","#b388ff"][Math.floor(Math.random()*5)],
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
        if (frames < 75) requestAnimationFrame(step);
        else cvs.style.display = "none";
    }
    step();
}

// ============================================================================
// 資料庫：5 款遊戲 × 各 20 關 + 各 1 個自製關卡 = 105 關
// ============================================================================

// --- 遊戲 1：🚀 星際編碼號 (20關 + 1自製) ---
// 字串編碼 7x7: 0=空地, 1=隕石, 2=水晶, 3=終點, 4=雷射門, 5=雷射開關, 6=蟲洞
const G1_LEVELS = [
    {name:"G1-01 直線啟航", opt:2, start:[1,5,0], desc:"歡迎來到星際編碼號！試著用「🔄重複 4 次」搭配「⬆️前進」直達太空船！", grid:["1111111","1311111","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-02 右轉彎道", opt:5, start:[1,5,0], desc:"先往上走 4 步，向右轉，再往前走 3 步抵達太空船！", grid:["1111111","1222311","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-03 雙重轉角", opt:7, start:[1,5,1], desc:"機器人面向右方！先往右、再往上、最後往左抵達終點。", grid:["1111111","1132211","1111211","1111211","1111211","1022211","1111111"]},
    {name:"G1-04 星際階梯", opt:5, start:[1,5,0], desc:"觀察規律：把「前進 ➔ 右轉 ➔ 前進 ➔ 左轉」放進重複 3 次迴圈！", grid:["1111111","1111111","1110311","1102111","1021111","1011111","1111111"]},
    {name:"G1-05 四階長梯", opt:5, start:[1,5,0], desc:"更長的階梯！同樣的 4 個動作，這次改用「🔄重複 4 次」一次解決！", grid:["1111111","1111031","1110211","1102111","1021111","1011111","1111111"]},
    {name:"G1-06 環狀巡航", opt:7, start:[1,5,0], desc:"沿著正方形外圍收集 3 個角落的水晶，善用兩段迴圈！", grid:["1111111","1222221","1211121","1211121","1211121","1011131","1111111"]},
    {name:"G1-07 雷射初體驗", opt:6, start:[1,3,1], desc:"紅色雷射擋路了！先走到「🔘開關」格執行「👆開關」，即可解除雷射！", grid:["1111111","1111111","1111111","1025423","1111111","1111111","1111111"]},
    {name:"G1-08 雷射支線", opt:8, start:[1,5,0], desc:"先直走去最上方按下雷射開關，再轉彎通過雷射門！", grid:["1111111","1522431","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-09 折返解鎖", opt:9, start:[1,3,1], desc:"開關在上方小房間，進去按完開關後向後轉出來，繼續往右前進！", grid:["1111111","1115111","1112111","1020423","1111111","1111111","1111111"]},
    {name:"G1-10 雙重防衛網", opt:8, start:[1,5,0], desc:"一個開關可以同時解除地圖上所有的雷射門！", grid:["1111111","1542431","1211111","1211111","1211111","1011111","1111111"]},
    {name:"G1-11 蟲洞初體驗", opt:4, start:[1,5,1], desc:"走進「🌀蟲洞」會瞬間移動到另一個蟲洞，而且機器人面向不會改變喔！", grid:["1111111","1622231","1111111","1111111","1111111","1022611","1111111"]},
    {name:"G1-12 蟲洞轉向", opt:6, start:[1,5,0], desc:"從下方往上走進蟲洞，出來後也是朝上喔！記得右轉才能拿到水晶。", grid:["1111111","1111111","1162231","1111111","1611111","1011111","1111111"]},
    {name:"G1-13 蟲洞與雷射", opt:7, start:[1,5,0], desc:"先往上踩開關，再走進蟲洞躍遷到右側通道直達終點！", grid:["1111111","1611131","1511141","1211121","1211161","1011111","1111111"]},
    {name:"G1-14 螺旋向心", opt:9, start:[1,5,0], desc:"順時針螺旋迷宮！算準每一邊的長度，逐步往中心太空船推進。", grid:["1111111","1222221","1211121","1213121","1212221","1011111","1111111"]},
    {name:"G1-15 之字形峽谷", opt:8, start:[1,5,0], desc:"連續 S 型彎道，考驗左轉與右轉的空間相對方向感！", grid:["1111111","1112231","1112111","1222111","1211111","1011111","1111111"]},
    {name:"G1-16 階梯雷射陣", opt:8, start:[1,5,0], desc:"先用階梯迴圈爬到頂端按下開關，再一口氣衝向終點！", grid:["1111111","1111543","1110211","1102111","1021111","1011111","1111111"]},
    {name:"G1-17 雙島躍遷", opt:7, start:[1,5,1], desc:"利用蟲洞在兩座太空孤島之間穿梭，先把開關打開再前往終點！", grid:["1111111","1116231","1111141","1111121","1111151","1025611","1111111"]},
    {name:"G1-18 迴圈傳送帶", opt:5, start:[1,5,0], desc:"超酷技巧：把蟲洞躍遷也算進「🔄重複迴圈」的步數裡，3 行指令就能過關！", grid:["1111111","1111311","1111211","1611211","1211611","1011111","1111111"]},
    {name:"G1-19 矩陣巡邏官", opt:9, start:[1,5,0], desc:"收集三條通道的水晶，善用迴圈減少重複的直走指令！", grid:["1111111","1222221","1211121","1213221","1211111","1011111","1111111"]},
    {name:"G1-20 星際總司令", opt:9, start:[1,5,0], desc:"畢業最終考驗！結合長廊迴圈、雷射開關、蟲洞躍遷與轉向，拿下滿分三星！", grid:["1111111","1526131","1211141","1211121","1211161","1011111","1111111"]},
    {name:"🛠️ 自製創客迷宮", opt:6, start:[1,5,0], desc:"【創客模式】點擊下方畫筆即可直接塗改地圖，設計完畢後直接按執行測試！", grid:["1111111","1000311","1011011","1211011","1011011","1000011","1111111"]}
];

// --- 遊戲 2：⚡ 光子邏輯閘 (20關 + 1自製) ---
const G2_LEVELS = [
    {name:"G2-01 認識 AND 合力門", ins:2, g1:"AND", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【AND 門】兩個輸入都必須是 1，輸出才會是 1！點擊左側開關啟動核心。"},
    {name:"G2-02 認識 OR 任一門", ins:2, g1:"OR", g2:"NONE", g3:"NONE", rule:"EXACT_1", desc:"【OR 門】只要任一個是 1 就會通電！（任務限制：只能開啟剛好 1 個開關）"},
    {name:"G2-03 認識 XOR 獨享門", ins:2, g1:"XOR", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【XOR 門】兩個輸入必須「一亮一暗（不同）」，輸出才會是 1！"},
    {name:"G2-04 認識 NAND 反合力門", ins:2, g1:"NAND", g2:"NONE", g3:"NONE", rule:"AT_LEAST_1", desc:"【NAND 門】只要不是兩個都亮，輸出就是 1！（限制：至少開啟 1 個開關）"},
    {name:"G2-05 認識 NOR 全暗門", ins:2, g1:"NOR", g2:"NONE", g3:"NONE", rule:"NONE", desc:"【NOR 門】只有當兩個輸入都是 0 時，輸出才會是 1！"},
    {name:"G2-06 雙閘合力串聯", ins:4, g1:"AND", g2:"OR", g3:"AND", rule:"MAX_3", desc:"上方 G1(AND) 與下方 G2(OR) 都要輸出 1，最終 G3(AND) 才會亮！（限制：最多開 3 個）"},
    {name:"G2-07 獨享與合力交會", ins:4, g1:"XOR", g2:"AND", g3:"AND", rule:"NONE", desc:"G1(XOR) 需一亮一暗，G2(AND) 需兩個都亮，最終匯集點亮核心！"},
    {name:"G2-08 雙重獨享謎題", ins:4, g1:"XOR", g2:"XOR", g3:"XOR", rule:"EXACT_1", desc:"三個都是 XOR 門！限制：【只能開啟剛好 1 個開關】點亮核心！"},
    {name:"G2-09 雙重獨享與合力", ins:4, g1:"XOR", g2:"XOR", g3:"AND", rule:"EXACT_2", desc:"上下兩個 XOR 都必須輸出 1，且【剛好開啟 2 個開關】！"},
    {name:"G2-10 反轉陷阱電路", ins:4, g1:"NAND", g2:"AND", g3:"AND", rule:"EXACT_2", desc:"G1 是 NAND（全亮會斷電），G2 是 AND。請用【剛好 2 個開關】點亮核心！"},
    {name:"G2-11 靜音啟動電路", ins:4, g1:"NOR", g2:"OR", g3:"AND", rule:"EXACT_1", desc:"G1(NOR) 必須全 0 才會輸出 1！請用【剛好 1 個開關】啟動核心。"},
    {name:"G2-12 對稱反轉網路", ins:4, g1:"NAND", g2:"NAND", g3:"XOR", rule:"EXACT_2", desc:"最後一關是 XOR，代表 G1 與 G2 必須「一亮一暗」！限制：【剛好開啟 2 個開關】。"},
    {name:"G2-13 高壓防過載", ins:4, g1:"OR", g2:"NAND", g3:"XOR", rule:"EXACT_3", desc:"進階推理：限制【必須開啟剛好 3 個開關】，且讓最終 XOR 輸出 1！"},
    {name:"G2-14 零能量反轉", ins:4, g1:"AND", g2:"OR", g3:"NOR", rule:"EXACT_1", desc:"最終是 NOR 門（G1 與 G2 都必須輸出 0 才會亮）！限制：【剛好開啟 1 個開關】。"},
    {name:"G2-15 雙核反合力", ins:4, g1:"XOR", g2:"XOR", g3:"NAND", rule:"EXACT_2", desc:"限制：【剛好開啟 2 個開關】且『開關 A 必須開啟』，讓最終 NAND 輸出 1！"},
    {name:"G2-16 嚴格奇偶檢驗", ins:4, g1:"AND", g2:"NOR", g3:"OR", rule:"EXACT_2", desc:"限制：【剛好開啟 2 個開關】，使 G1(AND) 或 G2(NOR) 至少一邊輸出 1！"},
    {name:"G2-17 邏輯鎖定迴路", ins:4, g1:"NOR", g2:"XOR", g3:"AND", rule:"EXACT_1", desc:"G1(NOR) 與 G2(XOR) 必須同時輸出 1！找出唯一符合的開關組合。"},
    {name:"G2-18 反向互斥網路", ins:4, g1:"NAND", g2:"NOR", g3:"XOR", rule:"EXACT_3", desc:"限制：【必須開啟剛好 3 個開關】，並使 G1(NAND) 與 G2(NOR) 結果相異！"},
    {name:"G2-19 雙通道極限", ins:4, g1:"XOR", g2:"NAND", g3:"AND", rule:"EXACT_3", desc:"限制：【必須開啟剛好 3 個開關】，且 G1(XOR) 與 G2(NAND) 同時為 1！"},
    {name:"G2-20 首席晶片架構師", ins:4, g1:"NOR", g2:"NAND", g3:"AND", rule:"EXACT_1", desc:"終極考驗：限制【剛好開啟 1 個開關】，同時滿足 NOR 與 NAND 雙重條件！"},
    {name:"🛠️ 自製數位電路", ins:4, g1:"XOR", g2:"AND", g3:"OR", rule:"NONE", desc:"【創客模式】直接點擊畫布中間的邏輯閘方塊，即可切換 AND/OR/XOR/NAND/NOR！"}
];

// --- 遊戲 3：⚖️ 能量排序室 (20關 + 1自製) ---
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
    {name:"G3-10 六瓶奇偶分流", arr:[11,40,33,20,22,15], mode:"EVEN_ODD", adj:false, opt:3, desc:"【奇偶分流】先把偶數 [20, 22, 40] 排左邊，奇數 [11, 15, 33] 排右邊！"},
    {name:"G3-11 能量山峰陣列", arr:[10,50,20,40,30], mode:"MOUNTAIN", adj:false, opt:2, desc:"【山峰排序】排成中間最高、兩側對稱遞減：[10, 30, 50, 40, 20]！"},
    {name:"G3-12 能量山谷陣列", arr:[30,10,50,20,40], mode:"VALLEY", adj:false, opt:2, desc:"【山谷排序】排成兩側高、中間最低：[50, 30, 10, 20, 40]！"},
    {name:"G3-13 波浪高低交錯", arr:[10,20,30,40,50], mode:"ZIGZAG", adj:false, opt:2, desc:"【波浪排序】排成高低交錯：[20, 10, 40, 30, 50]！"},
    {name:"G3-14 六瓶自由最佳化", arr:[60,50,40,30,20,10], mode:"ASC", adj:false, opt:3, desc:"【由小到大】6 瓶完全反序，對稱交換只需 3 步！"},
    {name:"G3-15 六瓶循環置換", arr:[20,30,40,50,60,10], mode:"ASC", adj:false, opt:5, desc:"【由小到大】全部往左錯位一格！體驗循環置換 (Cycle) 需 5 步。"},
    {name:"G3-16 五瓶泡泡進階", arr:[50,10,40,20,30], mode:"ASC", adj:true, opt:5, desc:"⚠️【只能交換相鄰兩瓶】5 瓶泡泡排序，黃金目標 5 步！"},
    {name:"G3-17 泡泡遞減挑戰", arr:[10,40,20,50,30], mode:"DESC", adj:true, opt:5, desc:"⚠️【只能交換相鄰兩瓶 + 由大到小】把大數往左浮上去！"},
    {name:"G3-18 七瓶極速歸位", arr:[70,20,50,10,60,40,30], mode:"ASC", adj:false, opt:5, desc:"【由小到大】7 瓶高難度亂序！先找能互相歸位的雙向交換。"},
    {name:"G3-19 八瓶旗艦排序", arr:[80,10,60,30,50,40,70,20], mode:"ASC", adj:false, opt:6, desc:"【由小到大】8 瓶大型陣列！運用選擇排序思維在 6 步內破解！"},
    {name:"G3-20 排序演算法宗師", arr:[50,30,40,10,20], mode:"ASC", adj:true, opt:7, desc:"⚠️【終極泡泡考驗：只能交換相鄰兩瓶】在 7 步內完成由小到大排序！"},
    {name:"🛠️ 自製排序實驗室", arr:[60,10,40,20,50,30], mode:"ASC", adj:false, opt:4, desc:"【創客模式】可在下方輸入自訂數字序列，並切換排序規則！"}
];

// --- 遊戲 4：🗼 星際河內塔 (20關 + 1自製) ---
const G4_LEVELS = [
    {name:"G4-01 雙環初體驗", pegs:[[2,1],[],[]], target:2, adj:false, opt:3, desc:"把所有能量環移到 C 柱！規則：小環永遠只能疊在大環上面。"},
    {name:"G4-02 指定 B 柱終點", pegs:[[2,1],[],[]], target:1, adj:false, opt:3, desc:"這次目標終點在中間的「B 柱」喔！只需 3 步。"},
    {name:"G4-03 散落雙環集合", pegs:[[],[2],[1]], target:0, adj:false, opt:2, desc:"能量環散開了！請用 2 步將它們全部集中到最左邊的「A 柱」。"},
    {name:"G4-04 經典三環河內塔", pegs:[[3,2,1],[],[]], target:2, adj:false, opt:7, desc:"經典遞迴：先把 [2,1] 移到 B 柱，再把大環 3 移到 C 柱。黃金 7 步！"},
    {name:"G4-05 三環移往中柱", pegs:[[3,2,1],[],[]], target:1, adj:false, opt:7, desc:"將 3 個環全部移到中間的「B 柱」，思考第一步該移去哪一柱？"},
    {name:"G4-06 散落三環重組", pegs:[[3],[2],[1]], target:2, adj:false, opt:3, desc:"三環各據一柱！只需 3 步就能在 C 柱完成合體！"},
    {name:"G4-07 錯位三環救援", pegs:[[3,1],[2],[]], target:2, adj:false, opt:5, desc:"觀察目前狀態，不用重頭搬，5 步內移到 C 柱！"},
    {name:"G4-08 四柱三環極速版", pegs:[[3,2,1],[],[],[]], target:3, adj:false, opt:5, desc:"多了一根 D 柱（共 4 柱）！善用多出來的柱子，3 環只需 5 步！"},
    {name:"G4-09 相鄰限制：雙環", pegs:[[2,1],[],[]], target:2, adj:true, opt:8, desc:"⚠️【相鄰限制：每次只能移到隔壁柱子 (A↔B↔C)】不能直接跨越！"},
    {name:"G4-10 相鄰限制：中柱起點", pegs:[[],[2,1],[]], target:2, adj:true, opt:4, desc:"⚠️【相鄰限制】從中間 B 柱出發，利用 A 柱緩衝移往 C 柱！"},
    {name:"G4-11 四環散落重組", pegs:[[4],[3],[2,1]], target:0, adj:false, opt:5, desc:"最大環 4 號已經在目標 A 柱底下了！只需把剩下 3 環搬過去。"},
    {name:"G4-12 四環雙塔合流", pegs:[[4,3],[2,1],[]], target:2, adj:false, opt:11, desc:"[4,3] 與 [2,1] 分成兩疊，規劃緩衝區移往 C 柱！"},
    {name:"G4-13 四柱四環挑戰", pegs:[[4,3,2,1],[],[],[]], target:3, adj:false, opt:9, desc:"4 根柱子搬運 4 個能量環！黃金步數只要 9 步！"},
    {name:"G4-14 經典三柱四環", pegs:[[4,3,2,1],[],[]], target:2, adj:false, opt:15, desc:"經典 4 環河內塔！運用遞迴思維（7步 + 1步 + 7步 = 15步）完美破解！"},
    {name:"G4-15 四柱散落五環", pegs:[[5,4],[3],[2],[1]], target:0, adj:false, opt:6, desc:"5 個環散落在 4 根柱子，而且 5 與 4 已經在目標 A 柱了！"},
    {name:"G4-16 四柱五環星際塔", pegs:[[5,4,3,2,1],[],[],[]], target:3, adj:false, opt:13, desc:"5 個能量環登場！利用 4 根柱子在 13 步內移到 D 柱！"},
    {name:"G4-17 四柱相鄰限制(3環)", pegs:[[3,2,1],[],[],[]], target:3, adj:true, opt:10, desc:"⚠️【4 柱 + 僅限相鄰柱移動】將 3 個環一路往右推進到 D 柱！"},
    {name:"G4-18 逆境五環救援", pegs:[[5],[4,3],[2,1]], target:0, adj:false, opt:11, desc:"5 號大環已在 A 柱，運用三柱遞迴把 [4,3] 與 [2,1] 疊回 A 柱！"},
    {name:"G4-19 經典三柱五環", pegs:[[5,4,3,2,1],[],[]], target:2, adj:false, opt:31, desc:"三柱 5 環大考驗（黃金 31 步）！考驗極致專注力與遞迴節奏。"},
    {name:"G4-20 遞迴宗師：相鄰三環", pegs:[[3,2,1],[],[]], target:2, adj:true, opt:26, desc:"⚠️【終極考驗：3 柱 3 環 + 只能移到相鄰柱子】黃金步數 26 步！"},
    {name:"🛠️ 自製河內塔工坊", pegs:[[3,2,1],[],[]], target:2, adj:false, opt:7, desc:"【創客模式】使用下方工具自由設定環數(2~5)、柱數(3~4)與相鄰限制！"}
];

// --- 遊戲 5：🎨 像素解碼器 (20關 + 1自製, 6x6 二進位矩陣) ---
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

// ============================================================================
// 介面切換與關卡載入器
// ============================================================================
function switchGame(gIdx) {
    g1StopTimer();
    appState.currentGame = gIdx;
    const btns = document.querySelectorAll("#gameTabs .nav-btn");
    btns.forEach((b, i) => b.classList.toggle("active", i === gIdx));
    loadLevel(0);
}

function renderLevelBar() {
    const bar = document.getElementById("levelBar");
    let html = "";
    for (let i = 0; i < 21; i++) {
        const isCustom = (i === 20);
        const isActive = (i === appState.currentLevel);
        const st = appState.stars[`${appState.currentGame}_${i}`] || 0;
        const starTxt = st > 0 ? " " + "★".repeat(st) : "";
        const label = isCustom ? "🛠️ 自製關卡" : `第${i+1}關${starTxt}`;
        const cls = `lvl-btn ${isCustom ? 'custom' : ''} ${isActive ? 'active' : ''}`;
        html += `<button class="${cls}" onclick="loadLevel(${i})">${label}</button>`;
    }
    bar.innerHTML = html;
}

function loadLevel(lIdx) {
    g1StopTimer();
    appState.currentLevel = lIdx;
    renderLevelBar();
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

// ============================================================================
// 遊戲 1：🚀 星際編碼號 (CodeBot)
// ============================================================================
let g1State = { cmds: [], grid: [], rx:1, ry:5, rdir:0, laserOn:true, gotC:0, totalC:0, timer:null, brush:1 };

function g1StopTimer() {
    if (g1State.timer) { clearTimeout(g1State.timer); g1State.timer = null; }
}

function initGame1(lIdx) {
    if (lIdx === 20 && appState.customLevels.g1) {
        G1_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g1));
    }
    const lvl = G1_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🚀 ${lvl.name}   【⭐⭐⭐ 黃金目標：${lvl.opt} 行有效積木內】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;

    g1State.cmds = [];
    g1State.brush = 1;

    const customHtml = (lIdx === 20) ? `
        <div class="brush-bar" id="g1BrushBar">
            <span style="font-size:0.82rem; color:#ffd54f; font-weight:bold; align-self:center;">🎨 點擊畫筆塗改地圖：</span>
            <button class="brush-btn" onclick="g1SetBrush(0,this)">空地</button>
            <button class="brush-btn active" onclick="g1SetBrush(1,this)">🪨隕石</button>
            <button class="brush-btn" onclick="g1SetBrush(2,this)">💎水晶</button>
            <button class="brush-btn" onclick="g1SetBrush(3,this)">🛸終點</button>
            <button class="brush-btn" onclick="g1SetBrush(4,this)">🔴雷射</button>
            <button class="brush-btn" onclick="g1SetBrush(5,this)">🔘開關</button>
            <button class="brush-btn" onclick="g1SetBrush(6,this)">🌀蟲洞</button>
            <button class="brush-btn" onclick="g1SetBrush(99,this)">🤖起點/轉向</button>
        </div>` : "";

    document.getElementById("stageContent").innerHTML = `
        <div class="game-flex">
            <div>
                <canvas id="g1Canvas" width="420" height="420"></canvas>
                <div class="status-banner" id="g1Status">🤖 機器人就緒！請在右側組合指令積木。</div>
                ${customHtml}
            </div>
            <div class="control-box">
                <div style="font-weight:bold; color:#4dd0e1; margin-bottom:6px;">🧩 點擊加入指令積木：</div>
                <div class="block-grid">
                    <button class="cmd-btn" style="background:#64b5f6;" onclick="g1Add('MOVE')">⬆️ 前進</button>
                    <button class="cmd-btn" style="background:#4dd0e1;" onclick="g1Add('LEFT')">↩️ 左轉</button>
                    <button class="cmd-btn" style="background:#4dd0e1;" onclick="g1Add('RIGHT')">↪️ 右轉</button>
                    <button class="cmd-btn" style="background:#ffd54f;" onclick="g1Add('SWITCH')">👆 觸發開關</button>
                    <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_2')">🔄 重複 2 次</button>
                    <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_3')">🔄 重複 3 次</button>
                    <button class="cmd-btn" style="background:#b388ff;" onclick="g1Add('LOOP_4')">🔄 重複 4 次</button>
                    <button class="cmd-btn" style="background:#ea80fc;" onclick="g1Add('END_LOOP')">🔚 結束重複</button>
                </div>
                <div style="display:flex; gap:6px; margin-bottom:6px;">
                    <button class="cmd-btn" style="background:#69f0ae; flex:2;" onclick="g1Run()">▶️ 執行程式</button>
                    <button class="cmd-btn" style="background:#ffb74d; flex:1;" onclick="g1Pop()">⌫ 退一步</button>
                    <button class="cmd-btn" style="background:#ff80ab; flex:1;" onclick="g1Clear()">🗑️ 清空</button>
                </div>
                <div style="font-size:0.85rem; color:#ffd54f; font-weight:bold;" id="g1CmdHeader">📋 指令序列 (0 行)：</div>
                <div class="cmd-list" id="g1CmdList"></div>
            </div>
        </div>
    `;

    document.getElementById("g1Canvas").addEventListener("click", g1CanvasClick);
    g1ResetBoard();
    g1RenderCmds(-1);
}

function g1SetBrush(b, btnEl) {
    g1State.brush = b;
    document.querySelectorAll("#g1BrushBar .brush-btn").forEach(el => el.classList.remove("active"));
    btnEl.classList.add("active");
}

function g1CanvasClick(e) {
    if (appState.currentLevel !== 20 || g1State.timer) return;
    const rect = e.target.getBoundingClientRect();
    const scaleX = 420 / rect.width;
    const scaleY = 420 / rect.height;
    const gx = Math.floor((e.clientX - rect.left) * scaleX / 60);
    const gy = Math.floor((e.clientY - rect.top) * scaleY / 60);
    if (gx >= 0 && gx < 7 && gy >= 0 && gy < 7) {
        const lvl = G1_LEVELS[20];
        let rowArr = lvl.grid[gy].split("");
        if (g1State.brush === 99) {
            if (lvl.start[0] === gx && lvl.start[1] === gy) lvl.start[2] = (lvl.start[2] + 1) % 4;
            else { lvl.start[0] = gx; lvl.start[1] = gy; }
            rowArr[gx] = "0";
        } else {
            rowArr[gx] = String(g1State.brush);
        }
        lvl.grid[gy] = rowArr.join("");
        appState.customLevels.g1 = JSON.parse(JSON.stringify(lvl));
        saveProgress();
        g1ResetBoard();
    }
}

function g1ResetBoard() {
    g1StopTimer();
    const lvl = G1_LEVELS[appState.currentLevel];
    g1State.grid = lvl.grid.map(r => r.split("").map(Number));
    g1State.rx = lvl.start[0];
    g1State.ry = lvl.start[1];
    g1State.rdir = lvl.start[2];
    g1State.laserOn = true;
    g1State.gotC = 0;
    g1State.totalC = g1State.grid.flat().filter(x => x === 2).length;
    g1Draw();
}

function g1Draw() {
    const cvs = document.getElementById("g1Canvas");
    if (!cvs) return;
    const ctx = cvs.getContext("2d");
    const cs = 60;
    ctx.clearRect(0, 0, 420, 420);

    for (let y = 0; y < 7; y++) {
        for (let x = 0; x < 7; x++) {
            const x1 = x * cs, y1 = y * cs;
            const cell = g1State.grid[y][x];
            ctx.fillStyle = (x + y) % 2 === 0 ? "#141827" : "#0e111d";
            if (cell === 4 && g1State.laserOn) ctx.fillStyle = "#3b1222";
            ctx.fillRect(x1, y1, cs, cs);
            ctx.strokeStyle = "#232942";
            ctx.strokeRect(x1, y1, cs, cs);

            ctx.font = "26px 'Segoe UI Emoji', sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            const cx = x1 + cs / 2, cy = y1 + cs / 2;

            if (cell === 1) ctx.fillText("🪨", cx, cy);
            else if (cell === 2) ctx.fillText("💎", cx, cy);
            else if (cell === 3) ctx.fillText("🛸", cx, cy);
            else if (cell === 4 && g1State.laserOn) {
                ctx.strokeStyle = "#ff4081"; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(x1, cy); ctx.lineTo(x1+cs, cy); ctx.stroke();
                ctx.lineWidth = 1;
                ctx.fillText("⚡", cx, cy);
            } else if (cell === 5) ctx.fillText("🔘", cx, cy);
            else if (cell === 6) ctx.fillText("🌀", cx, cy);
        }
    }

    // 繪製發光機器人與方向箭頭
    const rx = g1State.rx * cs + cs / 2, ry = g1State.ry * cs + cs / 2;
    ctx.beginPath();
    ctx.arc(rx, ry, 21, 0, Math.PI * 2);
    ctx.fillStyle = "#29b6f6";
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = "#fff";
    ctx.stroke();
    ctx.font = "22px 'Segoe UI Emoji', sans-serif";
    ctx.fillText("🤖", rx, ry);

    const dirs = [[0,-1],[1,0],[0,1],[-1,0]];
    const arrows = ["▲","▶","▼","◀"];
    const [dx, dy] = dirs[g1State.rdir];
    const ax = rx + dx * 22, ay = ry + dy * 22;
    ctx.beginPath();
    ctx.arc(ax, ay, 8, 0, Math.PI * 2);
    ctx.fillStyle = "#ff4081";
    ctx.fill();
    ctx.font = "bold 10px Consolas";
    ctx.fillStyle = "#fff";
    ctx.fillText(arrows[g1State.rdir], ax, ay);
}

function g1Add(cmd) {
    if (g1State.timer || g1State.cmds.length >= 24) return;
    g1State.cmds.push(cmd);
    g1RenderCmds(-1);
}
function g1Pop() {
    if (!g1State.timer && g1State.cmds.length > 0) {
        g1State.cmds.pop();
        g1RenderCmds(-1);
    }
}
function g1Clear() {
    if (!g1State.timer) {
        g1State.cmds = [];
        g1ResetBoard();
        g1RenderCmds(-1);
    }
}

function g1RenderCmds(activeIdx) {
    const listEl = document.getElementById("g1CmdList");
    const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
    const opt = G1_LEVELS[appState.currentLevel].opt;
    document.getElementById("g1CmdHeader").innerText = `📋 有效積木：${eff} 個 (黃金目標：${opt} 個)`;

    let html = "";
    let py = ["# 🚀 星際編碼號 Python 程式", "import space_bot as bot\n"];
    let indent = 0;
    const mapTxt = {
        MOVE: ["⬆️ 向前走一步", "bot.move_forward()"],
        LEFT: ["↩️ 向左轉 90°", "bot.turn_left()"],
        RIGHT: ["↪️ 向右轉 90°", "bot.turn_right()"],
        SWITCH: ["👆 觸發開關", "bot.trigger_switch()"]
    };

    g1State.cmds.forEach((c, i) => {
        const cls = (i === activeIdx) ? "cmd-item running" : "cmd-item";
        if (c === "END_LOOP") {
            indent = Math.max(0, indent - 1);
            html += `<div class="${cls}">${String(i+1).padStart(2,'0')}. ${"&nbsp;&nbsp;".repeat(indent)}🔚 結束重複</div>`;
        } else if (c.startsWith("LOOP_")) {
            const n = c.split("_")[1];
            html += `<div class="${cls}">${String(i+1).padStart(2,'0')}. ${"&nbsp;&nbsp;".repeat(indent)}🔄 重複 ${n} 次:</div>`;
            py.push(`${"    ".repeat(indent)}for i in range(${n}):`);
            indent++;
        } else {
            const [lbl, code] = mapTxt[c];
            html += `<div class="${cls}">${String(i+1).padStart(2,'0')}. ${"&nbsp;&nbsp;".repeat(indent)}${lbl}</div>`;
            py.push(`${"    ".repeat(indent)}${code}`);
        }
    });
    listEl.innerHTML = html || "<div style='color:#607d8b;'>尚未加入指令積木...</div>";
    updatePythonBox(
        py.join("\n"),
        "當地圖出現規律的直線或階梯時，使用 <code>for i in range(N):</code> 迴圈能大幅縮短程式碼行數，拿下 3 顆星！"
    );
}

function g1Compile(cmds) {
    function parse(idx) {
        let out = [];
        while (idx < cmds.length) {
            const c = cmds[idx];
            if (c === "END_LOOP") return [out, idx + 1];
            if (c.startsWith("LOOP_")) {
                const n = parseInt(c.split("_")[1]);
                const [sub, nxt] = parse(idx + 1);
                for (let k = 0; k < n; k++) out.push(...sub);
                idx = nxt;
            } else {
                out.push({act: c, line: idx});
                idx++;
            }
        }
        return [out, idx];
    }
    return parse(0)[0];
}

function g1Run() {
    if (g1State.timer || g1State.cmds.length === 0) return;
    g1ResetBoard();
    const queue = g1Compile(g1State.cmds);
    if (queue.length === 0) return;

    let stepIdx = 0;
    function step() {
        if (stepIdx >= queue.length) {
            g1State.timer = null;
            g1RenderCmds(-1);
            const curCell = g1State.grid[g1State.ry][g1State.rx];
            if (curCell === 3 && g1State.gotC === g1State.totalC) {
                const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
                const opt = G1_LEVELS[appState.currentLevel].opt;
                const stars = eff <= opt ? 3 : (eff <= opt + 2 ? 2 : 1);
                awardStars(0, appState.currentLevel, stars);
            } else {
                document.getElementById("g1Status").innerText = "🤔 還沒收集完所有水晶或還沒抵達太空船喔！";
            }
            return;
        }
        const {act, line} = queue[stepIdx];
        g1RenderCmds(line);
        const dirs = [[0,-1],[1,0],[0,1],[-1,0]];

        if (act === "LEFT") g1State.rdir = (g1State.rdir + 3) % 4;
        else if (act === "RIGHT") g1State.rdir = (g1State.rdir + 1) % 4;
        else if (act === "SWITCH") {
            if (g1State.grid[g1State.ry][g1State.rx] === 5) g1State.laserOn = !g1State.laserOn;
        } else if (act === "MOVE") {
            const [dx, dy] = dirs[g1State.rdir];
            const nx = g1State.rx + dx, ny = g1State.ry + dy;
            if (nx < 0 || nx >= 7 || ny < 0 || ny >= 7 || g1State.grid[ny][nx] === 1 || (g1State.grid[ny][nx] === 4 && g1State.laserOn)) {
                g1State.timer = null;
                document.getElementById("g1Status").innerText = "💥 撞上隕石或雷射防護網了！請調整積木再試一次。";
                return;
            }
            g1State.rx = nx; g1State.ry = ny;
            if (g1State.grid[ny][nx] === 2) {
                g1State.grid[ny][nx] = 0;
                g1State.gotC++;
            } else if (g1State.grid[ny][nx] === 6) {
                outer: for (let py = 0; py < 7; py++) {
                    for (let px = 0; px < 7; px++) {
                        if (g1State.grid[py][px] === 6 && (px !== nx || py !== ny)) {
                            g1State.rx = px; g1State.ry = py;
                            break outer;
                        }
                    }
                }
            }
        }
        g1Draw();
        stepIdx++;
        g1State.timer = setTimeout(step, 340);
    }
    step();
}

// ============================================================================
// 遊戲 2：⚡ 光子邏輯閘 (Logic Gate Circuit)
// ============================================================================
let g2State = { inVals: [0,0,0,0], clicks: 0, finalOut: 0 };

function initGame2(lIdx) {
    if (lIdx === 20 && appState.customLevels.g2) {
        G2_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g2));
    }
    const lvl = G2_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `⚡ ${lvl.name}`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g2State.inVals = [0,0,0,0];
    g2State.clicks = 0;

    document.getElementById("stageContent").innerHTML = `
        <div style="text-align:center;">
            <canvas id="g2Canvas" width="720" height="400"></canvas>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-top:10px; gap:8px;">
                <div style="font-size:0.86rem; color:#4dd0e1; text-align:left;">
                    💡 <b>邏輯閘真值表：</b>【AND】全1才1 ｜ 【OR】有1就1 ｜ 【XOR】相異才1 ｜ 【NAND】不全1就1 ｜ 【NOR】全0才1
                </div>
                <button class="cmd-btn" style="background:#69f0ae; padding:10px 22px; font-size:1rem;" onclick="g2CheckWin()">
                    ✅ 驗證並啟動核心
                </button>
            </div>
        </div>
    `;
    document.getElementById("g2Canvas").addEventListener("click", g2CanvasClick);
    g2EvalAndDraw();
}

function g2Calc(type, a, b) {
    if (type === "AND") return a & b;
    if (type === "OR") return a | b;
    if (type === "XOR") return a ^ b;
    if (type === "NAND") return 1 - (a & b);
    if (type === "NOR") return (a === 0 && b === 0) ? 1 : 0;
    return a;
}

function g2EvalAndDraw() {
    const lvl = G2_LEVELS[appState.currentLevel];
    const [A, B, C, D] = g2State.inVals;
    const out1 = g2Calc(lvl.g1, A, B);
    const out2 = (lvl.ins === 4) ? g2Calc(lvl.g2, C, D) : 0;
    const finalOut = (lvl.ins === 4) ? g2Calc(lvl.g3, out1, out2) : out1;
    g2State.finalOut = finalOut;

    const cvs = document.getElementById("g2Canvas");
    if (!cvs) return;
    const ctx = cvs.getContext("2d");
    ctx.clearRect(0, 0, 720, 400);

    const ys = (lvl.ins === 4) ? [75, 155, 245, 325] : [130, 270];
    const labels = ["開關 A", "開關 B", "開關 C", "開關 D"];

    // 畫導線與邏輯閘
    function drawWire(x1, y1, x2, y2, val) {
        ctx.strokeStyle = val ? "#69f0ae" : "#37474f";
        ctx.lineWidth = val ? 5 : 3;
        const mx = (x1 + x2) / 2;
        ctx.beginPath();
        ctx.moveTo(x1, y1); ctx.lineTo(mx, y1); ctx.lineTo(mx, y2); ctx.lineTo(x2, y2);
        ctx.stroke();
    }
    function drawGate(x, y, w, h, type, val) {
        ctx.fillStyle = val ? "#1e88e5" : "#263238";
        ctx.strokeStyle = val ? "#69f0ae" : "#90a4ae";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.roundRect(x, y, w, h, 12);
        ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#fff";
        ctx.font = "bold 15px 'Microsoft JhengHei'";
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(`${type} 閘`, x + w/2, y + h/2 - 10);
        ctx.font = "bold 13px Consolas";
        ctx.fillStyle = val ? "#ffd54f" : "#b0bec5";
        ctx.fillText(`OUT = ${val}`, x + w/2, y + h/2 + 12);
    }

    if (lvl.ins === 2) {
        drawWire(150, 130, 290, 185, A);
        drawWire(150, 270, 290, 215, B);
        drawGate(290, 155, 130, 90, lvl.g1, out1);
        drawWire(420, 200, 560, 200, finalOut);
    } else {
        drawWire(150, 75, 250, 105, A);
        drawWire(150, 155, 250, 130, B);
        drawGate(250, 75, 120, 80, lvl.g1, out1);

        drawWire(150, 245, 250, 275, C);
        drawWire(150, 325, 250, 300, D);
        drawGate(250, 245, 120, 80, lvl.g2, out2);

        drawWire(370, 115, 445, 185, out1);
        drawWire(370, 285, 445, 215, out2);
        drawGate(445, 160, 120, 80, lvl.g3, finalOut);
        drawWire(565, 200, 605, 200, finalOut);
    }

    // 畫左側開關
    for (let i = 0; i < lvl.ins; i++) {
        const y = ys[i], v = g2State.inVals[i];
        ctx.fillStyle = v ? "#69f0ae" : "#263238";
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.roundRect(30, y - 24, 120, 48, 10); ctx.fill(); ctx.stroke();
        ctx.fillStyle = v ? "#111" : "#fff";
        ctx.font = "bold 15px 'Microsoft JhengHei'";
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(`${labels[i]} : ${v}`, 90, y);
    }

    // 畫右側能量核心
    ctx.beginPath();
    ctx.arc(650, 200, 45, 0, Math.PI * 2);
    ctx.fillStyle = finalOut ? "#ffd54f" : "#263238";
    ctx.fill();
    ctx.lineWidth = 4;
    ctx.strokeStyle = finalOut ? "#69f0ae" : "#546e7a";
    ctx.stroke();
    ctx.fillStyle = finalOut ? "#111" : "#eceff4";
    ctx.font = "bold 15px 'Microsoft JhengHei'";
    ctx.fillText("🎯核心", 650, 190);
    ctx.fillText(`OUT=${finalOut}`, 650, 212);

    const py = [
        "# ⚡ 布林代數與數位邏輯電路",
        `A, B, C, D = ${A}, ${B}, ${C}, ${D}`,
        `gate1 = calc_${lvl.g1}(A, B)  # -> ${out1}`
    ];
    if (lvl.ins === 4) {
        py.push(`gate2 = calc_${lvl.g2}(C, D)  # -> ${out2}`);
        py.push(`core  = calc_${lvl.g3}(gate1, gate2)  # -> ${finalOut}`);
    } else {
        py.push(`core  = gate1  # -> ${finalOut}`);
    }
    updatePythonBox(
        py.join("\n"),
        "電腦 CPU 內部由數十億個邏輯閘組成。學會推演 <code>AND</code>、<code>OR</code>、<code>XOR</code>、<code>NAND</code>、<code>NOR</code> 的真值表，就能寫出零漏洞的 <code>if-else</code> 條件判斷！"
    );
}

function g2CanvasClick(e) {
    const lvl = G2_LEVELS[appState.currentLevel];
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (720 / rect.width);
    const y = (e.clientY - rect.top) * (400 / rect.height);
    const ys = (lvl.ins === 4) ? [75, 155, 245, 325] : [130, 270];

    for (let i = 0; i < lvl.ins; i++) {
        if (x >= 30 && x <= 150 && y >= ys[i] - 24 && y <= ys[i] + 24) {
            g2State.inVals[i] = 1 - g2State.inVals[i];
            g2State.clicks++;
            g2EvalAndDraw();
            return;
        }
    }
    if (appState.currentLevel === 20) {
        const types = ["AND", "OR", "XOR", "NAND", "NOR"];
        if (x >= 250 && x <= 370 && y >= 75 && y <= 155) lvl.g1 = types[(types.indexOf(lvl.g1)+1)%5];
        else if (x >= 250 && x <= 370 && y >= 245 && y <= 325) lvl.g2 = types[(types.indexOf(lvl.g2)+1)%5];
        else if (x >= 445 && x <= 565 && y >= 160 && y <= 240) lvl.g3 = types[(types.indexOf(lvl.g3)+1)%5];
        appState.customLevels.g2 = JSON.parse(JSON.stringify(lvl));
        saveProgress();
        g2EvalAndDraw();
    }
}

function g2CheckWin() {
    const lvl = G2_LEVELS[appState.currentLevel];
    if (g2State.finalOut !== 1) {
        alert("⚠️ 右側的能量核心目前還是 0（未點亮）喔！");
        return;
    }
    const onCount = g2State.inVals.slice(0, lvl.ins).reduce((a,b)=>a+b, 0);
    if (lvl.rule === "EXACT_1" && onCount !== 1) return alert(`本關限制：必須「剛好開啟 1 個開關」（目前開啟 ${onCount} 個）！`);
    if (lvl.rule === "EXACT_2" && onCount !== 2) return alert(`本關限制：必須「剛好開啟 2 個開關」（目前開啟 ${onCount} 個）！`);
    if (lvl.rule === "EXACT_3" && onCount !== 3) return alert(`本關限制：必須「剛好開啟 3 個開關」（目前開啟 ${onCount} 個）！`);
    if (lvl.rule === "AT_LEAST_1" && onCount < 1) return alert("本關限制：至少要開啟 1 個開關！");
    if (lvl.rule === "MAX_3" && onCount > 3) return alert("本關限制：最多只能開啟 3 個開關！");
    if (appState.currentLevel === 14 && g2State.inVals[0] !== 1) return alert("本關額外限制：開關 A 必須是開啟 (1) 狀態！");

    const stars = g2State.clicks <= 4 ? 3 : (g2State.clicks <= 7 ? 2 : 1);
    awardStars(1, appState.currentLevel, stars);
}

// ============================================================================
// 遊戲 3：⚖️ 能量排序室 (Sorting Lab)
// ============================================================================
let g3State = { arr: [], sel: null, swaps: 0 };

function initGame3(lIdx) {
    if (lIdx === 20 && appState.customLevels.g3) {
        G3_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g3));
    }
    const lvl = G3_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `⚖️ ${lvl.name}   【⭐⭐⭐ 黃金目標：${lvl.opt} 次交換內】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g3State.arr = [...lvl.arr];
    g3State.sel = null;
    g3State.swaps = 0;

    const customHtml = (lIdx === 20) ? `
        <div class="brush-bar">
            <span style="font-size:0.85rem; color:#ffd54f; font-weight:bold;">🛠️ 自訂數列(空白分隔)：</span>
            <input id="g3CustomIn" value="${lvl.arr.join(' ')}" style="background:#090b10; color:#fff; border:1px solid #4dd0e1; border-radius:6px; padding:4px 8px; width:170px;">
            <button class="brush-btn active" onclick="g3ApplyCustom()">套用數列</button>
            <button class="brush-btn" onclick="g3ToggleAdj()">切換相鄰限制 (目前:${lvl.adj?'開啟':'關閉'})</button>
        </div>` : "";

    document.getElementById("stageContent").innerHTML = `
        <div style="text-align:center;">
            <canvas id="g3Canvas" width="720" height="360"></canvas>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                <div class="status-banner" id="g3Status" style="margin:0;">已交換次數：0 次 （點擊兩瓶能量管即可交換位置）</div>
                <button class="cmd-btn" style="background:#ffb74d; padding:8px 16px;" onclick="initGame3(${lIdx})">🔄 重置本關</button>
            </div>
            ${customHtml}
        </div>
    `;
    document.getElementById("g3Canvas").addEventListener("click", g3CanvasClick);
    g3Draw("尚未執行交換");
}

function g3ApplyCustom() {
    const raw = document.getElementById("g3CustomIn").value.trim().split(/\s+/).map(Number).filter(n => n >= 5 && n <= 99).slice(0, 8);
    if (raw.length >= 3) {
        G3_LEVELS[20].arr = raw;
        appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20]));
        saveProgress();
        initGame3(20);
    } else alert("請輸入 3～8 個介於 5 到 99 之間的整數！");
}

function g3ToggleAdj() {
    G3_LEVELS[20].adj = !G3_LEVELS[20].adj;
    appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20]));
    saveProgress();
    initGame3(20);
}

function g3GetTarget() {
    const lvl = G3_LEVELS[appState.currentLevel];
    const base = [...lvl.arr];
    if (lvl.mode === "ASC") return base.sort((a,b)=>a-b);
    if (lvl.mode === "DESC") return base.sort((a,b)=>b-a);
    if (lvl.mode === "EVEN_ODD") {
        const ev = base.filter(x => x%2===0).sort((a,b)=>a-b);
        const od = base.filter(x => x%2!==0).sort((a,b)=>a-b);
        return [...ev, ...od];
    }
    if (lvl.mode === "MOUNTAIN") return [10, 30, 50, 40, 20];
    if (lvl.mode === "VALLEY") return [50, 30, 10, 20, 40];
    if (lvl.mode === "ZIGZAG") return [20, 10, 40, 30, 50];
    return base.sort((a,b)=>a-b);
}

function g3Draw(lastSwapCode) {
    const cvs = document.getElementById("g3Canvas");
    if (!cvs) return;
    const ctx = cvs.getContext("2d");
    ctx.clearRect(0, 0, 720, 360);

    const n = g3State.arr.length;
    const w = Math.floor(640 / n);
    const startX = 40 + Math.floor((640 - w * n) / 2);
    const target = g3GetTarget();
    const maxVal = Math.max(...g3State.arr, 1);

    ctx.fillStyle = "#69f0ae";
    ctx.font = "bold 15px Consolas";
    ctx.textAlign = "center";
    ctx.fillText(`🎯 目標排列：[ ${target.join(", ")} ]`, 360, 28);

    g3State.arr.forEach((val, i) => {
        const x1 = startX + i * w + 12;
        const bw = w - 24;
        const bh = Math.floor((val / maxVal) * 200) + 35;
        const y2 = 305, y1 = y2 - bh;
        const isSel = (g3State.sel === i);
        const isOk = (val === target[i]);

        // 試管外框與能量液
        ctx.fillStyle = isSel ? "#ffd54f" : (isOk ? "#00e676" : "#29b6f6");
        ctx.strokeStyle = isSel ? "#fff" : "#90caf9";
        ctx.lineWidth = isSel ? 3.5 : 1.5;
        ctx.beginPath();
        ctx.roundRect(x1, y1, bw, bh, [10, 10, 4, 4]);
        ctx.fill(); ctx.stroke();

        ctx.fillStyle = isSel ? "#ffd54f" : "#fff";
        ctx.font = "bold 16px Consolas";
        ctx.fillText(String(val), x1 + bw/2, y1 - 14);

        ctx.fillStyle = "#4dd0e1";
        ctx.font = "bold 12px 'Microsoft JhengHei'";
        ctx.fillText(`[${i}]`, x1 + bw/2, y2 + 22);
        if (isOk) {
            ctx.fillStyle = "#000";
            ctx.font = "bold 15px Consolas";
            ctx.fillText("✓", x1 + bw/2, y2 - 16);
        }
    });

    updatePythonBox(
        `# ⚖️ 陣列 (List) 索引交換演算法\npotions = [${g3State.arr.join(", ")}]\ntarget  = [${target.join(", ")}]\n\n# 最新交換動作：\n${lastSwapCode}`,
        "在 Python 中，交換陣列兩個位置的元素只需寫一行：<code>a[i], a[j] = a[j], a[i]</code>。學會觀察每個數字的目標索引，就能用最少交換次數完成排序！"
    );
}

function g3CanvasClick(e) {
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (720 / rect.width);
    const n = g3State.arr.length;
    const w = Math.floor(640 / n);
    const startX = 40 + Math.floor((640 - w * n) / 2);
    const idx = Math.floor((x - startX) / w);
    if (idx < 0 || idx >= n) return;

    if (g3State.sel === null) {
        g3State.sel = idx;
        g3Draw("# 已選取 potions[" + idx + "]");
    } else if (g3State.sel === idx) {
        g3State.sel = null;
        g3Draw("# 取消選取");
    } else {
        const i = g3State.sel, j = idx;
        const lvl = G3_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(i - j) !== 1) {
            alert("⚠️ 本關開啟了「泡泡限制」：每次只能交換相鄰（隔壁）的兩瓶能量液喔！");
            g3State.sel = null;
            g3Draw("# 違反相鄰交換限制");
            return;
        }
        const tmp = g3State.arr[i];
        g3State.arr[i] = g3State.arr[j];
        g3State.arr[j] = tmp;
        g3State.swaps++;
        g3State.sel = null;
        document.getElementById("g3Status").innerText = `已交換次數：${g3State.swaps} 次`;
        g3Draw(`potions[${i}], potions[${j}] = potions[${j}], potions[${i}]`);

        const target = g3GetTarget();
        if (g3State.arr.every((v, k) => v === target[k])) {
            const stars = g3State.swaps <= lvl.opt ? 3 : (g3State.swaps <= lvl.opt + 2 ? 2 : 1);
            awardStars(2, appState.currentLevel, stars);
        }
    }
}

// ============================================================================
// 遊戲 4：🗼 星際河內塔 (Stack Tower)
// ============================================================================
let g4State = { pegs: [], sel: null, moves: 0, totalDisks: 0 };

function initGame4(lIdx) {
    if (lIdx === 20 && appState.customLevels.g4) {
        G4_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g4));
    }
    const lvl = G4_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🗼 ${lvl.name}   【⭐⭐⭐ 黃金目標：${lvl.opt} 步內】`;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g4State.pegs = JSON.parse(JSON.stringify(lvl.pegs));
    g4State.sel = null;
    g4State.moves = 0;
    g4State.totalDisks = g4State.pegs.flat().length;

    const customHtml = (lIdx === 20) ? `
        <div class="brush-bar">
            <span style="font-size:0.85rem; color:#ffd54f; font-weight:bold;">🛠️ 自訂河內塔：</span>
            <button class="brush-btn" onclick="g4Custom(2,null)">2環</button>
            <button class="brush-btn" onclick="g4Custom(3,null)">3環</button>
            <button class="brush-btn" onclick="g4Custom(4,null)">4環</button>
            <button class="brush-btn" onclick="g4Custom(5,null)">5環</button>
            <button class="brush-btn" onclick="g4Custom(null,'PEGS')">切換 3柱/4柱</button>
            <button class="brush-btn" onclick="g4Custom(null,'ADJ')">切換相鄰限制</button>
        </div>` : "";

    document.getElementById("stageContent").innerHTML = `
        <div style="text-align:center;">
            <canvas id="g4Canvas" width="720" height="360"></canvas>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                <div class="status-banner" id="g4Status" style="margin:0;">移動步數：0 步 （點擊來源柱子取出頂端能量環，再點擊目標柱子放入）</div>
                <button class="cmd-btn" style="background:#ffb74d; padding:8px 16px;" onclick="initGame4(${lIdx})">🔄 重置本關</button>
            </div>
            ${customHtml}
        </div>
    `;
    document.getElementById("g4Canvas").addEventListener("click", g4CanvasClick);
    g4Draw("# 點擊柱子開始進行 stack.pop() 與 stack.append()");
}

function g4Custom(nDisks, toggleType) {
    const lvl = G4_LEVELS[20];
    let curN = lvl.pegs.flat().length;
    let pCount = lvl.pegs.length;
    if (nDisks) curN = nDisks;
    if (toggleType === "PEGS") pCount = (pCount === 3) ? 4 : 3;
    if (toggleType === "ADJ") lvl.adj = !lvl.adj;
    const firstPeg = Array.from({length: curN}, (_, i) => curN - i);
    lvl.pegs = [firstPeg, ...Array.from({length: pCount - 1}, () => [])];
    lvl.target = pCount - 1;
    lvl.opt = (pCount === 3) ? (Math.pow(2, curN) - 1) : (curN * 2 + 1);
    appState.customLevels.g4 = JSON.parse(JSON.stringify(lvl));
    saveProgress();
    initGame4(20);
}

function g4Draw(lastCode) {
    const cvs = document.getElementById("g4Canvas");
    if (!cvs) return;
    const ctx = cvs.getContext("2d");
    ctx.clearRect(0, 0, 720, 360);

    const lvl = G4_LEVELS[appState.currentLevel];
    const numP = g4State.pegs.length;
    const spacing = Math.floor(720 / numP);
    const colors = ["#ff80ab", "#ffb74d", "#ffd54f", "#69f0ae", "#64b5f6", "#b388ff"];
    const pNames = ["A 柱", "B 柱", "C 柱", "D 柱"];

    g4State.pegs.forEach((stack, pIdx) => {
        const cx = spacing * pIdx + spacing / 2;
        const isSel = (g4State.sel === pIdx);
        const isTarget = (pIdx === lvl.target);

        ctx.fillStyle = isTarget ? "#69f0ae" : "#455a64";
        ctx.fillRect(cx - 70, 305, 140, 14);
        ctx.fillStyle = isSel ? "#ffd54f" : "#37474f";
        ctx.fillRect(cx - 6, 95, 12, 210);

        ctx.fillStyle = isTarget ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 14px 'Microsoft JhengHei'";
        ctx.textAlign = "center";
        ctx.fillText(isTarget ? `🎯 ${pNames[pIdx]}(終點)` : pNames[pIdx], cx, 338);

        stack.forEach((disk, sPos) => {
            const w = 22 + disk * 15;
            let y2 = 303 - sPos * 32;
            if (isSel && sPos === stack.length - 1) y2 -= 20;
            ctx.fillStyle = colors[(disk - 1) % colors.length];
            ctx.strokeStyle = "#fff"; ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(cx - w, y2 - 28, w * 2, 28, 8);
            ctx.fill(); ctx.stroke();

            ctx.fillStyle = "#111";
            ctx.font = "bold 13px 'Microsoft JhengHei'";
            ctx.fillText(`環 ${disk}`, cx, y2 - 14);
        });
    });

    const pVars = g4State.pegs.map((s, i) => `stack_${["A","B","C","D"][i]} = [${s.join(", ")}]`).join("\n");
    updatePythonBox(
        `# 🗼 堆疊 (Stack: 後進先出 LIFO) 與遞迴\n${pVars}\n\n# 最新堆疊操作：\n${lastCode}`,
        "柱子就是程式設計中的 <b>Stack（堆疊）</b>：只能從頂端 <code>pop()</code> 取出或 <code>append()</code> 放入。要搬動 N 個環，必須先遞迴把上面的 N-1 個環搬到暫存柱！"
    );
}

function g4CanvasClick(e) {
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (720 / rect.width);
    const numP = g4State.pegs.length;
    const pIdx = Math.floor(x / (720 / numP));
    if (pIdx < 0 || pIdx >= numP) return;

    if (g4State.sel === null) {
        if (g4State.pegs[pIdx].length > 0) {
            g4State.sel = pIdx;
            g4Draw(`# 準備從 stack_${["A","B","C","D"][pIdx]} 取出頂端能量環`);
        }
    } else if (g4State.sel === pIdx) {
        g4State.sel = null;
        g4Draw("# 取消選取");
    } else {
        const src = g4State.sel, dst = pIdx;
        const lvl = G4_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(src - dst) !== 1) {
            alert("⚠️ 本關限制每次只能移到「隔壁相鄰的柱子」喔！");
            g4State.sel = null; g4Draw("# 違反相鄰柱限制"); return;
        }
        const disk = g4State.pegs[src][g4State.pegs[src].length - 1];
        const dstTop = g4State.pegs[dst][g4State.pegs[dst].length - 1];
        if (dstTop !== undefined && dstTop < disk) {
            alert(`⚠️ 大環（環 ${disk}）不能壓在小環（環 ${dstTop}）上面喔！`);
            g4State.sel = null; g4Draw("# 違反小環在大環上規則"); return;
        }
        g4State.pegs[src].pop();
        g4State.pegs[dst].push(disk);
        g4State.moves++;
        g4State.sel = null;
        document.getElementById("g4Status").innerText = `移動步數：${g4State.moves} 步`;
        const pL = ["A","B","C","D"];
        g4Draw(`disk = stack_${pL[src]}.pop()  # 環 ${disk}\nstack_${pL[dst]}.append(disk)`);

        if (g4State.pegs[lvl.target].length === g4State.totalDisks) {
            const stars = g4State.moves <= lvl.opt ? 3 : (g4State.moves <= lvl.opt + 4 ? 2 : 1);
            awardStars(3, appState.currentLevel, stars);
        }
    }
}

// ============================================================================
// 遊戲 5：🎨 像素解碼器 (Binary Matrix, 20關 + 1自製)
// ============================================================================
let g5State = { target: [], player: [], editTarget: false, mistakes: 0 };

function initGame5(lIdx) {
    if (lIdx === 20 && appState.customLevels.g5) {
        G5_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g5));
    }
    const lvl = G5_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = `🎨 ${lvl.name}   【二進位權重與二維矩陣解碼】`;
    document.getElementById("lvlDesc").innerText = "根據上方的「連續 1 格數」與右側的「二進位十進位加總密碼（權重 32, 16, 8, 4, 2, 1）」，點擊方格切換 0 與 1，還原太空像素圖騰！";

    g5State.target = lvl.grid.map(r => r.split("").map(Number));
    g5State.player = Array.from({length: 6}, () => [0,0,0,0,0,0]);
    g5State.editTarget = false;
    g5State.mistakes = 0;

    const customHtml = (lIdx === 20) ? `
        <button class="cmd-btn" id="g5CreatorBtn" style="background:#ff80ab; padding:8px 16px;" onclick="g5ToggleCreator()">
            🎨 點此繪製自訂謎題答案
        </button>` : "";

    document.getElementById("stageContent").innerHTML = `
        <div style="text-align:center;">
            <canvas id="g5Canvas" width="720" height="400"></canvas>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; flex-wrap:wrap; gap:8px;">
                <div class="status-banner" style="margin:0;">💡 當整列或整行的密碼完全吻合時，文字會變成綠色 ✅！</div>
                <div style="display:flex; gap:8px;">
                    ${customHtml}
                    <button class="cmd-btn" style="background:#ffb74d; padding:8px 16px;" onclick="initGame5(${lIdx})">🗑️ 清空重畫</button>
                </div>
            </div>
        </div>
    `;
    document.getElementById("g5Canvas").addEventListener("click", g5CanvasClick);
    g5Draw();
}

function g5ToggleCreator() {
    g5State.editTarget = !g5State.editTarget;
    const btn = document.getElementById("g5CreatorBtn");
    if (g5State.editTarget) {
        btn.innerText = "🔒 鎖定圖案並開始解謎";
        btn.style.background = "#69f0ae";
    } else {
        G5_LEVELS[20].grid = g5State.target.map(r => r.join(""));
        appState.customLevels.g5 = JSON.parse(JSON.stringify(G5_LEVELS[20]));
        saveProgress();
        g5State.player = Array.from({length: 6}, () => [0,0,0,0,0,0]);
        btn.innerText = "🎨 點此繪製自訂謎題答案";
        btn.style.background = "#ff80ab";
    }
    g5Draw();
}

function g5RLE(arr) {
    let res = [], c = 0;
    arr.forEach(v => { if (v === 1) c++; else if (c > 0) { res.push(c); c = 0; } });
    if (c > 0) res.push(c);
    return res.length ? res.join(" ") : "0";
}

function g5Draw() {
    const cvs = document.getElementById("g5Canvas");
    if (!cvs) return;
    const ctx = cvs.getContext("2d");
    ctx.clearRect(0, 0, 720, 400);

    const ox = 165, oy = 82, cs = 50;
    const board = g5State.editTarget ? g5State.target : g5State.player;
    const weights = [32, 16, 8, 4, 2, 1];

    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    for (let col = 0; col < 6; col++) {
        const cx = ox + col * cs + cs / 2;
        const tCol = g5State.target.map(r => r[col]);
        const pCol = board.map(r => r[col]);
        const ok = tCol.every((v, i) => v === pCol[i]);
        ctx.fillStyle = ok ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 12px 'Microsoft JhengHei'";
        ctx.fillText("連續:" + g5RLE(tCol), cx, 28);
        ctx.fillStyle = "#ffd54f";
        ctx.font = "bold 13px Consolas";
        ctx.fillText(`(${weights[col]})`, cx, 60);
    }

    for (let row = 0; row < 6; row++) {
        const ry = oy + row * cs + cs / 2;
        const tRow = g5State.target[row];
        const pRow = board[row];
        const ok = tRow.every((v, i) => v === pRow[i]);
        const tDec = tRow.reduce((acc, v, i) => acc + v * weights[i], 0);
        const pDec = pRow.reduce((acc, v, i) => acc + v * weights[i], 0);

        ctx.textAlign = "right";
        ctx.fillStyle = ok ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 13px 'Microsoft JhengHei'";
        ctx.fillText(`列[${row}] 連續: ${g5RLE(tRow)}`, ox - 12, ry);

        ctx.textAlign = "left";
        ctx.fillStyle = (tDec === pDec) ? "#69f0ae" : "#ffd54f";
        ctx.font = "bold 13px Consolas";
        ctx.fillText(`${tDec===pDec?'✅':'👉'} 十進位密碼: ${String(tDec).padStart(2,' ')} (目前: ${String(pDec).padStart(2,' ')})`, ox + 6 * cs + 14, ry);

        ctx.textAlign = "center";
        for (let col = 0; col < 6; col++) {
            const x1 = ox + col * cs, y1 = oy + row * cs;
            const v = board[row][col];
            ctx.fillStyle = v ? (g5State.editTarget ? "#ff80ab" : "#29b6f6") : "#161925";
            ctx.strokeStyle = "#37474f"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.roundRect(x1+2, y1+2, cs-4, cs-4, 6); ctx.fill(); ctx.stroke();
            ctx.fillStyle = v ? "#111" : "#546e7a";
            ctx.font = "bold 16px Consolas";
            ctx.fillText(String(v), x1 + cs/2, y1 + cs/2);
        }
    }

    const r0 = board[0];
    const dec0 = r0.reduce((acc, v, i) => acc + v * weights[i], 0);
    const matStr = board.map(r => `    [${r.join(", ")}],`).join("\n");
    updatePythonBox(
        `# 🎨 二維矩陣 (2D List) 與二進位轉換\nmatrix = [\n${matStr}\n]\n\n# 第 0 列的二進位轉十進位：\nrow0_val = int("${r0.join("")}", 2)  # = ${dec0}`,
        "電腦中的每個黑白像素都是 <code>0</code> 或 <code>1</code>。6 個位元的二進位權重由左至右依序為 <code>32, 16, 8, 4, 2, 1</code>，例如十進位密碼 <code>12</code> 就代表 <code>8 + 4</code>（第 3、4 格為 1）！"
    );
}

function g5CanvasClick(e) {
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (720 / rect.width);
    const y = (e.clientY - rect.top) * (400 / rect.height);
    const col = Math.floor((x - 165) / 50);
    const row = Math.floor((y - 82) / 50);
    if (row < 0 || row >= 6 || col < 0 || col >= 6) return;

    if (g5State.editTarget) {
        g5State.target[row][col] = 1 - g5State.target[row][col];
        g5Draw();
        return;
    }

    g5State.player[row][col] = 1 - g5State.player[row][col];
    if (g5State.player[row][col] === 1 && g5State.target[row][col] === 0) g5State.mistakes++;
    g5Draw();

    const won = g5State.player.every((r, ri) => r.every((v, ci) => v === g5State.target[ri][ci]));
    if (won) {
        const stars = g5State.mistakes <= 2 ? 3 : (g5State.mistakes <= 6 ? 2 : 1);
        awardStars(4, appState.currentLevel, stars);
    }
}

// 啟動初始化
loadSaveData();
switchGame(0);
</script>
</body>
</html>
"""

# 渲染自適應高度的互動遊戲元件
components.html(GAME_HTML, height=820, scrolling=True)