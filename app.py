import streamlit as st
import pandas as pd
from datetime import datetime

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="Lost & Found | ศูนย์แจ้งของหาย", page_icon="🔍", layout="centered")

# --- Custom CSS สำหรับคุมโทนชมพู-ขาว ---
st.markdown("""
    <style>
    /* เปลี่ยนสีพื้นหลังหลัก */
    .stApp {
        background-color: #fff5f7;
    }
    /* ปรับแต่งปุ่ม */
    div.stButton > button {
        background-color: #ff85a2;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #ff6b8e;
        color: white;
    }
    /* ปรับแต่งหัวข้อ */
    h1, h2, h3 {
        color: #ff85a2 !important;
    }
    /* ปรับแต่ง Card */
    .item-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff85a2;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัวของ Web App ---
st.title("🔍 Lost & Found Center")
st.subheader("ศูนย์รวมแจ้งของหายและของที่เก็บได้")

# --- Tabs สำหรับเมนูหลัก ---
tab1, tab2, tab3 = st.tabs(["🏠 หน้าแรก", "📝 แจ้งเรื่องใหม่", "📊 สถิติ"])

# --- จำลองฐานข้อมูล (ในที่นี้ใช้ List ธรรมดา - ถ้าใช้จริงแนะนำให้เชื่อม Google Sheets) ---
if 'items' not in st.session_state:
    st.session_state.items = [
        {"type": "ของหาย", "name": "กระเป๋าสตางค์สีดำ", "loc": "ตึก A", "date": "2026-02-18"},
        {"type": "พบของ", "name": "กุญแจรถยนต์", "loc": "ลานจอดรถ", "date": "2026-02-17"}
    ]

# --- Tab 1: หน้าแรก (แสดงรายการ) ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 ค้นหาสิ่งของ...", placeholder="เช่น กุญแจ, กระเป๋า")
    with col2:
        filter_type = st.selectbox("ประเภท", ["ทั้งหมด", "ของหาย", "พบของ"])

    st.write("---")
    
    for item in st.session_state.items:
        # กรองข้อมูล
        if filter_type != "ทั้งหมด" and item['type'] != filter_type:
            continue
        if search.lower() not in item['name'].lower():
            continue
            
        # แสดงผลในรูปแบบ Card
        st.markdown(f"""
            <div class="item-card">
                <span style="color: {'#ff4b4b' if item['type'] == 'ของหาย' else '#28a745'}; font-weight: bold;">
                    [{item['type']}]
                </span>
                <h4 style="margin: 5px 0;">{item['name']}</h4>
                <p style="font-size: 0.9em; color: #666;">
                    📍 สถานที่: {item['loc']} <br>
                    📅 วันที่: {item['date']}
                </p>
            </div>
        """, unsafe_allow_html=True)

# --- Tab 2: แจ้งเรื่องใหม่ ---
with tab2:
    st.markdown("### กรอกรายละเอียด")
    with st.form("report_form", clear_on_submit=True):
        new_type = st.radio("ประเภทการแจ้ง", ["ของหาย", "พบของ"], horizontal=True)
        new_name = st.text_input("ชื่อสิ่งของ")
        new_loc = st.text_input("สถานที่")
        new_date = st.date_input("วันที่เกิดเหตุ")
        new_img = st.file_uploader("แนบรูปภาพ (ถ้ามี)", type=['jpg', 'png'])
        
        submitted = st.form_submit_button("บันทึกข้อมูล")
        if submitted:
            if new_name and new_loc:
                new_entry = {
                    "type": new_type,
                    "name": new_name,
                    "loc": new_loc,
                    "date": str(new_date)
                }
                st.session_state.items.insert(0, new_entry)
                st.success("บันทึกข้อมูลสำเร็จแล้ว!")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

# --- Tab 3: สถิติ (Dashboard เล็กๆ) ---
with tab3:
    st.write("ภาพรวมระบบ")
    df = pd.DataFrame(st.session_state.items)
    if not df.empty:
        st.bar_chart(df['type'].value_counts())
