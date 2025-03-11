import streamlit as st
import subprocess
import os
import time
import requests
from streamlit_quill import st_quill
import psutil
import atexit

st.set_page_config(page_title="📄 GitHub Content Editor", layout="wide")

API_URL = "http://127.0.0.1:5000"
GITHUB_REPO = "https://github.com/bharath-akurathi/test"
RAW_GITHUB = "https://raw.githubusercontent.com/bharath-akurathi/test/main"

# Function to check if backend.py is running
def is_backend_running():
    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = process.info.get("cmdline", [])
        if cmdline and "python3" in cmdline[0] and "backend.py" in cmdline:
            return True
    return False

# Function to start backend.py
def start_backend():
    if not is_backend_running():
        subprocess.Popen(["python3", "backend.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)

start_backend()

st.title("📄 GitHub-Based Content Editor")
st.write("Upload a **TXT, DOCX, or PDF** file, or type directly into the editor.")

uploaded_file = st.file_uploader("Upload Document", type=["txt", "docx", "pdf"])
extracted_text = ""
extracted_images = []

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post(f"{API_URL}/api/upload", files=files)

    if response.status_code == 200:
        data = response.json()
        extracted_text = data.get("text", "")
        extracted_images = data.get("images", [])
        st.success(f"✅ **{uploaded_file.name}** uploaded and saved to GitHub!")

# Text Editor
st.subheader("📜 Edit or Write Text")
quill_content = st_quill(value=extracted_text, placeholder="Edit here...")

if st.button("💾 Save to GitHub"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"uploads/saved_content_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(quill_content)
    
    subprocess.run(["git", "-C", "test", "add", filename])
    subprocess.run(["git", "-C", "test", "commit", "-m", f"📜 Saved content {filename}"])
    subprocess.run(["git", "-C", "test", "push"])
    
    st.success(f"✅ Content saved as `{filename}` and pushed to GitHub!")

# Display Images from GitHub
if extracted_images:
    st.subheader("🖼️ Extracted Images")
    for img_url in extracted_images:
        github_img_url = f"{RAW_GITHUB}/{img_url}"
        st.image(github_img_url, caption="Extracted Image", use_container_width=True)

def stop_backend():
    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = process.info.get("cmdline", [])
        if cmdline and "python3" in cmdline[0] and "backend.py" in cmdline:
            os.kill(process.info["pid"], 9)

atexit.register(stop_backend)
