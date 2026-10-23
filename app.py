import sys
import os
import subprocess

# ==============================================================================
# 自動環境檢查與啟動器：
# 支援直接執行 `python app.py` 或 `streamlit run app.py`
# ==============================================================================
def ensure_streamlit_and_launch():
    try:
        import streamlit as st
    except ImportError:
        print("正在為您自動安裝 streamlit 套件，請稍候...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        import streamlit as st

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            print("🚀 正在啟動《星際邏輯學院》Web 音效旗艦版伺服器...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
            sys.exit(0)
    except Exception:
        pass

ensure_streamlit_and_launch()

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="星際邏輯學院 | 105關卡運算思維遊戲 (Web Audio 音效版)",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.4rem !important;
        padding-right: 0.4rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌌 星際邏輯學院 2.5")
    st.markdown("""
    **五大運算思維訓練 × 各 20 關 + 自製沙盒**
    - 🚀 **星際編碼號**：序列、迴圈、條件與蟲洞
    - ⚡ **光子邏輯閘**：AND / OR / XOR / NAND / NOR
    - ⚖️ **能量排序室**：選擇、泡泡、奇偶與山峰排序
    - 🗼 **星際河內塔**：Stack 堆疊與遞迴拆解
    - 🎨 **像素解碼器**：二進位權重與 2D 矩陣推理
    ---
    ### 🔊 純 Web Audio 合成音效系統
    - 內建 **11 種即時合成音效** 與 **多聲部勝利交響樂**（零外部音檔依賴）。
    - 可點擊右上角 **「🔊 音效」** 按鈕隨時開關聲音或開啟音效測試台。
    """)

# ==============================================================================
# 內嵌完整響應式 HTML5 + Web Audio API 合成器 + 105 關卡互動遊戲引擎
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
    .top-header {
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        background: var(--bg-panel); border: 1px solid rgba(100,181,246,0.3);
        border-radius: 14px; padding: 10px 14px; margin-bottom: 8px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.4);
        gap: 8px;
    }
    .brand-title {
        font-size: 1.2rem; font-weight: 900;
        background: linear-gradient(90deg, #ffd54f, #4dd0e1, #ff80ab);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        display: flex; align-items: center; gap: 6px;
    }
    .nav-tabs { display: flex; flex-wrap: wrap; gap: 5px; }
    .nav-btn {
        background: var(--bg-card); color: var(--text-main);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
        padding: 7px 10px; font-size: 0.86rem; font-weight: bold;
        cursor: pointer; transition: all 0.2s;
    }
    .nav-btn:hover { transform: translateY(-2px); border-color: var(--accent-cyan); }
    .nav-btn.active {
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #111; border-color: #fff; box-shadow: 0 0 12px rgba(255,213,79,0.5);
    }
    .header-controls { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .star-badge {
        background: rgba(105,240,174,0.15); border: 1px solid var(--accent-green);
        color: var(--accent-green); padding: 5px 11px; border-radius: 20px;
        font-weight: bold; font-size: 0.88rem;
    }
    .tool-btn {
        background: #37474f; color: #fff; border: 1px solid var(--accent-cyan);
        padding: 5px 10px; border-radius: 8px; cursor: pointer; font-size: 0.83rem; font-weight: bold;
        transition: 0.15s;
    }
    .tool-btn:hover { background: var(--accent-cyan); color: #111; }
    .tool-btn.muted { border-color: #ff80ab; color: #ff80ab; }

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
    .lvl-btn.custom { background: linear-gradient(135deg, #ff80ab, #f50057); color: #fff; }
    .lvl-btn.custom.active { border: 2px solid #ffd54f; box-shadow: 0 0 12px #ff80ab; }

    .main-grid {
        display: grid; grid-template-columns: 1fr 360px; gap: 12px;
        transform-origin: top center; transition: transform 0.15s ease;
    }
    @media (max-width: 960px) { .main-grid { grid-template-columns: 1fr; } }

    .stage-card, .code-card {
        background: var(--bg-panel); border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1); padding: 14px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.45);
    }
    .lvl-header-title { font-size: 1.2rem; font-weight: bold; color: var(--accent-gold); margin-bottom: 4px; }
    .lvl-header-desc { font-size: 0.92rem; color: var(--text-sub); margin-bottom: 10px; line-height: 1.4; }

    .game-flex { display: flex; flex-wrap: wrap; gap: 14px; align-items: flex-start; justify-content: center; }
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
    .block-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px; }
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

    .modal-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.75); z-index: 999; align-items: center; justify-content: center;
        padding: 16px;
    }
    .modal-box {
        background: #1a1e2e; border: 2px solid var(--accent-cyan);
        border-radius: 16px; max-width: 540px; width: 100%; padding: 20px;
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
    <div class="brand-title">🚀 星際邏輯學院 <span style="font-size:0.78rem; color:#4dd0e1;">Web Audio 交響版</span></div>
    <div class="nav-tabs" id="gameTabs">
        <button class="nav-btn active" onclick="sfx.click(); switchGame(0)">1️⃣ 星際編碼號</button>
        <button class="nav-btn" onclick="sfx.click(); switchGame(1)">2️⃣ 光子邏輯閘</button>
        <button class="nav-btn" onclick="sfx.click(); switchGame(2)">3️⃣ 能量排序室</button>
        <button class="nav-btn" onclick="sfx.click(); switchGame(3)">4️⃣ 星際河內塔</button>
        <button class="nav-btn" onclick="sfx.click(); switchGame(4)">5️⃣ 像素解碼器</button>
    </div>
    <div class="header-controls">
        <div style="display:flex; align-items:center; gap:4px; font-size:0.8rem; color:#b0bec5;">
            🔍縮放:
            <input type="range" id="zoomSlider" min="65" max="135" value="100" style="width:68px;" oninput="applyZoom(this.value)">
            <span id="zoomVal">100%</span>
        </div>
        <button class="tool-btn" id="muteBtn" onclick="sfx.toggleMute()">🔊 音效: 開</button>
        <button class="tool-btn" onclick="sfx.click(); openAudioTestModal()">🎵 試聽室</button>
        <div class="star-badge" id="totalStarsBadge">🏆 0 / 300 ⭐</div>
        <button class="tool-btn" onclick="sfx.click(); openSaveModal()">💾 存檔</button>
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
// 🎵 純 Web Audio API 數位合成音效引擎 (SpaceSynthAudio - 零外部音檔依賴)
// ============================================================================
class SpaceSynthAudio {
    constructor() {
        this.ctx = null;
        this.muted = false;
    }

    init() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
        if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
        }
    }

    toggleMute() {
        this.muted = !this.muted;
        const btn = document.getElementById("muteBtn");
        if (this.muted) {
            btn.innerText = "🔇 音效: 關";
            btn.classList.add("muted");
        } else {
            btn.innerText = "🔊 音效: 開";
            btn.classList.remove("muted");
            this.click();
        }
    }

    // 基礎單音合成器 (支援頻率滑音與 ADSR 衰減包絡)
    playTone(freqStart, freqEnd, duration, type = "sine", maxGain = 0.16, delay = 0) {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime + delay;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freqStart, now);
        if (freqEnd && freqEnd !== freqStart) {
            osc.frequency.exponentialRampToValueAtTime(Math.max(20, freqEnd), now + duration);
        }

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(maxGain, now + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + duration + 0.02);
    }

    // 1. UI 科技按鍵音
    click() {
        this.playTone(620, 920, 0.045, "triangle", 0.12);
    }

    // 2. 機器人移動步伐音效
    move() {
        this.playTone(210, 340, 0.085, "triangle", 0.18);
    }

    // 3. 機器人轉向伺服馬達音效
    turn() {
        this.playTone(330, 490, 0.075, "sine", 0.15);
    }

    // 4. 收集能量水晶清脆雙音
    crystal() {
        this.playTone(987.77, 987.77, 0.09, "sine", 0.18, 0);      // B5
        this.playTone(1318.51, 1318.51, 0.24, "triangle", 0.20, 0.07); // E6
    }

    // 5. 雷射開關與高壓邏輯閘音效
    laser() {
        this.playTone(960, 175, 0.20, "sawtooth", 0.15, 0);
        this.playTone(480, 880, 0.12, "square", 0.08, 0.04);
    }

    // 6. 蟲洞瞬間移動空間躍遷音效
    portal() {
        const notes = [261.6, 392.0, 523.2, 783.9];
        notes.forEach((f, idx) => {
            this.playTone(f, f * 1.25, 0.09, "sine", 0.16, idx * 0.045);
        });
    }

    // 7. 能量排序室：液體試管交換氣泡音
    swap() {
        this.playTone(340, 620, 0.11, "sine", 0.18, 0);
        this.playTone(520, 760, 0.09, "triangle", 0.14, 0.06);
    }

    // 8. 河內塔：拿起能量環
    pickup() {
        this.playTone(280, 460, 0.08, "sine", 0.16);
    }

    // 9. 河內塔：放下能量環
    drop() {
        this.playTone(420, 210, 0.10, "triangle", 0.18);
    }

    // 10. 像素解碼器：切換 1 或 0
    pixel(val) {
        if (val === 1) this.playTone(523.25, 659.25, 0.07, "sine", 0.15);
        else this.playTone(392.00, 293.66, 0.07, "sine", 0.12);
    }

    // 11. 錯誤與碰撞警報音 (低頻雙鋸齒波)
    error() {
        this.playTone(175, 130, 0.16, "sawtooth", 0.20, 0);
        this.playTone(145, 98, 0.26, "sawtooth", 0.22, 0.15);
    }

    // 12. 過關勝利交響樂 (多聲部和弦進行 + 三星高音禮讚)
    victory(stars = 3) {
        // 主旋律號角 (C5 -> G4 -> C5 -> E5 -> G5 -> C6)
        const melody = [
            {f: 523.25, d: 0.13, t: 0.00}, // C5
            {f: 392.00, d: 0.13, t: 0.13}, // G4
            {f: 523.25, d: 0.13, t: 0.26}, // C5
            {f: 659.25, d: 0.18, t: 0.39}, // E5
            {f: 783.99, d: 0.22, t: 0.57}, // G5
            {f: 1046.50, d: 0.55, t: 0.79} // C6
        ];
        melody.forEach(n => {
            this.playTone(n.f, n.f, n.d, "triangle", 0.20, n.t);
        });

        // 交響低音和弦襯底 (C Major 溫暖共鳴)
        const chord = [261.63, 329.63, 392.00]; // C4, E4, G4
        chord.forEach(f => {
            this.playTone(f, f, 0.45, "sine", 0.09, 0.0);
            this.playTone(f * 1.5, f * 1.5, 0.65, "sine", 0.09, 0.79);
        });

        // 若獲得 3 顆星，追加高音星塵慶祝琶音
        if (stars >= 3) {
            const sparkle = [1318.5, 1568.0, 2093.0]; // E6, G6, C7
            sparkle.forEach((f, i) => {
                this.playTone(f, f, 0.18, "sine", 0.14, 1.05 + i * 0.08);
            });
        }
    }
}

const sfx = new SpaceSynthAudio();

function openAudioTestModal() {
    showModal(`
        <h3 style="color:#ffd54f; margin-top:0;">🎵 星際 Web Audio 合成音效試聽室</h3>
        <p style="font-size:0.88rem; color:#b0bec5;">
            所有音效皆由瀏覽器透過數學波形（正弦波、三角波、鋸齒波）即時運算生成：
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:14px 0;">
            <button class="cmd-btn" style="background:#64b5f6;" onclick="sfx.move()">🤖 機器人移動音</button>
            <button class="cmd-btn" style="background:#4dd0e1;" onclick="sfx.turn()">🔄 機械轉向伺服音</button>
            <button class="cmd-btn" style="background:#ffd54f;" onclick="sfx.crystal()">💎 收集能量水晶</button>
            <button class="cmd-btn" style="background:#ff80ab;" onclick="sfx.laser()">⚡ 雷射與電路導通</button>
            <button class="cmd-btn" style="background:#b388ff;" onclick="sfx.portal()">🌀 蟲洞空間躍遷</button>
            <button class="cmd-btn" style="background:#80deea;" onclick="sfx.swap()">🧪 能量試管交換</button>
            <button class="cmd-btn" style="background:#ffb74d;" onclick="sfx.error()">💥 碰撞與錯誤警報</button>
            <button class="cmd-btn" style="background:#69f0ae;" onclick="sfx.victory(3)">🎺 過關勝利交響樂</button>
        </div>
        <button class="cmd-btn" style="background:#b0bec5; padding:8px 20px; margin:0 auto;" onclick="sfx.click(); closeModal()">關閉試聽室</button>
    `);
}

// ============================================================================
// 全域狀態與三重存檔系統 (localStorage + JSON 下載上傳 + 存檔通行碼)
// ============================================================================
const STORAGE_KEY = "STAR_LOGIC_ACADEMY_SAVE_V2";
let appState = {
    currentGame: 0,
    currentLevel: 0,
    stars: {},
    customLevels: {}
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
    sfx.victory(s);
    if (l < 20) {
        const k = `${g}_${l}`;
        appState.stars[k] = Math.max(appState.stars[k] || 0, s);
        saveProgress();
    }
    fireConfetti();
    const starIcons = "⭐".repeat(s);
    const nextBtnHtml = (l < 19)
        ? `<button class="cmd-btn" style="background:#69f0ae; padding:10px 20px; margin:8px;" onclick="sfx.click(); closeModal(); loadLevel(${l+1});">⏩ 挑戰下一關 (第 ${l+2} 關)</button>`
        : `<button class="cmd-btn" style="background:#ff80ab; padding:10px 20px; margin:8px;" onclick="sfx.click(); closeModal(); loadLevel(20);">🛠️ 前往自製創客關卡</button>`;

    showModal(`
        <h2 style="color:#ffd54f; margin-top:0;">🎉 任務大成功！</h2>
        <div style="font-size:2.5rem; margin:10px 0;">${starIcons}</div>
        <p style="color:#eceff4; font-size:1rem;">恭喜完成 <b>第 ${l+1} 關</b>！進度已自動儲存。</p>
        <div style="display:flex; justify-content:center; flex-wrap:wrap; margin-top:14px;">
            <button class="cmd-btn" style="background:#64b5f6; padding:10px 16px; margin:8px;" onclick="sfx.click(); closeModal();">🔄 留在本關最佳化</button>
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
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 14px;" onclick="sfx.click(); downloadJsonSave()">⬇️ 下載 .json 存檔</button>
            <label class="cmd-btn" style="background:#64b5f6; padding:8px 14px; cursor:pointer;">
                📂 讀取 .json 存檔
                <input type="file" accept=".json" style="display:none;" onchange="uploadJsonSave(event)">
            </label>
            <button class="cmd-btn" style="background:#ff80ab; padding:8px 14px;" onclick="sfx.error(); resetAllSave()">🗑️ 清空重來</button>
        </div>
        <div style="text-align:left; font-size:0.82rem; color:#ffd54f; margin-bottom:4px;">🔑 跨裝置存檔通行碼 (可複製貼上)：</div>
        <textarea id="saveCodeBox" style="width:100%; height:65px; background:#090b10; color:#69f0ae; border:1px solid #455a64; border-radius:6px; font-family:monospace; font-size:0.78rem; padding:6px;">${saveStr}</textarea>
        <div style="display:flex; gap:8px; justify-content:center; margin-top:10px;">
            <button class="cmd-btn" style="background:#ffd54f; padding:7px 14px;" onclick="importSaveCode()">📥 載入上方通行碼</button>
            <button class="cmd-btn" style="background:#b0bec5; padding:7px 14px;" onclick="sfx.click(); closeModal()">關閉視窗</button>
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
            sfx.victory(3);
            alert("🎉 存檔讀取成功！");
        } catch (err) { sfx.error(); alert("存檔格式錯誤！"); }
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
        sfx.victory(3);
        alert("🎉 通行碼載入成功！");
    } catch (e) { sfx.error(); alert("通行碼無效，請確認是否完整複製！"); }
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
    {name:"G1-15 之字形峽谷", opt:8, start:[1,5,0], desc:"連續 S 型彎道，考驗左
