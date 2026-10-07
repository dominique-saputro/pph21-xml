import streamlit as st
from pathlib import Path

pages = st.navigation([
    st.Page("xml_pph21.py", title="Converter PPh21 Coretax"),
    st.Page("calculator.py", title="Kalkulator TER PPh21"),
    ])

BASE_DIR = Path(__file__).parent
FORMAT_DIR = BASE_DIR / "format"

format_bulanan = (FORMAT_DIR / "Format Bulanan Tetap & Tidak Tetap.xlsx").read_bytes()
format_tahunan = (FORMAT_DIR / "Format Tahunan A1.xlsx").read_bytes()

st.sidebar.write("Download Format Upload")
st.sidebar.download_button(
    label="Bulanan",
    data=format_bulanan,
    file_name="Format Bulanan Tetap & Tidak Tetap.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    icon=":material/download:",
)

st.sidebar.download_button(
    label="Tahunan A1",
    data=format_tahunan,
    file_name="Format Tahunan A1.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    icon=":material/download:",
)

pages.run()

