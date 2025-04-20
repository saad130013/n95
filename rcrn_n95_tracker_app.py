
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="متابعة دورات RCRN/N95", layout="wide")
st.title("📋 نظام متابعة الموظفين لدورة COVID-19 Vaccine & RCRN/N95")

EXCEL_PATH = "rcrn_course_data.xlsx"

# تحميل البيانات من Excel
@st.cache_data
def load_data():
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
        df.columns = df.columns.str.strip()
        return df
    else:
        return pd.DataFrame(columns=["NO", "Name", "MRN", "Department", "Course Notes", "Attended?", "Attendance Date"])

df = load_data()

# نموذج البحث
st.sidebar.header("🔍 البحث عن الموظف")
search_name = st.sidebar.text_input("🔠 الاسم")
search_mrn = st.sidebar.text_input("🔢 رقم السجل الطبي MRN")

results = df
if search_name:
    results = results[df["Name"].astype(str).str.contains(search_name, case=False, na=False)]
if search_mrn:
    results = results[df["MRN"].astype(str).str.contains(search_mrn)]

st.subheader("📄 نتائج البحث")
try:
    results_cleaned = results.astype(str)
    st.dataframe(results_cleaned)
except Exception as e:
    st.error(f"حدث خطأ أثناء عرض النتائج: {e}")

# تحديث حالة الحضور
st.subheader("✅ تحديث حالة الدورة")
if not df.empty and "Name" in df.columns:
    selected_name = st.selectbox("اختر اسم الموظف", df["Name"].dropna().unique())
    selected_row = df[df["Name"] == selected_name].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        attended = st.selectbox("هل حضر الدورة؟", ["نعم", "لا"], index=0 if selected_row.get("Attended?") == "نعم" else 1)
    with col2:
        attendance_date = st.date_input("تاريخ الحضور", value=datetime.today())

    if st.button("💾 حفظ التحديث"):
        df.loc[df["Name"] == selected_name, "Attended?"] = attended
        df.loc[df["Name"] == selected_name, "Attendance Date"] = attendance_date
        df.to_excel(EXCEL_PATH, index=False)
        st.success("✅ تم حفظ التحديث بنجاح")

# عرض الموظفين الذين لم يحضروا الدورة
st.subheader("❗الموظفون الذين لم يحضروا الدورة بعد")
if "Attended?" in df.columns:
    try:
        missing = df[df["Attended?"] != "نعم"]
        st.dataframe(missing.astype(str))
    except Exception as e:
        st.error(f"تعذر عرض العهد غير المكتملة: {e}")
