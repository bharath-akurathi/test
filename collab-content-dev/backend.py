from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import fitz  # PyMuPDF for PDFs
import docx
import subprocess
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

GIT_REPO_PATH = "/Users/akurathi/Documents/GitHub/test"  # Local GitHub repo directory
UPLOAD_FOLDER = os.path.join(GIT_REPO_PATH, "uploads")
TEXT_FOLDER = os.path.join(GIT_REPO_PATH, "texts")
IMAGE_FOLDER = os.path.join(GIT_REPO_PATH, "images")

ALLOWED_EXTENSIONS = {"txt", "docx", "pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_and_images_from_pdf(pdf_path, doc_id):
    doc = fitz.open(pdf_path)
    text = ""
    image_paths = []

    for page_num in range(len(doc)):
        text += doc[page_num].get_text("text") + "\n"

        for img_index, img in enumerate(doc[page_num].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            img_filename = f"{doc_id}_page{page_num + 1}_img{img_index + 1}.{image_ext}"
            img_path = os.path.join(IMAGE_FOLDER, img_filename)

            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_paths.append(f"images/{img_filename}")

    return text, image_paths

def push_to_github(commit_message):
    """Push new content to the GitHub repository."""
    try:
        subprocess.run(["git", "-C", GIT_REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "push"], check=True)
        print("✅ Changes pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        doc_id = filename.rsplit(".", 1)[0]
        extracted_text = ""
        image_paths = []

        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                extracted_text = file.read()

        elif filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(file_path)

        elif filename.endswith(".pdf"):
            extracted_text, image_paths = extract_text_and_images_from_pdf(file_path, doc_id)

        # Save extracted text in the Git repo
        text_filename = f"{doc_id}.txt"
        text_path = os.path.join(TEXT_FOLDER, text_filename)
        with open(text_path, "w", encoding="utf-8") as file:
            file.write(extracted_text)

        # Push changes to GitHub
        push_to_github(f"📄 Added {filename}")

        return jsonify({
            "message": "File uploaded successfully!",
            "filename": filename,
            "text": extracted_text,
            "images": image_paths
        })

    return jsonify({"error": "Invalid file type. Allowed: txt, docx, pdf."}), 400

if __name__ == "__main__":
    app.run(debug=True)
