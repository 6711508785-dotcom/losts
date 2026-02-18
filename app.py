import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration (ต้องอยู่บนสุด)
st.set_page_config(
    page_title="Lost & Found | มินิมอล",
    page_icon="🌸",
    layout="centered"
)

# 2. Initialize Session State (ป้องกัน Error ทันทีที่เปิดแอป)
if 'items' not in st.session_state:
    st.session_state.items = [
        {"type": "ของหาย", "name": "กระเป๋าสตางค์สีดำ", "loc": "ตึกคอมพิวเตอร์", "date": "2026-02-18", "contact": "081-xxx-xxxx"},
        {"type": "พบของ", "name": "กุญแจรถยนต์", "loc": "โรงอาหาร", "date": "2026-02-17", "contact": "ติดต่อเคาน์เตอร์ประชาสัมพันธ์"}
    ]

# 3. Custom CSS สำหรับความ Minimalist และโทนชมพู
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    
    * { font-family: 'Kanit', sans-serif; }
    
    /* พื้นหลังและโทนสี */
    .stApp { background-color: #FFFFFF; }
    
    /* ปรับแต่งปุ่มให้มนและนิ่มนวล */
    div.stButton > button {
        background-color: #FFB6C1;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FF8DA1;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
    }

    /* สไตล์ Card สิ่งของ */
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #FFF9FA;
        border: 1px solid #FFE4E8;
        margin-bottom: 15px;
    }
    .badge-lost { color: #FF6B6B; font-weight: 500; font-size: 0.85rem; }
    .badge-found { color: #4CAF50; font-weight: 500; font-size: 0.85rem; }
    
    /* ปรับแต่ง Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        color: #999;
        border: none;
    }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #FFB6C1; }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนแสดงผลหน้าเว็บ ---

st.markdown("<h1 style='text-align: center; color: #FF8DA1;'>🌸 Lost & Found</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>ศูนย์รวมแจ้งของหาย-พบของที่เรียบง่ายที่สุด</p>", unsafe_allow_html=True)
st.write("")

# สร้าง Tabs
tab1, tab2 = st.tabs(["🔍 ดูประกาศทั้งหมด", "✍️ แจ้งเรื่องใหม่"])

with tab1:
    # ส่วนค้นหาแบบ Minimal
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("", placeholder="ค้นหาสิ่งของ...")
    with col2:
        filter_type = st.selectbox("", ["ทั้งหมด", "ของหาย", "พบของ"])

    st.write("---")

    # แสดงผลรายการ
    for item in st.session_state.items:
        # กรองข้อมูล
        if filter_type != "ทั้งหมด" and item['type'] != filter_type:
            continue
        if search_query.lower() not in item['name'].lower():
            continue

        badge_class = "badge-lost" if item['type'] == "ของหาย" else "badge-found"
        
        st.markdown(f"""
            <div class="card">
                <span class="{badge_class}">• {item['type']}</span>
                <h3 style="margin: 5px 0; color: #444;">{item['name']}</h3>
                <p style="margin: 0; color: #777; font-size: 0.9rem;">
                    📍 {item['loc']} | 📅 {item['date']}
                </p>
                <div style="margin-top: 10px; font-size: 0.85rem; color: #FF8DA1;">
                    📞 ติดต่อ: {item['contact']}
                </div>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h4 style='color: #FF8DA1;'>กรอกรายละเอียดสิ่งของ</h4>", unsafe_allow_html=True)
    with st.form("new_report", clear_on_submit=True):
        type_choice = st.radio("ประเภท", ["ของหาย", "พบของ"], horizontal=True)
        item_name = st.text_input("ชื่อสิ่งของ*")
        location = st.text_input("สถานที่*")
        contact_info = st.text_input("เบอร์โทรหรือช่องทางติดต่อ")
        report_date = st.date_input("วันที่", value=datetime.now())
        
        submitted = st.form_submit_button("ลงประกาศ")
        
        if submitted:
            if item_name and location:
                new_data = {
                    "type": type_choice,
                    "name": item_name,
                    "loc": location,
                    "date": str(report_date),
                    "contact": contact_info if contact_info else "ไม่ระบุ"
                }
                # เพิ่มข้อมูลไว้ด้านบนสุดของลิสต์
                st.session_state.items.insert(0, new_data)
                st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")
                st.rerun() # สั่งรีเฟรชหน้าจอเพื่อแสดงข้อมูลใหม่ทันที
            else:
                st.warning("กรุณากรอกชื่อสิ่งของและสถานที่")
