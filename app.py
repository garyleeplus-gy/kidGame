import sys
import os
import subprocess

# 自動環境檢查：支援本地直接執行 python app.py 或雲端 streamlit run app.py
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
    .block-container { padding: 0.3rem 0.5rem 0rem 0.5rem !important; max-width: 100% !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌌 星際邏輯學院 Web 2.0")
    st.markdown("""
    - **5 大運算思維遊戲 × 各 20 關 + 自製沙盒 (共 105 關)**
    - 🖥️ **黃金比例雙欄舞台**：左側大尺寸地圖畫布、右側等高寬版動作面板、底部橫向演算法透視窗。
    - ⏳ **家長計時器**：頂部顯示「小時/分鐘/秒」倒數，時間到自動存檔並鎖定畫面（需家長授權密碼解鎖）。
    - 📱 **手機/平板適應**：可使用頂部「🔍縮放」滑桿調整大小，支援雙指縮放。
    - 💾 **跨裝置存檔**：點擊右上角「存檔」可下載 `.json` 存檔或複製通行碼。
    """)

GAME_HTML = r'''<!DOCTYPE html>
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
        margin: 0; padding: 6px 10px;
        background: radial-gradient(circle at 50% 15%, #1a1f35 0%, #0b0d14 100%);
        color: var(--text);
        font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
        overflow-x: hidden;
    }
    /* 頂部導覽列 */
    .top-header {
        display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
        background: var(--bg-panel); border: 1px solid rgba(100,181,246,0.35);
        border-radius: 12px; padding: 6px 12px; margin-bottom: 6px; gap: 8px;
    }
    .brand {
        font-size: 1.12rem; font-weight: 900;
        background: linear-gradient(90deg, #ffd54f, #4dd0e1, #ff80ab);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .nav-tabs { display: flex; flex-wrap: wrap; gap: 5px; }
    .nav-btn {
        background: var(--bg-card); color: var(--text);
        border: 1px solid rgba(255,255,255,0.12); border-radius: 8px;
        padding: 5px 10px; font-size: 0.83rem; font-weight: bold; cursor: pointer;
        transition: all 0.15s;
    }
    .nav-btn:hover { border-color: var(--cyan); }
    .nav-btn.active {
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #111; border-color: #fff;
    }
    .header-right { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
    .timer-badge {
        background: rgba(77, 208, 225, 0.15); border: 1px solid var(--cyan);
        color: var(--cyan); padding: 4px 10px; border-radius: 20px;
        font-weight: bold; font-size: 0.83rem; cursor: pointer;
        font-family: Consolas, "Microsoft JhengHei", monospace;
    }
    .timer-badge.warn {
        background: rgba(255, 183, 77, 0.2); border-color: #ffb74d; color: #ffb74d;
    }
    .timer-badge.danger {
        background: rgba(255, 64, 129, 0.25); border-color: #ff4081; color: #ff80ab;
    }
    .star-badge {
        background: rgba(105,240,174,0.15); border: 1px solid var(--green);
        color: var(--green); padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.83rem;
    }
    .tool-btn {
        background: #37474f; color: #fff; border: 1px solid var(--cyan);
        padding: 4px 9px; border-radius: 8px; cursor: pointer; font-size: 0.8rem; font-weight: bold;
    }
    .tool-btn:hover { background: var(--cyan); color: #111; }

    /* 關卡選擇列 */
    .level-bar {
        display: flex; align-items: center; gap: 5px; overflow-x: auto;
        background: var(--bg-panel); padding: 6px 10px; border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.08); margin-bottom: 8px;
    }
    .lvl-btn {
        flex: 0 0 auto; background: var(--bg-card); color: var(--sub);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 7px;
        padding: 4px 9px; font-size: 0.79rem; font-weight: bold; cursor: pointer;
    }
    .lvl-btn.active { background: var(--blue); color: #000; border-color: #fff; }
    .lvl-btn.custom { background: linear-gradient(135deg, #ff80ab, #f50057); color: #fff; }

    /* 主版面：上下垂直堆疊（上方居中大舞台 + 下方全寬 Python 演算法透視窗） */
    .main-layout {
        display: flex; flex-direction: column; gap: 10px;
        transform-origin: top center; transition: transform 0.15s ease;
    }
    .stage-card {
        background: var(--bg-panel); border-radius: 14px;
        border: 1px solid rgba(100,181,246,0.25); padding: 14px 20px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
    }
    .stage-header {
        text-align: center; margin-bottom: 12px;
    }
    .lvl-title { font-size: 1.2rem; font-weight: bold; color: var(--gold); margin-bottom: 4px; }
    .lvl-desc { font-size: 0.92rem; color: var(--sub); line-height: 1.35; }

    /* 遊戲舞台內部配置：左側大動作視窗 + 右側與紅框同尺寸的寬版動作面板 (等高對齊) */
    .game-flex {
        display: flex; flex-wrap: wrap; gap: 26px;
        align-items: stretch; justify-content: center;
    }
    canvas {
        background: #0b0e17; border-radius: 12px; border: 2px solid rgba(100,181,246,0.45);
        max-width: 100%; height: auto; touch-action: manipulation;
        box-shadow: 0 6px 20px rgba(0,0,0,0.55);
    }
    .wide-canvas {
        width: 820px; max-width: 100%; height: auto;
    }
    /* 右側動作積木面板：放大至紅框範圍 (寬 480~520px，高度與左側地圖+狀態列等高) */
    .ctrl-box {
        flex: 1 1 460px; max-width: 520px; min-height: 548px;
        background: rgba(15,17,26,0.9);
        border-radius: 14px; padding: 16px 18px;
        border: 1px solid rgba(100,181,246,0.22);
        box-shadow: 0 6px 20px rgba(0,0,0,0.45);
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .block-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 9px; margin-bottom: 10px;
    }
    .cmd-btn {
        border: none; border-radius: 9px; padding: 11px 12px;
        font-size: 0.95rem; font-weight: bold; cursor: pointer; color: #111;
        transition: transform 0.08s, filter 0.15s;
    }
    .cmd-btn:hover { filter: brightness(1.1); }
    .cmd-btn:active { transform: scale(0.96); }
    .cmd-list {
        background: #090b10; border-radius: 10px; padding: 10px 12px;
        flex: 1; min-height: 220px; max-height: 275px; overflow-y: auto;
        font-family: Consolas, "Microsoft JhengHei", monospace;
        font-size: 0.92rem; border: 1px solid #2c3146; margin-top: 6px;
        text-align: left; line-height: 1.5;
    }
    .cmd-item { padding: 4px 6px; border-radius: 5px; }
    .cmd-item.running { background: rgba(255,213,79,0.28); border-left: 4px solid var(--gold); color: #fff; font-weight: bold; }

    .status-bar {
        margin-top: 8px; padding: 9px 14px; border-radius: 9px;
        background: rgba(105,240,174,0.12); border-left: 4px solid var(--green);
        font-weight: bold; font-size: 0.9rem; color: var(--green);
        transition: all 0.2s; text-align: left;
    }
    .status-bar.err {
        background: rgba(255, 128, 171, 0.15); border-left-color: var(--pink); color: var(--pink);
    }

    /* 底部區域：全寬橫向「🐍 即時 Python 演算法透視窗」 */
    .bottom-algo-dock {
        background: var(--bg-panel); border-radius: 14px;
        border: 1px solid rgba(105, 240, 174, 0.3); padding: 10px 16px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
        display: grid; grid-template-columns: 1.6fr 1fr; gap: 14px; align-items: stretch;
    }
    @media (max-width: 860px) {
        .bottom-algo-dock { grid-template-columns: 1fr; }
    }
    .code-box {
        background: #090b10; color: #69f0ae; font-family: Consolas, monospace;
        font-size: 0.86rem; padding: 10px 12px; border-radius: 9px;
        height: 135px; overflow-y: auto; white-space: pre-wrap; border: 1px solid #2e354d;
        line-height: 1.4;
    }
    .concept-box {
        background: rgba(255,213,79,0.08);
        border: 1px solid rgba(255,213,79,0.35); border-radius: 9px;
        padding: 10px 12px; font-size: 0.86rem; color: var(--gold); line-height: 1.45;
        display: flex; align-items: center;
    }

    .modal-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.82); z-index: 999; align-items: center; justify-content: center; padding: 14px;
    }
    .modal-box {
        background: #1a1e2e; border: 2px solid var(--cyan); border-radius: 14px;
        max-width: 500px; width: 100%; padding: 18px; text-align: center;
    }
    /* 時間到鎖定全螢幕遮罩 */
    .lock-overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at center, #1b2238 0%, #07090e 100%);
        z-index: 2000; align-items: center; justify-content: center; padding: 20px;
        flex-direction: column; text-align: center;
    }
    .brush-bar {
        display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px;
        background: rgba(255,255,255,0.06); padding: 6px 10px; border-radius: 9px; justify-content: center;
    }
    .brush-btn {
        background: #2c3146; color: #fff; border: 1px solid transparent;
        padding: 4px 8px; border-radius: 6px; cursor: pointer; font-size: 0.78rem;
    }
    .brush-btn.active { border-color: var(--gold); background: #3f4765; }
    .time-input {
        width: 65px; background: #090b10; color: #69f0ae; border: 1px solid #4dd0e1;
        border-radius: 6px; padding: 6px; font-size: 1rem; text-align: center; font-weight: bold;
    }
</style>
</head>
<body>

<div class="top-header">
    <div class="brand">🚀 星際邏輯學院 <span style="font-size:0.75rem; color:#4dd0e1;">105關旗艦版</span></div>
    <div class="nav-tabs" id="gameTabs">
        <button class="nav-btn active" onclick="switchGame(0)">1️⃣ 星際編碼號</button>
        <button class="nav-btn" onclick="switchGame(1)">2️⃣ 光子邏輯閘</button>
        <button class="nav-btn" onclick="switchGame(2)">3️⃣ 能量排序室</button>
        <button class="nav-btn" onclick="switchGame(3)">4️⃣ 星際河內塔</button>
        <button class="nav-btn" onclick="switchGame(4)">5️⃣ 像素解碼器</button>
    </div>
    <div class="header-right">
        <button class="tool-btn" id="soundToggleBtn" onclick="toggleSound()">🔊 音效: 開</button>
        <div class="timer-badge" id="timerBadge" onclick="openTimerModal()" title="點擊設定家長倒數計時器">
            ⏳ 00時 30分 00秒
        </div>
        <div style="display:flex; align-items:center; gap:3px; font-size:0.8rem; color:#b0bec5;">
            🔍縮放:<input type="range" min="65" max="135" value="100" style="width:60px;" oninput="applyZoom(this.value)">
            <span id="zoomVal">100%</span>
        </div>
        <div class="star-badge" id="totalStarsBadge">🏆 0 / 300 ⭐</div>
        <button class="tool-btn" onclick="openSaveModal()">💾 存檔</button>
    </div>
</div>

<div class="level-bar" id="levelBar"></div>

<!-- 主工作區：上方為居中大動作舞台與右側大面板，下方為橫向 Python 演算法透視窗 -->
<div class="main-layout" id="mainGrid">
    <div class="stage-card" id="mainStageCard">
        <div class="stage-header">
            <div class="lvl-title" id="lvlTitle">載入關卡中...</div>
            <div class="lvl-desc" id="lvlDesc"></div>
        </div>
        <div id="stageContent"></div>
    </div>

    <!-- 底部：即時 Python 演算法透視窗 -->
    <div class="bottom-algo-dock">
        <div>
            <div style="font-size:0.95rem; font-weight:bold; color:#69f0ae; margin-bottom:5px;">
                🐍 即時 Python 演算法透視窗 <span style="font-size:0.78rem; color:#b0bec5; font-weight:normal;">（你的每一步操作都會即時轉譯成真正的 Python 程式碼）</span>
            </div>
            <div class="code-box" id="pythonPreview"></div>
        </div>
        <div style="display:flex; flex-direction:column; justify-content:center;">
            <div class="concept-box" id="conceptBox"></div>
        </div>
    </div>
</div>

<!-- 一般彈跳視窗 -->
<div class="modal-overlay" id="modalOverlay"><div class="modal-box" id="modalContent"></div></div>

<!-- 家長計時器時間到鎖定與關閉畫面 (密碼完全隱藏) -->
<div class="lock-overlay" id="lockOverlay">
    <div style="max-width:480px; background:#181c2b; border:2px solid #ffd54f; border-radius:18px; padding:28px;">
        <div style="font-size:3.5rem; margin-bottom:8px;">⏰</div>
        <h2 style="color:#ffd54f; margin:0 0 10px 0;">今日遊玩時間已到！</h2>
        <p style="color:#69f0ae; font-weight:bold; font-size:1rem; margin-bottom:8px;">
            ✅ 系統已自動為您完成闖關進度存檔並匯出備份！
        </p>
        <p style="color:#b0bec5; font-size:0.9rem; line-height:1.5; margin-bottom:18px;">
            優秀的太空工程師也需要讓眼睛休息喔！請離開螢幕遠眺休息。<br>
            （若家長需延長使用時間，請由家長輸入授權密碼解鎖）
        </p>
        <div style="display:flex; gap:8px; justify-content:center; align-items:center; flex-wrap:wrap;">
            <input type="password" id="unlockPinInput" placeholder="請輸入家長授權密碼" style="background:#090b10; color:#fff; border:1px solid #4dd0e1; border-radius:8px; padding:8px 12px; width:175px; text-align:center;">
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 16px;" onclick="parentUnlockTime()">🔓 延長 30 分鐘</button>
        </div>
        <div style="margin-top:12px;">
            <button class="cmd-btn" style="background:#64b5f6; padding:7px 14px; font-size:0.82rem;" onclick="downloadJsonSave()">⬇️ 再次下載 .json 存檔備份</button>
        </div>
    </div>
</div>

<!-- 過關專用慶祝煙火 Canvas (僅在過關 awardStars 時啟動，平時完全隱藏不干擾操作) -->
<canvas id="confettiCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:3000; display:none;"></canvas>

<script>
const NL = String.fromCharCode(10);
const STORAGE_KEY = "STAR_LOGIC_ACADEMY_SAVE_V3";
const TIMER_KEY = "STAR_LOGIC_PARENT_TIMER_V3";
// 家長預設密碼修正為 8888，且不顯示於任何 UI 文字中
const PARENT_PIN = "8888";

let appState = { currentGame: 0, currentLevel: 0, stars: {}, customLevels: {} };
let timerState = { remainingSec: 1800, active: true, intervalId: null };

// ============================================================================
// Web Audio API 太空音效合成器
// ============================================================================
let audioCtx = null;
let soundEnabled = true;

function getAudioCtx() {
    if (!soundEnabled) return null;
    try {
        if (!audioCtx) {
            const AC = window.AudioContext || window.webkitAudioContext;
            if (AC) audioCtx = new AC();
        }
        if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
        return audioCtx;
    } catch (e) { return null; }
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    const btn = document.getElementById("soundToggleBtn");
    if (soundEnabled) {
        btn.innerText = "🔊 音效: 開";
        btn.style.borderColor = "#4dd0e1";
        sfxClick();
    } else {
        btn.innerText = "🔇 音效: 關";
        btn.style.borderColor = "#ff80ab";
    }
}

function playTone(freq, type, duration, vol, slideFreq) {
    const ctx = getAudioCtx();
    if (!ctx) return;
    try {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type || "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        if (slideFreq) osc.frequency.exponentialRampToValueAtTime(slideFreq, ctx.currentTime + duration);
        gain.gain.setValueAtTime(vol || 0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
    } catch (e) {}
}

function sfxClick() { playTone(620, "triangle", 0.06, 0.09, 780); }
function sfxStep() { playTone(360, "sine", 0.07, 0.08, 440); }
function sfxTurn() { playTone(460, "triangle", 0.08, 0.08, 350); }
function sfxCrystal() {
    playTone(987.77, "sine", 0.1, 0.14);
    setTimeout(function() { playTone(1318.5, "sine", 0.18, 0.15); }, 80);
}
function sfxLaser() { playTone(820, "sawtooth", 0.18, 0.1, 260); }
function sfxPortal() { playTone(300, "sine", 0.22, 0.12, 960); }
function sfxSwap() { playTone(500, "sine", 0.1, 0.12, 740); }
function sfxError() { playTone(165, "sawtooth", 0.24, 0.15, 115); }
function sfxWin() {
    const notes = [523.25, 659.25, 783.99, 1046.5, 1318.5];
    notes.forEach(function(n, idx) {
        setTimeout(function() { playTone(n, "triangle", 0.25, 0.18); }, idx * 105);
    });
}

document.addEventListener("pointerdown", function() { getAudioCtx(); }, { once: true });

// ============================================================================
// 過關專用全螢幕慶祝煙火 (僅在過關 awardStars 時呼叫)
// ============================================================================
let confettiParticles = [];
let confettiAnimId = null;

function fireConfetti() {
    const cvs = document.getElementById("confettiCanvas");
    cvs.style.display = "block";
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    confettiParticles = [];
    const colors = ["#ffd54f","#69f0ae","#64b5f6","#ff80ab","#b388ff","#4dd0e1"];
    for (let w = 0; w < 3; w++) {
        const cx = cvs.width * (0.25 + w * 0.25);
        const cy = cvs.height * 0.32;
        for (let i = 0; i < 32; i++) {
            const ang = Math.random() * Math.PI * 2;
            const spd = Math.random() * 7 + 2;
            confettiParticles.push({
                x: cx, y: cy,
                vx: Math.cos(ang) * spd,
                vy: Math.sin(ang) * spd - 2,
                r: Math.random() * 5 + 3,
                c: colors[Math.floor(Math.random() * colors.length)],
                alpha: 1.1
            });
        }
    }
    if (confettiAnimId) cancelAnimationFrame(confettiAnimId);
    const ctx = cvs.getContext("2d");
    function step() {
        ctx.clearRect(0, 0, cvs.width, cvs.height);
        for (let i = confettiParticles.length - 1; i >= 0; i--) {
            const p = confettiParticles[i];
            p.x += p.vx; p.y += p.vy; p.vy += 0.18; p.alpha -= 0.02;
            if (p.alpha <= 0) { confettiParticles.splice(i, 1); continue; }
            ctx.save();
            ctx.globalAlpha = Math.min(1, p.alpha);
            ctx.fillStyle = p.c;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
            ctx.restore();
        }
        if (confettiParticles.length > 0) {
            confettiAnimId = requestAnimationFrame(step);
        } else {
            confettiAnimId = null;
            cvs.style.display = "none";
        }
    }
    confettiAnimId = requestAnimationFrame(step);
}

// ============================================================================
// 家長倒數計時器核心邏輯 (時/分/秒 顯示 + 自動存檔關閉 + 預設密碼 8888 隱藏)
// ============================================================================
function initParentalTimer() {
    try {
        const savedTimer = window.localStorage.getItem(TIMER_KEY);
        if (savedTimer) {
            const p = JSON.parse(savedTimer);
            if (typeof p.remainingSec === "number") timerState.remainingSec = p.remainingSec;
            if (typeof p.active === "boolean") timerState.active = p.active;
        }
    } catch (e) {}

    if (timerState.remainingSec <= 0 && timerState.active) {
        triggerTimeUpLock(false);
    } else {
        updateTimerBadgeUI();
        startTimerLoop();
    }
}

function saveTimerState() {
    try {
        window.localStorage.setItem(TIMER_KEY, JSON.stringify({
            remainingSec: timerState.remainingSec,
            active: timerState.active
        }));
    } catch (e) {}
}

function formatHMS(totalSec) {
    const s = Math.max(0, Math.floor(totalSec));
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = s % 60;
    return String(hrs).padStart(2, "0") + "時 " + String(mins).padStart(2, "0") + "分 " + String(secs).padStart(2, "0") + "秒";
}

function updateTimerBadgeUI() {
    const badge = document.getElementById("timerBadge");
    if (!badge) return;
    if (!timerState.active) {
        badge.innerText = "⏳ 計時器: 暫停中";
        badge.className = "timer-badge";
        return;
    }
    badge.innerText = "⏳ " + formatHMS(timerState.remainingSec);
    if (timerState.remainingSec <= 60) badge.className = "timer-badge danger";
    else if (timerState.remainingSec <= 300) badge.className = "timer-badge warn";
    else badge.className = "timer-badge";
}

function startTimerLoop() {
    if (timerState.intervalId) clearInterval(timerState.intervalId);
    timerState.intervalId = setInterval(function() {
        if (!timerState.active) return;
        if (timerState.remainingSec > 0) {
            timerState.remainingSec--;
            updateTimerBadgeUI();
            if (timerState.remainingSec > 0 && timerState.remainingSec <= 10) {
                playTone(880, "sine", 0.05, 0.06);
            }
            if (timerState.remainingSec % 5 === 0) saveTimerState();
            if (timerState.remainingSec <= 0) triggerTimeUpLock(true);
        }
    }, 1000);
}

function triggerTimeUpLock(autoDownload) {
    if (timerState.intervalId) clearInterval(timerState.intervalId);
    g1StopTimer();
    timerState.remainingSec = 0;
    saveTimerState();
    saveProgress();
    updateTimerBadgeUI();
    sfxError();
    if (autoDownload) { try { downloadJsonSave(); } catch (e) {} }
    document.getElementById("lockOverlay").style.display = "flex";
    try { window.close(); } catch (e) {}
}

function parentUnlockTime() {
    const pin = document.getElementById("unlockPinInput").value.trim();
    if (pin !== PARENT_PIN) {
        sfxError();
        alert("⚠️ 家長授權密碼錯誤！");
        return;
    }
    sfxWin();
    document.getElementById("unlockPinInput").value = "";
    timerState.remainingSec = 1800;
    timerState.active = true;
    saveTimerState();
    document.getElementById("lockOverlay").style.display = "none";
    updateTimerBadgeUI();
    startTimerLoop();
}

function openTimerModal() {
    sfxClick();
    const curS = Math.max(0, timerState.remainingSec);
    const h = Math.floor(curS / 3600);
    const m = Math.floor((curS % 3600) / 60);
    const s = curS % 60;

    showModal(`
        <h3 style="color:#ffd54f; margin-top:0;">⏳ 家長護眼計時器設定</h3>
        <p style="font-size:0.85rem; color:#b0bec5; line-height:1.4;">
            設定今日允許的總遊玩時數（<b>小時 / 分鐘 / 秒</b>）。<br>
            倒數結束時將<b>自動儲存進度、匯出備份並關閉鎖定畫面</b>。
        </p>
        <div style="display:flex; justify-content:center; align-items:center; gap:6px; margin:14px 0;">
            <input type="number" id="tHr" class="time-input" min="0" max="12" value="${h}"> <span>小時</span>
            <input type="number" id="tMin" class="time-input" min="0" max="59" value="${m}"> <span>分鐘</span>
            <input type="number" id="tSec" class="time-input" min="0" max="59" value="${s}"> <span>秒</span>
        </div>
        <div style="display:flex; gap:6px; justify-content:center; margin-bottom:12px; flex-wrap:wrap;">
            <button class="brush-btn" onclick="setQuickTime(0,15,0)">快速：15分鐘</button>
            <button class="brush-btn" onclick="setQuickTime(0,30,0)">快速：30分鐘</button>
            <button class="brush-btn" onclick="setQuickTime(1,0,0)">快速：1小時</button>
            <button class="brush-btn" onclick="setQuickTime(0,0,10)">測試：10秒鐘</button>
        </div>
        <div style="margin-bottom:12px;">
            <input type="password" id="parentPinSet" placeholder="請輸入家長授權密碼" style="background:#090b10; color:#fff; border:1px solid #4dd0e1; border-radius:6px; padding:7px 10px; width:190px; text-align:center;">
        </div>
        <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 16px;" onclick="applyTimerSetting(true)">▶️ 啟動倒數計時</button>
            <button class="cmd-btn" style="background:#ffb74d; padding:8px 14px;" onclick="applyTimerSetting(false)">⏸️ 暫停計時器</button>
            <button class="cmd-btn" style="background:#b0bec5; padding:8px 14px;" onclick="closeModal()">取消</button>
        </div>
    `);
}

function setQuickTime(h, m, s) {
    sfxClick();
    document.getElementById("tHr").value = h;
    document.getElementById("tMin").value = m;
    document.getElementById("tSec").value = s;
}

function applyTimerSetting(enableFlag) {
    const pin = document.getElementById("parentPinSet").value.trim();
    if (pin !== PARENT_PIN) {
        sfxError();
        alert("⚠️ 家長授權密碼錯誤！無法變更計時器設定。");
        return;
    }
    const h = Math.max(0, parseInt(document.getElementById("tHr").value) || 0);
    const m = Math.max(0, parseInt(document.getElementById("tMin").value) || 0);
    const s = Math.max(0, parseInt(document.getElementById("tSec").value) || 0);
    const total = h * 3600 + m * 60 + s;

    if (enableFlag && total <= 0) {
        alert("請設定至少 1 秒以上的倒數時間！");
        return;
    }
    sfxClick();
    timerState.remainingSec = total;
    timerState.active = enableFlag;
    saveTimerState();
    updateTimerBadgeUI();
    if (enableFlag) startTimerLoop();
    closeModal();
}

// ============================================================================
// 乾淨幾何繪圖函式與存檔核心
// ============================================================================
function drawRoundBox(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
}

function loadSaveData() {
    try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
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
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify({ stars: appState.stars, customLevels: appState.customLevels }));
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
    sfxWin();
    fireConfetti();
    const nextBtn = (l < 19)
        ? `<button class="cmd-btn" style="background:#69f0ae; padding:9px 18px; margin:6px;" onclick="closeModal(); loadLevel(${l+1});">⏩ 下一關 (第 ${l+2} 關)</button>`
        : `<button class="cmd-btn" style="background:#ff80ab; padding:9px 18px; margin:6px;" onclick="closeModal(); loadLevel(20);">🛠️ 自製創客關卡</button>`;
    showModal(`
        <h2 style="color:#ffd54f; margin:0;">🎉 闖關大成功！</h2>
        <div style="font-size:2.5rem; margin:10px 0;">${"⭐".repeat(s)}</div>
        <p style="color:#eceff4;">恭喜完成 <b>第 ${l+1} 關</b>！進度已自動儲存。</p>
        <div>
            <button class="cmd-btn" style="background:#64b5f6; padding:9px 14px; margin:6px;" onclick="closeModal();">🔄 留在本關</button>
            ${nextBtn}
        </div>
    `);
}

function updateTotalStarsUI() {
    let total = 0;
    for (let g = 0; g < 5; g++) {
        for (let l = 0; l < 20; l++) {
            total += (appState.stars[g + "_" + l] || 0);
        }
    }
    document.getElementById("totalStarsBadge").innerText = "🏆 " + total + " / 300 ⭐";
}

function applyZoom(val) {
    document.getElementById("zoomVal").innerText = val + "%";
    document.getElementById("mainGrid").style.transform = "scale(" + (val / 100) + ")";
}

function openSaveModal() {
    sfxClick();
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
            saveProgress(); loadLevel(appState.currentLevel); closeModal(); sfxWin();
        } catch (err) { sfxError(); alert("存檔格式錯誤！"); }
    };
    r.readAsText(f);
}

function importSaveCode() {
    try {
        const d = JSON.parse(decodeURIComponent(atob(document.getElementById("saveCodeBox").value.trim())));
        if (d.stars) appState.stars = d.stars;
        if (d.customLevels) appState.customLevels = d.customLevels;
        saveProgress(); loadLevel(appState.currentLevel); closeModal(); sfxWin();
    } catch (e) { sfxError(); alert("通行碼無效！"); }
}

function resetAllSave() {
    if (confirm("確定要清空所有星章紀錄嗎？")) {
        appState.stars = {}; appState.customLevels = {};
        saveProgress(); loadLevel(appState.currentLevel); closeModal();
    }
}

function showModal(html) { document.getElementById("modalContent").innerHTML = html; document.getElementById("modalOverlay").style.display = "flex"; }
function closeModal() { sfxClick(); document.getElementById("modalOverlay").style.display = "none"; }

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
    {name:"G1-09 折返解鎖", opt:9, start:[1,3,1], desc:"開關在上方小房間，進去按完開關後轉彎出來繼續前進！", grid:["1111111","1115111","1112111","1020423","1111111","1111111","1111111"]},
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
    sfxClick();
    g1StopTimer(); appState.currentGame = gIdx;
    document.querySelectorAll("#gameTabs .nav-btn").forEach((b, i) => b.classList.toggle("active", i === gIdx));
    loadLevel(0);
}

function renderLevelBar() {
    let html = "";
    for (let i = 0; i < 21; i++) {
        const isC = (i === 20), isA = (i === appState.currentLevel);
        const st = appState.stars[appState.currentGame + "_" + i] || 0;
        const lbl = isC ? "🛠️ 自製關卡" : "第" + (i+1) + "關" + (st ? " " + "★".repeat(st) : "");
        html += `<button class="lvl-btn ${isC?'custom':''} ${isA?'active':''}" onclick="sfxClick(); loadLevel(${i})">${lbl}</button>`;
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
    document.getElementById("conceptBox").innerHTML = "<div>💡 <b>運算思維小百科：</b><br>" + tip + "</div>";
}

// ============================================================================
// 遊戲 1：🚀 星際編碼號 (左側 504x504 大視窗 + 右側紅框大尺寸等高動作面板)
// ============================================================================
const G1_CS = 72;
const G1_CANVAS_SIZE = 504;
let g1State = {
    cmds: [], grid: [], rx:1, ry:5, rdir:0, laserOn:true, gotC:0, totalC:0,
    timer:null, brush:1, trace:[], localFx:null
};
function g1StopTimer() { if (g1State.timer) { clearTimeout(g1State.timer); g1State.timer = null; } }

function initGame1(lIdx) {
    if (lIdx === 20 && appState.customLevels.g1) G1_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g1));
    const lvl = G1_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = "🚀 " + lvl.name + " 【⭐⭐⭐ 黃金目標：" + lvl.opt + " 個有效積木】";
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
        <div style="display:flex; flex-direction:column; justify-content:space-between;">
            <canvas id="g1Canvas" width="${G1_CANVAS_SIZE}" height="${G1_CANVAS_SIZE}"></canvas>
            <div class="status-bar" id="g1Status" style="width:${G1_CANVAS_SIZE}px; max-width:100%;">🤖 機器人就緒！請在右側點擊積木編排程式。</div>
            ${customHtml}
        </div>
        <div class="ctrl-box">
            <div>
                <div style="font-size:1rem; font-weight:bold; color:#4dd0e1; margin-bottom:10px; text-align:left;">🧩 動作積木面板：</div>
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
                <div style="display:flex; gap:8px; margin-bottom:12px;">
                    <button class="cmd-btn" style="background:#69f0ae; flex:1.6;" onclick="g1Run()">▶️ 執行</button>
                    <button class="cmd-btn" style="background:#ffb74d; flex:1;" onclick="g1Pop()">⌫ 退回</button>
                    <button class="cmd-btn" style="background:#ff80ab; flex:1;" onclick="g1Clear()">🗑️ 清空</button>
                </div>
            </div>
            <div style="display:flex; flex-direction:column; flex:1;">
                <div style="font-size:0.9rem; color:#ffd54f; font-weight:bold; text-align:left;" id="g1CmdHeader"></div>
                <div class="cmd-list" id="g1CmdList"></div>
            </div>
        </div>
    </div>`;
    document.getElementById("g1Canvas").addEventListener("click", g1CanvasClick);
    g1ResetBoard(); g1RenderCmds(-1);
}

function g1SetBrush(b, el) {
    sfxClick(); g1State.brush = b;
    document.querySelectorAll("#g1BrushBar .brush-btn").forEach(x => x.classList.remove("active"));
    el.classList.add("active");
}

function g1CanvasClick(e) {
    if (appState.currentLevel !== 20 || g1State.timer) return;
    sfxClick();
    const r = e.target.getBoundingClientRect();
    const gx = Math.floor((e.clientX - r.left) * (G1_CANVAS_SIZE / r.width) / G1_CS);
    const gy = Math.floor((e.clientY - r.top) * (G1_CANVAS_SIZE / r.height) / G1_CS);
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
        saveProgress();
        g1ResetBoard();
        g1State.localFx = { x: gx, y: gy, color: "#ffd54f", text: "✏️已修改" };
        g1Draw();
    }
}

function g1ResetBoard() {
    g1StopTimer();
    const lvl = G1_LEVELS[appState.currentLevel];
    g1State.grid = lvl.grid.map(r => r.split("").map(Number));
    g1State.rx = lvl.start[0]; g1State.ry = lvl.start[1]; g1State.rdir = lvl.start[2];
    g1State.laserOn = true; g1State.gotC = 0;
    g1State.trace = [[g1State.rx, g1State.ry]];
    g1State.localFx = null;
    let cnt = 0;
    for (let y=0; y<7; y++) for (let x=0; x<7; x++) if (g1State.grid[y][x] === 2) cnt++;
    g1State.totalC = cnt;
    const stBar = document.getElementById("g1Status");
    if (stBar) stBar.className = "status-bar";
    g1Draw();
}

function g1Draw() {
    const cvs = document.getElementById("g1Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"), cs = G1_CS, half = cs / 2;
    ctx.clearRect(0, 0, G1_CANVAS_SIZE, G1_CANVAS_SIZE);
    const icons = {1:"🪨", 2:"💎", 3:"🛸", 5:"🔘", 6:"🌀"};
    for (let y = 0; y < 7; y++) {
        for (let x = 0; x < 7; x++) {
            const x1 = x * cs, y1 = y * cs, cell = g1State.grid[y][x];
            ctx.fillStyle = (cell === 4 && g1State.laserOn) ? "#3b1222" : ((x+y)%2===0 ? "#141827" : "#0e111d");
            ctx.fillRect(x1, y1, cs, cs);
            ctx.strokeStyle = "#232942"; ctx.strokeRect(x1, y1, cs, cs);
            ctx.font = "30px 'Segoe UI Emoji', sans-serif";
            ctx.textAlign = "center"; ctx.textBaseline = "middle";
            if (icons[cell]) {
                ctx.fillText(icons[cell], x1 + half, y1 + half);
            } else if (cell === 4 && g1State.laserOn) {
                ctx.strokeStyle = "#ff4081"; ctx.lineWidth = 3.5;
                ctx.beginPath(); ctx.moveTo(x1+4, y1 + half); ctx.lineTo(x1+cs-4, y1 + half); ctx.stroke();
                ctx.lineWidth = 1;
                ctx.fillText("⚡", x1 + half, y1 + half);
            }
        }
    }

    // 繪製局部步進軌跡虛線
    if (g1State.trace.length > 1) {
        ctx.save();
        ctx.strokeStyle = "rgba(100, 181, 246, 0.7)";
        ctx.lineWidth = 4.5;
        ctx.setLineDash([7, 5]);
        for (let i = 0; i < g1State.trace.length - 1; i++) {
            const [x1, y1] = g1State.trace[i];
            const [x2, y2] = g1State.trace[i+1];
            if (Math.abs(x1 - x2) + Math.abs(y1 - y2) === 1) {
                ctx.beginPath();
                ctx.moveTo(x1 * cs + half, y1 * cs + half);
                ctx.lineTo(x2 * cs + half, y2 * cs + half);
                ctx.stroke();
            }
        }
        ctx.restore();
    }

    // 繪製單格局部動作回饋
    if (g1State.localFx) {
        const fx = g1State.localFx;
        const cx = fx.x * cs + half;
        ctx.save();
        ctx.strokeStyle = fx.color;
        ctx.lineWidth = 3.5;
        ctx.strokeRect(fx.x * cs + 3, fx.y * cs + 3, cs - 6, cs - 6);
        if (fx.text) {
            const tagY = fyTop(fx.y, cs);
            ctx.fillStyle = "rgba(9, 11, 16, 0.88)";
            ctx.fillRect(cx - 28, tagY, 56, 20);
            ctx.fillStyle = fx.color;
            ctx.font = "bold 12px 'Microsoft JhengHei'";
            ctx.textAlign = "center"; ctx.textBaseline = "middle";
            ctx.fillText(fx.text, cx, tagY + 10);
        }
        ctx.restore();
    }

    // 繪製機器人與清楚的面向箭頭
    const rx = g1State.rx * cs + half, ry = g1State.ry * cs + half;
    ctx.beginPath(); ctx.arc(rx, ry, 24, 0, Math.PI*2);
    ctx.fillStyle = "#29b6f6"; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = "#fff"; ctx.stroke();
    ctx.font = "25px 'Segoe UI Emoji', sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("🤖", rx, ry);

    const dirs = [[0,-1],[1,0],[0,1],[-1,0]], arrs = ["▲","▶","▼","◀"];
    const dx = dirs[g1State.rdir][0], dy = dirs[g1State.rdir][1];
    ctx.beginPath(); ctx.arc(rx+dx*25, ry+dy*25, 9, 0, Math.PI*2);
    ctx.fillStyle = "#ff4081"; ctx.fill();
    ctx.font = "bold 11px Consolas"; ctx.fillStyle = "#fff";
    ctx.fillText(arrs[g1State.rdir], rx+dx*25, ry+dy*25);
}

function fyTop(gy, cs) { return gy > 0 ? (gy * cs - 11) : (gy * cs + cs - 20); }

function g1Add(c) { if (!g1State.timer && g1State.cmds.length < 24) { sfxClick(); g1State.cmds.push(c); g1RenderCmds(-1); } }
function g1Pop() { if (!g1State.timer && g1State.cmds.length > 0) { sfxClick(); g1State.cmds.pop(); g1RenderCmds(-1); } }
function g1Clear() { if (!g1State.timer) { sfxClick(); g1State.cmds = []; g1ResetBoard(); g1RenderCmds(-1); } }

function g1RenderCmds(actIdx) {
    const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
    const opt = G1_LEVELS[appState.currentLevel].opt;
    document.getElementById("g1CmdHeader").innerText = "📋 有效積木：" + eff + " 個 (目標：" + opt + " 個)";
    let html = "", py = ["# 🚀 星際編碼號 Python 腳本", "import space_bot as bot", ""], ind = 0;
    const m = { MOVE:["⬆️ 前進","bot.move()"], LEFT:["↩️ 左轉","bot.turn_left()"], RIGHT:["↪️ 右轉","bot.turn_right()"], SWITCH:["👆 開關","bot.trigger_switch()"] };
    g1State.cmds.forEach((c, i) => {
        const cls = (i === actIdx) ? "cmd-item running" : "cmd-item";
        if (c === "END_LOOP") { ind = Math.max(0, ind-1); html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}🔚 結束重複</div>`; }
        else if (c.startsWith("LOOP_")) {
            const n = c.split("_")[1];
            html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}🔄 重複 ${n} 次:</div>`;
            py.push("    ".repeat(ind) + "for _ in range(" + n + "):"); ind++;
        } else {
            html += `<div class="${cls}">${i+1}. ${"&nbsp;&nbsp;".repeat(ind)}${m[c][0]}</div>`;
            py.push("    ".repeat(ind) + m[c][1]);
        }
    });
    document.getElementById("g1CmdList").innerHTML = html || "<div style='color:#607d8b;'>尚未加入指令...</div>";
    updatePythonBox(py.join(NL), "使用 <code>for _ in range(N):</code> 迴圈能把重複的路線濃縮成幾行程式碼，輕鬆拿下 3 星！");
}

function g1Compile(cmds) {
    function parse(i) {
        let out = [];
        while (i < cmds.length) {
            const c = cmds[i];
            if (c === "END_LOOP") return [out, i+1];
            if (c.startsWith("LOOP_")) {
                const n = parseInt(c.split("_")[1]);
                const res = parse(i+1);
                for (let k = 0; k < n; k++) out.push(...res[0]);
                i = res[1];
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
    const stBar = document.getElementById("g1Status");
    let idx = 0;
    function step() {
        if (idx >= q.length) {
            g1State.timer = null; g1RenderCmds(-1);
            if (g1State.grid[g1State.ry][g1State.rx] === 3 && g1State.gotC === g1State.totalC) {
                g1State.localFx = { x: g1State.rx, y: g1State.ry, color: "#69f0ae", text: "🛸抵達!" };
                g1Draw();
                const eff = g1State.cmds.filter(c => c !== "END_LOOP").length;
                const opt = G1_LEVELS[appState.currentLevel].opt;
                awardStars(0, appState.currentLevel, eff <= opt ? 3 : (eff <= opt+2 ? 2 : 1));
            } else {
                sfxError();
                stBar.className = "status-bar err";
                stBar.innerText = "🤔 還沒收集完水晶 (" + g1State.gotC + "/" + g1State.totalC + ") 或還沒抵達太空船喔！";
            }
            return;
        }
        const item = q[idx]; g1RenderCmds(item.line);
        const dirs = [[0,-1],[1,0],[0,1],[-1,0]];
        const dirNames = ["北(上)", "東(右)", "南(下)", "西(左)"];

        if (item.act === "LEFT") {
            sfxTurn();
            g1State.rdir = (g1State.rdir + 3) % 4;
            g1State.localFx = { x: g1State.rx, y: g1State.ry, color: "#4dd0e1", text: "↩️左轉" };
            stBar.innerText = "↩️ 向左轉！目前面向：" + dirNames[g1State.rdir];
        }
        else if (item.act === "RIGHT") {
            sfxTurn();
            g1State.rdir = (g1State.rdir + 1) % 4;
            g1State.localFx = { x: g1State.rx, y: g1State.ry, color: "#4dd0e1", text: "↪️右轉" };
            stBar.innerText = "↪️ 向右轉！目前面向：" + dirNames[g1State.rdir];
        }
        else if (item.act === "SWITCH") {
            if (g1State.grid[g1State.ry][g1State.rx] === 5) {
                sfxLaser();
                g1State.laserOn = !g1State.laserOn;
                g1State.localFx = { x: g1State.rx, y: g1State.ry, color: "#ffd54f", text: g1State.laserOn ? "🔴開啟" : "🟢解除" };
                stBar.innerText = "👆 觸發開關！雷射門已" + (g1State.laserOn ? "開啟" : "解除");
            } else {
                sfxError();
                g1State.localFx = { x: g1State.rx, y: g1State.ry, color: "#ffb74d", text: "❓無開關" };
            }
        }
        else if (item.act === "MOVE") {
            const dx = dirs[g1State.rdir][0], dy = dirs[g1State.rdir][1], nx = g1State.rx + dx, ny = g1State.ry + dy;
            if (nx<0 || nx>=7 || ny<0 || ny>=7 || g1State.grid[ny][nx]===1 || (g1State.grid[ny][nx]===4 && g1State.laserOn)) {
                g1State.timer = null;
                sfxError();
                const errX = Math.max(0, Math.min(6, nx)), errY = Math.max(0, Math.min(6, ny));
                g1State.localFx = { x: errX, y: errY, color: "#ff4081", text: "💥阻擋!" };
                g1Draw();
                stBar.className = "status-bar err";
                stBar.innerText = "💥 在座標 (" + errX + "," + errY + ") 撞上障礙物或雷射！請調整積木。";
                return;
            }
            sfxStep();
            g1State.rx = nx; g1State.ry = ny;
            g1State.trace.push([nx, ny]);
            g1State.localFx = { x: nx, y: ny, color: "#64b5f6", text: "" };
            stBar.innerText = "⬆️ 前進一步至 (" + nx + "," + ny + ") | 水晶：" + g1State.gotC + "/" + g1State.totalC;

            if (g1State.grid[ny][nx] === 2) {
                g1State.grid[ny][nx] = 0; g1State.gotC++;
                sfxCrystal();
                g1State.localFx = { x: nx, y: ny, color: "#69f0ae", text: "+1💎" };
                stBar.innerText = "💎 收集到能量水晶！ (" + g1State.gotC + "/" + g1State.totalC + ")";
            }
            else if (g1State.grid[ny][nx] === 6) {
                sfxPortal();
                outer: for (let py=0; py<7; py++) for (let px=0; px<7; px++) {
                    if (g1State.grid[py][px] === 6 && (px !== nx || py !== ny)) {
                        g1State.rx = px; g1State.ry = py;
                        g1State.trace.push([px, py]);
                        g1State.localFx = { x: px, y: py, color: "#b388ff", text: "🌀躍遷" };
                        stBar.innerText = "🌀 透過蟲洞瞬間移動至 (" + px + "," + py + ")！";
                        break outer;
                    }
                }
            }
        }
        g1Draw(); idx++; g1State.timer = setTimeout(step, 340);
    }
    step();
}

// ============================================================================
// 遊戲 2：⚡ 光子邏輯閘
// ============================================================================
let g2State = { inVals: [0,0,0,0], clicks: 0, finalOut: 0, lastChangedIdx: -1 };

function initGame2(lIdx) {
    if (lIdx === 20 && appState.customLevels.g2) G2_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g2));
    const lvl = G2_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = "⚡ " + lvl.name;
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g2State.inVals = [0,0,0,0]; g2State.clicks = 0; g2State.lastChangedIdx = -1;
    document.getElementById("stageContent").innerHTML = `<div style="max-width:820px; margin:0 auto; text-align:center;">
        <canvas id="g2Canvas" class="wide-canvas" width="700" height="360"></canvas>
        <div class="status-bar" id="g2Status" style="margin-bottom:8px;">
            ⚡ 請點擊左側開關切換 0 與 1，觀察邏輯閘輸出變化。
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="font-size:0.84rem; color:#4dd0e1;">💡 【AND】全1才1 ｜ 【OR】有1就1 ｜ 【XOR】不同才1 ｜ 【NAND】不全1就1 ｜ 【NOR】全0才1</div>
            <button class="cmd-btn" style="background:#69f0ae; padding:8px 18px; font-size:0.9rem;" onclick="g2CheckWin()">✅ 驗證並啟動核心</button>
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
    const lvl = G2_LEVELS[appState.currentLevel];
    const A = g2State.inVals[0], B = g2State.inVals[1], C = g2State.inVals[2], D = g2State.inVals[3];
    const out1 = g2Calc(lvl.g1, A, B);
    const out2 = (lvl.ins === 4) ? g2Calc(lvl.g2, C, D) : 0;
    const finalOut = (lvl.ins === 4) ? g2Calc(lvl.g3, out1, out2) : out1;
    g2State.finalOut = finalOut;

    const cvs = document.getElementById("g2Canvas"); if (!cvs) return;
    const ctx = cvs.getContext("2d"); ctx.clearRect(0, 0, 700, 360);
    const ys = (lvl.ins === 4) ? [65, 145, 225, 305] : [120, 245];

    function wire(x1, y1, x2, y2, v) {
        ctx.strokeStyle = v ? "#69f0ae" : "#37474f"; ctx.lineWidth = v ? 4.5 : 2.5;
        const mx = (x1+x2)/2;
        ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(mx,y1); ctx.lineTo(mx,y2); ctx.lineTo(x2,y2); ctx.stroke();
        if (v) {
            ctx.fillStyle = "#ffd54f";
            ctx.beginPath(); ctx.arc(mx, (y1+y2)/2, 4.5, 0, Math.PI*2); ctx.fill();
        }
    }
    function gate(x, y, w, h, t, v) {
        ctx.fillStyle = v ? "#1565c0" : "#263238"; ctx.strokeStyle = v ? "#69f0ae" : "#78909c"; ctx.lineWidth = 2.5;
        drawRoundBox(ctx, x, y, w, h, 10);
        ctx.fillStyle = "#fff"; ctx.font = "bold 14px 'Microsoft JhengHei'"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(t + " 閘", x+w/2, y+h/2-9);
        ctx.fillStyle = v ? "#ffd54f" : "#b0bec5"; ctx.fillText("OUT = " + v, x+w/2, y+h/2+11);
    }

    if (lvl.ins === 2) {
        wire(145, 120, 280, 168, A); wire(145, 245, 280, 198, B);
        gate(280, 140, 125, 85, lvl.g1, out1); wire(405, 182, 545, 182, finalOut);
    } else {
        wire(145, 65, 245, 95, A); wire(145, 145, 245, 120, B); gate(245, 68, 115, 75, lvl.g1, out1);
        wire(145, 225, 245, 255, C); wire(145, 305, 245, 280, D); gate(245, 228, 115, 75, lvl.g2, out2);
        wire(360, 105, 435, 170, out1); wire(360, 265, 435, 200, out2); gate(435, 148, 115, 75, lvl.g3, finalOut);
        wire(550, 185, 590, 185, finalOut);
    }

    for (let i = 0; i < lvl.ins; i++) {
        const y = ys[i], v = g2State.inVals[i];
        const isLast = (g2State.lastChangedIdx === i);
        ctx.fillStyle = v ? "#69f0ae" : "#263238";
        ctx.strokeStyle = isLast ? "#ffd54f" : "#fff";
        ctx.lineWidth = isLast ? 3.5 : 2;
        drawRoundBox(ctx, 25, y-22, 120, 44, 9);
        ctx.fillStyle = v ? "#111" : "#fff"; ctx.font = "bold 14px 'Microsoft JhengHei'";
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText("開關 " + ["A","B","C","D"][i] + " = " + v, 85, y);
        if (isLast) {
            ctx.fillStyle = "#ffd54f"; ctx.font = "bold 12px sans-serif";
            ctx.fillText("▶", 14, y);
        }
    }

    const cy = (lvl.ins === 2) ? 182 : 185;
    ctx.beginPath(); ctx.arc(635, cy, 42, 0, Math.PI*2);
    ctx.fillStyle = finalOut ? "#ffd54f" : "#263238"; ctx.fill();
    ctx.lineWidth = 4; ctx.strokeStyle = finalOut ? "#69f0ae" : "#546e7a"; ctx.stroke();
    ctx.fillStyle = finalOut ? "#111" : "#eceff4";
    ctx.fillText("🎯核心", 635, cy-10); ctx.fillText("OUT=" + finalOut, 635, cy+12);

    const py = [
        "# ⚡ 布林邏輯電路模擬",
        "A, B, C, D = " + A + ", " + B + ", " + C + ", " + D,
        "gate1 = calc_" + lvl.g1 + "(A, B) # -> " + out1
    ];
    if (lvl.ins === 4) {
        py.push("gate2 = calc_" + lvl.g2 + "(C, D) # -> " + out2);
        py.push("core  = calc_" + lvl.g3 + "(gate1, gate2) # -> " + finalOut);
    } else {
        py.push("core  = gate1 # -> " + finalOut);
    }
    updatePythonBox(py.join(NL), "學會推演 <code>AND</code>、<code>OR</code>、<code>XOR</code>、<code>NAND</code>、<code>NOR</code> 真值表，能幫你寫出嚴密的程式條件判斷！");
}

function g2CanvasClick(e) {
    const lvl = G2_LEVELS[appState.currentLevel], r = e.target.getBoundingClientRect();
    const x = (e.clientX - r.left) * (700 / r.width), y = (e.clientY - r.top) * (360 / r.height);
    const ys = (lvl.ins === 4) ? [65, 145, 225, 305] : [120, 245];
    const stBar = document.getElementById("g2Status");

    for (let i = 0; i < lvl.ins; i++) {
        if (x >= 25 && x <= 145 && y >= ys[i]-22 && y <= ys[i]+22) {
            g2State.inVals[i] = 1 - g2State.inVals[i];
            g2State.clicks++;
            g2State.lastChangedIdx = i;
            sfxClick();
            g2EvalAndDraw();
            stBar.className = "status-bar";
            stBar.innerText = "👆 動作回饋：切換「開關 " + ["A","B","C","D"][i] + "」為 " + g2State.inVals[i] + " ➔ 核心目前輸出 OUT = " + g2State.finalOut;
            return;
        }
    }
    if (appState.currentLevel === 20) {
        const ts = ["AND","OR","XOR","NAND","NOR"];
        if (x>=245 && x<=360 && y>=68 && y<=143) lvl.g1 = ts[(ts.indexOf(lvl.g1)+1)%5];
        else if (x>=245 && x<=360 && y>=228 && y<=303) lvl.g2 = ts[(ts.indexOf(lvl.g2)+1)%5];
        else if (x>=435 && x<=550 && y>=148 && y<=223) lvl.g3 = ts[(ts.indexOf(lvl.g3)+1)%5];
        sfxLaser();
        appState.customLevels.g2 = JSON.parse(JSON.stringify(lvl)); saveProgress(); g2EvalAndDraw();
    }
}

function g2CheckWin() {
    const lvl = G2_LEVELS[appState.currentLevel];
    const stBar = document.getElementById("g2Status");
    if (g2State.finalOut !== 1) {
        sfxError(); stBar.className = "status-bar err";
        stBar.innerText = "⚠️ 驗證未通過：右側的能量核心目前還是 0（未點亮）喔！"; return;
    }
    const cnt = g2State.inVals.slice(0, lvl.ins).reduce((a,b)=>a+b, 0);
    if (lvl.rule === "EXACT_1" && cnt !== 1) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：必須剛好開啟 1 個開關（目前開啟 " + cnt + " 個）！"; return; }
    if (lvl.rule === "EXACT_2" && cnt !== 2) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：必須剛好開啟 2 個開關（目前開啟 " + cnt + " 個）！"; return; }
    if (lvl.rule === "EXACT_3" && cnt !== 3) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：必須剛好開啟 3 個開關（目前開啟 " + cnt + " 個）！"; return; }
    if (lvl.rule === "AT_LEAST_1" && cnt < 1) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：至少要開啟 1 個開關！"; return; }
    if (lvl.rule === "MAX_3" && cnt > 3) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：最多只能開啟 3 個開關！"; return; }
    if (appState.currentLevel === 14 && g2State.inVals[0] !== 1) { sfxError(); stBar.className="status-bar err"; stBar.innerText="⚠️ 限制未達成：開關 A 必須是開啟狀態！"; return; }
    awardStars(1, appState.currentLevel, g2State.clicks <= 4 ? 3 : (g2State.clicks <= 7 ? 2 : 1));
}

// ============================================================================
// 遊戲 3：⚖️ 能量排序室
// ============================================================================
let g3State = { arr: [], sel: null, swaps: 0, lastSwapPair: null };

function initGame3(lIdx) {
    if (lIdx === 20 && appState.customLevels.g3) G3_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g3));
    const lvl = G3_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = "⚖️ " + lvl.name + " 【⭐⭐⭐ 黃金目標：" + lvl.opt + " 次交換內】";
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g3State.arr = [...lvl.arr]; g3State.sel = null; g3State.swaps = 0; g3State.lastSwapPair = null;

    const customHtml = (lIdx === 20) ? `<div class="brush-bar">
        <input id="g3CustomIn" value="${lvl.arr.join(' ')}" style="background:#090b10; color:#fff; border:1px solid #4dd0e1; border-radius:6px; padding:4px 8px; width:160px;">
        <button class="brush-btn active" onclick="g3ApplyCustom()">套用數列</button>
        <button class="brush-btn" onclick="g3ToggleAdj()">相鄰限制: ${lvl.adj?'開':'關'}</button>
    </div>` : "";

    document.getElementById("stageContent").innerHTML = `<div style="max-width:820px; margin:0 auto; text-align:center;">
        <canvas id="g3Canvas" class="wide-canvas" width="700" height="340"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; gap:8px;">
            <div class="status-bar" id="g3Status" style="margin:0; flex:1;">已交換：0 次 （點擊兩瓶能量管交換位置）</div>
            <button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="sfxClick(); initGame3(${lIdx})">🔄 重置</button>
        </div>
        ${customHtml}
    </div>`;
    document.getElementById("g3Canvas").addEventListener("click", g3CanvasClick);
    g3Draw("# 尚未執行交換");
}

function g3ApplyCustom() {
    sfxClick();
    const raw = document.getElementById("g3CustomIn").value.trim().split(" ").filter(x => x !== "").map(Number).filter(n => n>=5 && n<=99).slice(0,8);
    if (raw.length >= 3) { G3_LEVELS[20].arr = raw; appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20])); saveProgress(); initGame3(20); }
}
function g3ToggleAdj() { sfxClick(); G3_LEVELS[20].adj = !G3_LEVELS[20].adj; appState.customLevels.g3 = JSON.parse(JSON.stringify(G3_LEVELS[20])); saveProgress(); initGame3(20); }

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
    ctx.fillText("🎯 目標排列：[ " + target.join(", ") + " ]", 350, 22);

    if (g3State.lastSwapPair) {
        const [i1, i2] = g3State.lastSwapPair;
        const cx1 = sx + i1 * w + w / 2;
        const cx2 = sx + i2 * w + w / 2;
        const midX = (cx1 + cx2) / 2;
        ctx.save();
        ctx.strokeStyle = "#ffd54f"; ctx.lineWidth = 2.5; ctx.setLineDash([5, 3]);
        ctx.beginPath();
        ctx.moveTo(cx1, 68);
        ctx.quadraticCurveTo(midX, 34, cx2, 68);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = "#ffd54f"; ctx.font = "bold 12px 'Microsoft JhengHei'";
        ctx.fillText("⇄ 剛交換 [" + i1 + "] 與 [" + i2 + "]", midX, 44);
        ctx.restore();
    }

    g3State.arr.forEach((v, i) => {
        const x1 = sx + i*w + 10, bw = w - 20, bh = Math.floor((v/maxV)*170) + 35, y2 = 292, y1 = y2 - bh;
        const isSel = (g3State.sel === i), isOk = (v === target[i]);
        const isSwapped = g3State.lastSwapPair && (g3State.lastSwapPair[0] === i || g3State.lastSwapPair[1] === i);

        ctx.fillStyle = isSel ? "#ffd54f" : (isOk ? "#00e676" : "#29b6f6");
        ctx.strokeStyle = isSel ? "#fff" : (isSwapped ? "#ffd54f" : "#90caf9");
        ctx.lineWidth = (isSel || isSwapped) ? 3 : 1.5;
        drawRoundBox(ctx, x1, y1, bw, bh, 8);

        ctx.fillStyle = isSel ? "#ffd54f" : "#fff";
        ctx.font = "bold 15px Consolas"; ctx.fillText(String(v), x1+bw/2, y1-12);
        ctx.fillStyle = isSwapped ? "#ffd54f" : "#4dd0e1";
        ctx.font = "bold 12px sans-serif"; ctx.fillText("[" + i + "]", x1+bw/2, y2+20);
        if (isOk) {
            ctx.fillStyle = "#0b0e17"; ctx.font = "bold 14px Consolas";
            ctx.fillText("✓", x1+bw/2, y2-14);
        }
    });
    const py = [
        "# ⚖️ 陣列排序演算法",
        "potions = [" + g3State.arr.join(", ") + "]",
        "target  = [" + target.join(", ") + "]",
        "",
        code
    ];
    updatePythonBox(py.join(NL), "Python 交換陣列元素只需一行：<code>a[i], a[j] = a[j], a[i]</code>！");
}

function g3CanvasClick(e) {
    const r = e.target.getBoundingClientRect(), x = (e.clientX - r.left) * (700 / r.width);
    const n = g3State.arr.length, w = Math.floor(620 / n), sx = 40 + Math.floor((620 - w*n)/2);
    const idx = Math.floor((x - sx) / w); if (idx < 0 || idx >= n) return;
    const stBar = document.getElementById("g3Status");

    if (g3State.sel === null) {
        sfxClick(); g3State.sel = idx;
        stBar.className = "status-bar";
        stBar.innerText = "👉 已選取索引 [" + idx + "] (數值 " + g3State.arr[idx] + ")，請點擊另一瓶進行交換。";
        g3Draw("# 選取 potions[" + idx + "]");
    }
    else if (g3State.sel === idx) {
        sfxClick(); g3State.sel = null;
        stBar.innerText = "已取消選取（目前已交換：" + g3State.swaps + " 次）";
        g3Draw("# 取消選取");
    }
    else {
        const i = g3State.sel, j = idx, lvl = G3_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(i - j) !== 1) {
            sfxError();
            stBar.className = "status-bar err";
            stBar.innerText = "⚠️ 泡泡排序限制：只能交換「相鄰（隔壁）」的兩瓶能量液喔！";
            g3State.sel = null; g3Draw("# 違反相鄰限制"); return;
        }
        const tmp = g3State.arr[i]; g3State.arr[i] = g3State.arr[j]; g3State.arr[j] = tmp;
        g3State.swaps++; g3State.sel = null;
        g3State.lastSwapPair = [Math.min(i, j), Math.max(i, j)];
        sfxSwap();
        stBar.className = "status-bar";
        stBar.innerText = "⇄ 成功交換 [" + i + "] 與 [" + j + "]！ (累計交換：" + g3State.swaps + " 次)";
        g3Draw("potions[" + i + "], potions[" + j + "] = potions[" + j + "], potions[" + i + "]");
        const t = g3GetTarget();
        if (g3State.arr.every((v, k) => v === t[k])) awardStars(2, appState.currentLevel, g3State.swaps <= lvl.opt ? 3 : (g3State.swaps <= lvl.opt+2 ? 2 : 1));
    }
}

// ============================================================================
// 遊戲 4：🗼 星際河內塔
// ============================================================================
let g4State = { pegs: [], sel: null, moves: 0, totalDisks: 0, lastMoveArc: null };

function initGame4(lIdx) {
    if (lIdx === 20 && appState.customLevels.g4) G4_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g4));
    const lvl = G4_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = "🗼 " + lvl.name + " 【⭐⭐⭐ 黃金目標：" + lvl.opt + " 步內】";
    document.getElementById("lvlDesc").innerText = lvl.desc;
    g4State.pegs = JSON.parse(JSON.stringify(lvl.pegs)); g4State.sel = null; g4State.moves = 0; g4State.lastMoveArc = null;
    let dCnt = 0;
    g4State.pegs.forEach(p => dCnt += p.length);
    g4State.totalDisks = dCnt;

    const customHtml = (lIdx === 20) ? `<div class="brush-bar">
        <button class="brush-btn" onclick="g4Custom(2,null)">2環</button>
        <button class="brush-btn" onclick="g4Custom(3,null)">3環</button>
        <button class="brush-btn" onclick="g4Custom(4,null)">4環</button>
        <button class="brush-btn" onclick="g4Custom(5,null)">5環</button>
        <button class="brush-btn" onclick="g4Custom(null,'PEGS')">3柱/4柱</button>
        <button class="brush-btn" onclick="g4Custom(null,'ADJ')">相鄰限制</button>
    </div>` : "";

    document.getElementById("stageContent").innerHTML = `<div style="max-width:820px; margin:0 auto; text-align:center;">
        <canvas id="g4Canvas" class="wide-canvas" width="700" height="340"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; gap:8px;">
            <div class="status-bar" id="g4Status" style="margin:0; flex:1;">步數：0 步 （點擊來源柱取出頂端環，再點目標柱放入）</div>
            <button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="sfxClick(); initGame4(${lIdx})">🔄 重置</button>
        </div>
        ${customHtml}
    </div>`;
    document.getElementById("g4Canvas").addEventListener("click", g4CanvasClick);
    g4Draw("# 點擊柱子進行 pop() 與 append()");
}

function g4Custom(nD, tType) {
    sfxClick();
    const lvl = G4_LEVELS[20];
    let curN = nD || 3, pC = lvl.pegs.length;
    if (!nD) { curN = 0; lvl.pegs.forEach(p => curN += p.length); }
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

    if (g4State.lastMoveArc) {
        const {src, dst, disk} = g4State.lastMoveArc;
        const x1 = sp * src + sp / 2, x2 = sp * dst + sp / 2, midX = (x1 + x2) / 2;
        ctx.save();
        ctx.strokeStyle = "#4dd0e1"; ctx.lineWidth = 2.5; ctx.setLineDash([5, 4]);
        ctx.beginPath(); ctx.moveTo(x1, 78); ctx.quadraticCurveTo(midX, 26, x2, 78); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = "#4dd0e1"; ctx.font = "bold 12px 'Microsoft JhengHei'"; ctx.textAlign = "center";
        ctx.fillText("環" + disk + ": " + pN[src] + " ➔ " + pN[dst], midX, 38);
        ctx.restore();
    }

    g4State.pegs.forEach((st, idx) => {
        const cx = sp * idx + sp / 2, isSel = (g4State.sel === idx), isT = (idx === lvl.target);
        ctx.fillStyle = isT ? "#69f0ae" : "#455a64"; ctx.fillRect(cx-65, 290, 130, 12);
        ctx.fillStyle = isSel ? "#ffd54f" : "#37474f"; ctx.fillRect(cx-6, 90, 12, 200);
        ctx.fillStyle = isT ? "#69f0ae" : "#eceff4"; ctx.font = "bold 13px sans-serif"; ctx.textAlign = "center";
        ctx.fillText(isT ? "🎯 " + pN[idx] + "(終點)" : pN[idx], cx, 320);

        st.forEach((d, sPos) => {
            const isTop = (sPos === st.length - 1);
            const w = 20 + d * 14, y2 = 288 - sPos * 30 - (isSel && isTop ? 18 : 0);
            const isJustMoved = g4State.lastMoveArc && g4State.lastMoveArc.dst === idx && isTop;
            ctx.fillStyle = cols[(d-1)%cols.length];
            ctx.strokeStyle = (isSel && isTop) || isJustMoved ? "#ffd54f" : "#fff";
            ctx.lineWidth = (isSel && isTop) || isJustMoved ? 3.5 : 2;
            drawRoundBox(ctx, cx-w, y2-26, w*2, 26, 7);
            ctx.fillStyle = "#111"; ctx.font = "bold 12px sans-serif"; ctx.fillText("環 " + d, cx, y2-13);
        });
    });
    const py = ["# 🗼 堆疊 (Stack) 與遞迴"];
    g4State.pegs.forEach((s, i) => py.push("stack_" + ["A","B","C","D"][i] + " = [" + s.join(", ") + "]"));
    py.push(""); py.push(code);
    updatePythonBox(py.join(NL), "柱子就是 <b>Stack（後進先出）</b>：只能從頂端 <code>pop()</code> 取出或 <code>append()</code> 放入！");
}

function g4CanvasClick(e) {
    const r = e.target.getBoundingClientRect(), x = (e.clientX - r.left) * (700 / r.width);
    const numP = g4State.pegs.length, idx = Math.floor(x / (700 / numP));
    if (idx < 0 || idx >= numP) return;
    const stBar = document.getElementById("g4Status");
    const pL = ["A","B","C","D"];

    if (g4State.sel === null) {
        if (g4State.pegs[idx].length) {
            sfxClick(); g4State.sel = idx;
            const topD = g4State.pegs[idx][g4State.pegs[idx].length-1];
            stBar.className = "status-bar";
            stBar.innerText = "👆 已拿起 " + pL[idx] + " 柱頂端的「環 " + topD + "」，請點擊目標柱子放入。";
            g4Draw("# 選取 stack_" + pL[idx] + " 頂端環 " + topD);
        }
    }
    else if (g4State.sel === idx) {
        sfxClick(); g4State.sel = null;
        stBar.innerText = "已放下能量環（目前步數：" + g4State.moves + " 步）";
        g4Draw("# 取消選取");
    }
    else {
        const src = g4State.sel, dst = idx, lvl = G4_LEVELS[appState.currentLevel];
        if (lvl.adj && Math.abs(src - dst) !== 1) {
            sfxError(); stBar.className = "status-bar err";
            stBar.innerText = "⚠️ 相鄰移動限制：每次只能移到隔壁相鄰的柱子喔！";
            g4State.sel = null; g4Draw("# 違反相鄰限制"); return;
        }
        const disk = g4State.pegs[src][g4State.pegs[src].length-1], top = g4State.pegs[dst][g4State.pegs[dst].length-1];
        if (top !== undefined && top < disk) {
            sfxError(); stBar.className = "status-bar err";
            stBar.innerText = "⚠️ 違反堆疊規則：大環（環 " + disk + "）不能壓在小環（環 " + top + "）上面！";
            g4State.sel = null; g4Draw("# 違反大小規則"); return;
        }
        g4State.pegs[src].pop(); g4State.pegs[dst].push(disk); g4State.moves++; g4State.sel = null;
        g4State.lastMoveArc = { src: src, dst: dst, disk: disk };
        sfxSwap();
        stBar.className = "status-bar";
        stBar.innerText = "✅ 將「環 " + disk + "」從 " + pL[src] + " 柱移至 " + pL[dst] + " 柱 (累計：" + g4State.moves + " 步)";
        g4Draw("d = stack_" + pL[src] + ".pop()" + NL + "stack_" + pL[dst] + ".append(d)");
        if (g4State.pegs[lvl.target].length === g4State.totalDisks) awardStars(3, appState.currentLevel, g4State.moves <= lvl.opt ? 3 : (g4State.moves <= lvl.opt+4 ? 2 : 1));
    }
}

// ============================================================================
// 遊戲 5：🎨 像素解碼器
// ============================================================================
let g5State = { target: [], player: [], editTarget: false, mistakes: 0, lastCell: null };

function initGame5(lIdx) {
    if (lIdx === 20 && appState.customLevels.g5) G5_LEVELS[20] = JSON.parse(JSON.stringify(appState.customLevels.g5));
    const lvl = G5_LEVELS[lIdx];
    document.getElementById("lvlTitle").innerText = "🎨 " + lvl.name + " 【二進位權重與 2D 矩陣解碼】";
    document.getElementById("lvlDesc").innerText = "根據上方「連續亮格數」與右側「二進位加總密碼 (32, 16, 8, 4, 2, 1)」，點擊格子切換 0 與 1！";
    g5State.target = lvl.grid.map(r => r.split("").map(Number));
    g5State.player = Array.from({length:6}, ()=>[0,0,0,0,0,0]);
    g5State.editTarget = false; g5State.mistakes = 0; g5State.lastCell = null;

    const customBtn = (lIdx === 20) ? `<button class="cmd-btn" id="g5CreatorBtn" style="background:#ff80ab; padding:7px 14px;" onclick="g5ToggleCreator()">🎨 繪製自訂謎題</button>` : "";
    document.getElementById("stageContent").innerHTML = `<div style="max-width:820px; margin:0 auto; text-align:center;">
        <canvas id="g5Canvas" class="wide-canvas" width="700" height="375"></canvas>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; gap:8px;">
            <div class="status-bar" id="g5Status" style="margin:0; flex:1;">💡 點擊方格切換 0 與 1，當整列或整行密碼吻合時會變成綠色 ✅！</div>
            <div style="display:flex; gap:6px;">${customBtn}<button class="cmd-btn" style="background:#ffb74d; padding:7px 14px;" onclick="sfxClick(); initGame5(${lIdx})">🗑️ 清空</button></div>
        </div>
    </div>`;
    document.getElementById("g5Canvas").addEventListener("click", g5CanvasClick);
    g5Draw();
}

function g5ToggleCreator() {
    sfxClick();
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
        ctx.font = "bold 12px sans-serif"; ctx.fillText("連續:" + g5RLE(tC), cx, 24);
        ctx.fillStyle = "#ffd54f"; ctx.font = "bold 12px Consolas"; ctx.fillText("(" + wts[c] + ")", cx, 52);
    }

    for (let r = 0; r < 6; r++) {
        const ry = oy + r*cs + cs/2, tR = g5State.target[r], pR = board[r];
        const tD = tR.reduce((a,v,i)=>a+v*wts[i],0), pD = pR.reduce((a,v,i)=>a+v*wts[i],0);
        ctx.textAlign = "right"; ctx.fillStyle = tR.every((v,i)=>v===pR[i]) ? "#69f0ae" : "#eceff4";
        ctx.font = "bold 12px sans-serif"; ctx.fillText("列[" + r + "] 連續: " + g5RLE(tR), ox-10, ry);

        ctx.textAlign = "left"; ctx.fillStyle = (tD===pD) ? "#69f0ae" : "#ffd54f";
        ctx.font = "bold 13px Consolas";
        ctx.fillText((tD===pD?"✅":"👉") + " 密碼:" + String(tD).padStart(2," ") + " (目前:" + String(pD).padStart(2," ") + ")", ox+6*cs+12, ry);

        ctx.textAlign = "center";
        for (let c = 0; c < 6; c++) {
            const x1 = ox + c*cs, y1 = oy + r*cs, v = board[r][c];
            const isLast = g5State.lastCell && g5State.lastCell.r === r && g5State.lastCell.c === c;
            ctx.fillStyle = v ? (g5State.editTarget ? "#ff80ab" : "#29b6f6") : "#161925";
            ctx.strokeStyle = isLast ? "#ffd54f" : (v ? "#fff" : "#37474f");
            ctx.lineWidth = isLast ? 3 : 1.8;
            drawRoundBox(ctx, x1+2, y1+2, cs-4, cs-4, 6);
            ctx.fillStyle = v ? "#111" : "#546e7a"; ctx.font = "bold 15px Consolas";
            ctx.fillText(String(v), x1+cs/2, y1+cs/2);

            if (isLast) {
                ctx.fillStyle = v ? "#ffd54f" : "#ff80ab";
                ctx.font = "bold 10px Consolas";
                ctx.fillText((v ? "+" : "-") + wts[c], x1 + cs - 14, y1 + 11);
            }
        }
    }
    const r0 = board[0], d0 = r0.reduce((a,v,i)=>a+v*wts[i],0);
    const py = ["# 🎨 二維陣列與二進位", "matrix = ["];
    board.forEach(r => py.push("  [" + r.join(", ") + "],"));
    py.push("]");
    py.push("row0_dec = int('" + r0.join("") + "', 2) # = " + d0);
    updatePythonBox(py.join(NL), "6 位元二進位權重由左至右為 <code>32, 16, 8, 4, 2, 1</code>，把亮起格子的權重加起來就是十進位密碼！");
}

function g5CanvasClick(e) {
    const rect = e.target.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (700 / rect.width), y = (e.clientY - rect.top) * (375 / rect.height);
    const c = Math.floor((x - 160) / 48), r = Math.floor((y - 72) / 48);
    if (r < 0 || r >= 6 || c < 0 || c >= 6) return;
    const wts = [32, 16, 8, 4, 2, 1];
    const stBar = document.getElementById("g5Status");

    if (g5State.editTarget) {
        sfxClick(); g5State.target[r][c] = 1 - g5State.target[r][c];
        g5State.lastCell = { r: r, c: c };
        g5Draw(); return;
    }

    g5State.player[r][c] = 1 - g5State.player[r][c];
    g5State.lastCell = { r: r, c: c };
    const newVal = g5State.player[r][c];

    if (newVal === 1 && g5State.target[r][c] === 0) {
        g5State.mistakes++;
        sfxClick();
    } else {
        sfxClick();
    }
    const rowSum = g5State.player[r].reduce((a,v,i)=>a+v*wts[i], 0);
    stBar.className = "status-bar";
    stBar.innerText = "👆 點擊座標 [" + r + "][" + c + "] 切換為 " + newVal + " (權重 " + (newVal ? "+" : "-") + wts[c] + ") ➔ 第 " + r + " 列目前總和：" + rowSum;
    g5Draw();

    if (g5State.player.every((row, ri) => row.every((v, ci) => v === g5State.target[ri][ci]))) {
        awardStars(4, appState.currentLevel, g5State.mistakes <= 2 ? 3 : (g5State.mistakes <= 6 ? 2 : 1));
    }
}

loadSaveData();
initParentalTimer();
switchGame(0);
</script>
</body>
</html>'''

components.html(GAME_HTML, height=920, scrolling=True)
# === 檔案結束 (請確認複製到此行) ===
