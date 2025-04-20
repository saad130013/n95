
# 🏥 RCRN/N95 Course Tracker

نظام بسيط وذكي لمتابعة حضور الموظفين لدورات **COVID-19 Vaccine & RCRN/N95** في المنشآت الصحية.

## ✅ الميزات:
- 🔍 البحث بالاسم أو رقم MRN
- 📋 عرض حالة كل موظف (هل حضر الدورة أم لا)
- 🗓️ تحديث تاريخ حضور الدورة لكل موظف
- 💾 حفظ التعديلات تلقائيًا في ملف Excel
- 🚫 عرض قائمة الموظفين الذين لم يحضروا الدورة بعد

## 📂 الملفات:
- `rcrn_n95_tracker_app.py` : كود تطبيق Streamlit
- `rcrn_course_data.xlsx` : قاعدة بيانات الموظفين

## 🚀 طريقة التشغيل:
```bash
pip install streamlit pandas openpyxl
streamlit run rcrn_n95_tracker_app.py
```

## 📦 تم تطويره باستخدام:
- Python 3
- Streamlit
- Pandas
