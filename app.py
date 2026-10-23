import sys
import os
import json
import subprocess

# 自動偵測環境：支援本地直接執行 python app.py 或雲端 streamlit run app.py
def ensure_streamlit():
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
            sys.exit(0)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
        sys.exit(0)

ensure_streamlit()

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="星際邏輯學院 | 105關卡運算思維遊戲", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container { padding: 0.4rem !important; max-width: 100% !important; }
    header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 105 關卡完整資料庫 (5 款遊戲 × 20 關 + 1 創客自製關卡)
# ==============================================================================
LEVEL_DATA = {
    "g1": [
        {"name":"G1-01 直線啟航","opt":2,"start":[1,5,0],"desc":"用「🔄重複 4 次」搭配「⬆️前進」收集水晶直達太空船！","grid":["1111111","1311111","1211111","1211111","1211111","1011111","1111111"]},
        {"name":"G1-02 右轉彎道","opt":5,"start":[1,5,0],"desc":"先往上走 4 步，向右轉，再往前走 3 步抵達太空船！","grid":["1111111","1222311","1211111","1211111","1211111","1011111","1111111"]},
        {"name":"G1-03 雙重轉角","opt":7,"start":[1,5,1],"desc":"機器人面向右方！先往右、再往上、最後往左抵達終點。","grid":["1111111","1132211","1111211","1111211","1111211","1022211","1111111"]},
        {"name":"G1-04 星際階梯","opt":5,"start":[1,5,0],"desc":"把「前進 ➔ 右轉 ➔ 前進 ➔ 左轉」放進重複 3 次迴圈！","grid":["1111111","1111111","1110311","1102111","1021111","1011111","1111111"]},
        {"name":"G1-05 四階長梯","opt":5,"start":[1,5,0],"desc":"更長的階梯！同樣的 4 個動作，改用「🔄重複 4 次」一次解決！","grid":["1111111","1111031","1110211","1102111","1021111","1011111","1111111"]},
        {"name":"G1-06 環狀巡航","opt":7,"start":[1,5,0],"desc":"沿著正方形外圍收集水晶，善用兩段迴圈！","grid":["1111111","1222221","1211121","1211121","1211121","1011131","1111111"]},
        {"name":"G1-07 雷射初體驗","opt":6,"start":[1,3,1],"desc":"先走到「🔘開關」格執行「👆觸發開關」，即可解除紅色雷射！","grid":["1111111","1111111","1111111","1025423","1111111","1111111","1111111"]},
        {"name":"G1-08 雷射支線","opt":8,"start":[1,5,0],"desc":"先直走去最上方按下雷射開關，再轉彎通過雷射門！","grid":["1111111","1522431","1211111","1211111","1211111","1011111","1111111"]},
        {"name":"G1-09 折返解鎖","opt":9,"start":[1,3,1],"desc":"開關在上方房間，進去按完開
