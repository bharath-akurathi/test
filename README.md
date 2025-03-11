### **📘 Collaborative Content Editor**  
A **Streamlit-based web app** for collaborative content editing, supporting **real-time text editing, file uploads (TXT, DOCX, PDF), image extraction, and GitHub integration** for version control. 🚀  

---

## **🛠 Features**  
✅ **Upload & Edit**: Upload TXT, DOCX, or PDF files and edit them in a live text editor.  
✅ **Extract Images**: Extract images from PDFs and display them in the frontend.  
✅ **Auto-Save to GitHub**: Saves files in a GitHub repository (`test`).  
✅ **Backend Auto-Start**: Automatically starts the Flask backend when launching the app.  

---

## **📌 Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/bharath-akurathi/test.git
cd test
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**  
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **🚀 Running the App**  

### **1️⃣ Start Streamlit Frontend**  
```bash
streamlit run app.py
```
> This will automatically start `backend.py`.  

### **2️⃣ Manually Start Backend (If Needed)**  
If the backend doesn’t start automatically, run:  
```bash
python3 backend.py
```

---

## **📂 File Structure**  
```
test/
│── app.py                  # Streamlit Frontend
│── backend.py               # Flask API Backend
│── requirements.txt         # Required Python Packages
│── saved/                   # Stores edited files
│── images/                  # Extracted images from PDFs
│── uploads/                 # Stores uploaded files
│── README.md                # Documentation
```

---

## **📤 Saving & Pushing to GitHub**  
Every time a file is saved, it is **automatically committed and pushed** to the repository.  
To manually push:  
```bash
git add .
git commit -m "Updated content"
git push origin main
```

---

## **🔧 Troubleshooting**  

❌ **Backend Not Starting?**  
Run:  
```bash
python3 backend.py
```

❌ **Git Not Pushing Files?**  
Make sure you have write access to the repository and try:  
```bash
cd /path/to/test
git status
git add .
git commit -m "Fixed file upload issue"
git push origin main
```

---

## **🎯 Contributing**  
Feel free to **fork** this repo, submit **pull requests**, and improve the app! 🚀  

---

### **📝 Author**  
📌 **Bharath Akurathi** | [GitHub](https://github.com/bharath-akurathi)  

---

This README provides everything needed to **install, run, and troubleshoot** the project. 🚀 Let me know if you need any modifications! 😊
