import os
from pathlib import Path
import requests
import base64
import streamlit as st

st.set_page_config(page_title="Financial Assistant", page_icon="💰")
st.title("Multimodal Financial Assistant")
st.caption("Answers are grounded in indexed policy evidence; unsupported questions should be refused.")

api_url = os.getenv("ASSISTANT_API_URL", "http://localhost:8000")
question = st.text_input("Ask about a financial policy")
if st.button("Ask") and question:
    response = requests.post(f"{api_url}/ask", json={"question": question}, timeout=30)
    response.raise_for_status()
    data = response.json()
    st.write(data["answer"])
    if data["sources"]:
        st.subheader("Sources")
        for source in data["sources"]:
            label = f"{Path(source['source']).name}" + (f" — page {source['page']}" if source.get("page") else "")
            st.caption(label)
            st.write(source["text"])

st.divider()
st.subheader("Image inspection")
image = st.file_uploader("Upload a financial statement or chart", type=["png", "jpg", "jpeg"])
if image:
    st.image(image)
    if st.button("Inspect image"):
        raw = image.getvalue()
        encoded = base64.b64encode(raw).decode("ascii")
        mime = image.type or "image/jpeg"
        response = requests.post(f"{api_url}/describe-image", json={"question": "Read the financial information in this image and summarize the relevant figures.", "image_data_url": f"data:{mime};base64,{encoded}"}, timeout=45)
        response.raise_for_status()
        st.write(response.json()["answer"])
