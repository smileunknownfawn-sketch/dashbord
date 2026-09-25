"""Безпечна точка запуску фінальної версії."""

import traceback
from pathlib import Path

import streamlit as st

from app_v3 import main


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log_dir = Path(__file__).resolve().parent / "data"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "last_error.log"
        log_file.write_text(traceback.format_exc(), encoding="utf-8")
        st.error("Виникла внутрішня помилка програми.")
        st.info("Дані не видалено. Технічний журнал збережено у папці data/last_error.log.")
        with st.expander("Технічна інформація для обслуговування"):
            st.code(traceback.format_exc(), language="text")
