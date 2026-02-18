import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ป้องกัน Error ตั้งแต่บรรทัดแรก ---
st.set_page_config(page_title="Lost & Found", page_icon="🌸")

# ใช้ฟังก์ชันเพื่อการันตีว่าข้อมูลต้องมีอยู่จริง
def get_items():
    if "items" not in st.session_state:
        st.session_state["items"] = [
            {"type": "ของหาย", "name": "กระเป๋าสตางค์", "loc": "ตึก A", "date": "2026-02-18", "contact": "081-xxx"},
            {"type": "พบของ", "name": "กุญแจรถ", "loc": "โรงอาหาร", "date": "2026-02-17", "contact": "ประชาสัมพันธ์"}
        ]
    return st.session_state["items"]

# เรียกใช้ฟังก์ชันทันที
items_list = get_items()

# --- 2. สไตล์มินิมอลชมพูขาว ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    * { font-family: 'Kanit', sans-serif; }
    .stApp { background-color: #FFFFFF; }
    .card {
        padding: 1.5rem; border-radius: 15px; background-color: #FFF9FA;
        border: 1px solid #FFE4E8; margin-bottom: 1rem;
    }
    .badge { padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; }
    .lost { background-color: #FFE4E4; color: #FF6B6B; }
    .found { background-color: #E4FFE4; color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF8DA1;'>🌸 Lost & Found</h1>", unsafe_allow_html=True)

# --- 3. ส่วนการทำงาน ---
tab1, tab2 = st.tabs(["🔍 รายการสิ่งของ", "➕ แจ้งเรื่องใหม่"])

with tab1:
    c1, c2 = st.columns([2, 1])
    search = c1.text_input("ค้นหา", placeholder="ชื่อของ...", label_visibility="collapsed")
    cat = c2.selectbox("ประเภท", ["ทั้งหมด", "ของหาย", "พบของ"], label_visibility="collapsed")
    
    st.write("---")

    # วนลูปจากตัวแปร items_list ที่เราการันตีไว้แล้วข้างบน
    for item in items_list:
        if cat != "ทั้งหมด" and item['type'] != cat: continue
        if search.lower() not in item['name'].lower(): continue

        type_class = "lost" if item['type'] == "ของหาย" else "found"
        st.markdown(f"""
            <div class="card">
                <span class="badge {type_class}">{item['type']}</span>
                <h3 style="margin: 10px 0;">{item['name']}</h3>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">📍 {item['loc']} | 📅 {item['date']}</p>
                <p style="color: #FF8DA1; font-size: 0.85rem; margin-top: 5px;">📞 {item['contact']}</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    with st.form("add_form", clear_on_submit=True):
        f_type = st.radio("ประเภท", ["ของหาย", "พบของ"], horizontal=True)
        f_name = st.text_input("ชื่อสิ่งของ*")
        f_loc = st.text_input("สถานที่*")
        f_contact = st.text_input("ช่องทางติดต่อ")
        if st.form_submit_button("บันทึกประกาศ"):
            if f_name and f_loc:
                new_item = {"type": f_type, "name": f_name, "loc": f_loc, "date": str(datetime.now().date()), "contact": f_contact}
                st.session_state["items"].insert(0, new_item)
                st.success("สำเร็จ!")
                st.rerun()
