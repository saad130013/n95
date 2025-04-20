
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="متابعة دورة RCRN/N95", layout="wide")
st.title("📋 نظام متابعة الموظفين لدورة COVID-19 Vaccine & RCRN/N95")

EXCEL_PATH = "rcrn_n95_attendance.xlsx"

# ✅ تحميل البيانات الحقيقية من الجدول في ملف Excel
@st.cache_data
def load_data():
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH, skiprows=6, usecols="A:D")
        df.columns = ["NO", "Name", "MRN", "Due Date"]
        return df
    else:
        return pd.DataFrame(columns=["NO", "Name", "MRN", "Due Date"])

df = load_data()

# 🔍 نموذج البحث
st.sidebar.header("🔎 البحث عن الموظف")
search_name = st.sidebar.text_input("👤 الاسم")
search_mrn = st.sidebar.text_input("🆔 رقم السجل الطبي MRN")

results = df
if search_name:
    results = results[results["Name"].astype(str).str.contains(search_name, case=False, na=False)]
if search_mrn:
    results = results[results["MRN"].astype(str).str.contains(search_mrn)]

# عرض نتائج البحث
st.subheader("🗂️ نتائج البحث")
try:
    st.dataframe(results.astype(str))
except Exception as e:
    st.error(f"حدث خطأ أثناء عرض النتائج: {e}")

# تحديث حالة الحضور
st.subheader("✅ تحديث حالة الدورة")
if not df.empty:
    selected_name = st.selectbox("اختر اسم الموظف", df["Name"].dropna().unique())
    col1, col2 = st.columns(2)
    with col1:
        attended = st.selectbox("هل حضر الدورة؟", ["نعم", "لا"])
    with col2:
        attendance_date = st.date_input("تاريخ الحضور", value=datetime.today())

    if st.button("💾 حفظ التحديث"):
        df.loc[df["Name"] == selected_name, "Attended?"] = attended
        df.loc[df["Name"] == selected_name, "Attendance Date"] = attendance_date
        df.to_excel(EXCEL_PATH, index=False)
        st.success("✅ تم حفظ التحديث بنجاح")

# عرض الموظفين الذين لم يحضروا
st.subheader("❗الموظفون الذين لم يحضروا الدورة بعد")
if "Attended?" in df.columns:
    missing = df[df["Attended?"] != "نعم"]
    st.dataframe(missing.astype(str))
