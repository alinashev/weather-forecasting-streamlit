import base64

import streamlit as st

def set_background_color(color: str):
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {color};
            }}
        </style>
    """, unsafe_allow_html=True)

def show_gif(path: str, width: int = None, height: int = None):
    with open(path, "rb") as f:
        gif_bytes = f.read()
        encoded = base64.b64encode(gif_bytes).decode()

    size_attr = ""
    if width:
        size_attr += f'width="{width}" '
    if height:
        size_attr += f'height="{height}" '

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/gif;base64,{encoded}" {size_attr}/>
        </div>
        """,
        unsafe_allow_html=True
    )
