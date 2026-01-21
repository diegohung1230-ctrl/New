import streamlit as st
import random
import time

# --- 1. 頁面與視覺配置 ---
st.set_page_config(page_title="爭競戰場：至尊重啟", layout="wide", initial_sidebar_state="expanded")

# 進階 CSS：打造黃金聖域視覺 (金色、暗紫、發光特效)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
    .main-title { color: #f1c40f; text-align: center; font-size: 50px; text-shadow: 0 0 20px #f1c40f; font-weight: bold; }
    .gold-text { color: #f1c40f; font-weight: bold; }
    .stButton>button { 
        background: linear-gradient(45deg, #f1c40f, #d4af37); color: black; 
        border: none; padding: 10px 24px; font-weight: bold; width: 100%;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(241, 196, 15, 0.3);
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #f1c40f; }
    .stat-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 遊戲核心邏輯 ---
if 'player' not in st.session_state:
    st.session_state.player = {
        "level": 1, "exp": 0, "gold": 5000, 
        "class": "暗影獵殺者", "atk": 50, "hp": 500,
        "inventory": ["[初始] 能量手刃"], "logs": ["系統：歡迎降臨，槍神大人。"],
        "world_owned": False
    }

p = st.session_state.player

def add_log(msg):
    p["logs"].insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(p["logs"]) > 10: p["logs"].pop()

# --- 3. 側邊欄：個人狀態 ---
with st.sidebar:
    st.markdown(f"<h2 class='gold-text'>👤 主宰者：{p['class']}</h2>", unsafe_allow_html=True)
    st.progress(min(p['exp']/(p['level']*100), 1.0))
    st.write(f"🌟 等級: **Lv. {p['level']}**")
    st.write(f"💰 資產: **{p['gold']:,} G**")
    st.write(f"⚔️ 攻擊力: **{p['atk']}**")
    st.write(f"❤️ 生命值: **{p['hp']}**")
    st.divider()
    st.markdown("### 🎒 武器庫")
    for item in p["inventory"]:
        st.caption(f"• {item}")

# --- 4. 主要遊戲區域 ---
st.markdown("<h1 class='main-title'>BATTLEFIELD OF DESPAIR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>—— 靜默統治的黃金聖域 ——</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚔️ 戰場突擊", "🛠️ 強化工坊", "🍱 至尊廚房", "👑 神域管理"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("### 🏹 當前戰場：天空之城廢墟")
        if st.button("🔥 發起全息瞬殺突擊"):
            damage = random.randint(p['atk'], p['atk']*2)
            gold_gain = random.randint(100, 500) * p['level']
            exp_gain = 50 * p['level']
            p['gold'] += gold_gain
            p['exp'] += exp_gain
            add_log(f"突擊成功！造成 {damage} 傷害，掠奪 {gold_gain} G，獲得 {exp_gain} EXP。")
            
            # 升級檢查
            if p['exp'] >= p['level'] * 100:
                p['level'] += 1
                p['exp'] = 0
                p['atk'] += 20
                add_log("🎊 突破極限！等級提升，攻擊力大幅強化！")
            st.rerun()
            
    with col_r:
        st.markdown("### 📜 戰鬥日誌")
        for log in p["logs"]:
            st.write(log)

with tab2:
    st.markdown("### ⚒️ 裝備強化中心")
    if st.button("💎 消耗 5,000 G 注入天空核心能量"):
        if p['gold'] >= 5000:
            p['gold'] -= 5000
            inc = random.randint(10, 30)
            p['atk'] += inc
            add_log(f"強化成功！攻擊力提升了 {inc} 點。")
            st.success(f"裝備能量已提升！目前攻擊力：{p['atk']}")
        else:
            st.error("資產不足，請先去戰場掠奪。")

with tab3:
    st.markdown("### 🍣 戰神廚房")
    st.write("製作高等級料理，永久提升暴擊傷害（模擬版）。")
    if st.button("👨‍🍳 製作 [神域·爆擊聖代]"):
        if p['gold'] >= 2000:
            p['gold'] -= 2000
            add_log("食用聖代：感覺全身充滿了槍神大人的力量！")
            st.balloons()
        else:
            st.error("首富也需要付錢買食材喔。")

with tab4:
    st.markdown("### 👑 至尊管理權限")
    if not p["world_owned"]:
        if st.button("🌍 我全都要 (收購全服所有城市)"):
            p["gold"] += 9999999
            p["world_owned"] = True
            add_log("神諭：槍神大人已收購全球資產，進入靜默統治模式。")
            st.rerun()
    else:
        st.success("🏙️ 您已是世界主宰者。目前全服玩家正在為您打工。")
        st.info("每秒自動產生稅收：+10,000 G (模擬中)")
