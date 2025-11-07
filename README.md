🔐 Secure File Sharing System

A Secure File Sharing Web Application built using Python Flask and Flask-WTF, designed to allow users to upload and download files securely.
It ensures data confidentiality using AES encryption and secure key management, providing a safe and simple interface for file sharing.


---

🚀 Features

🧩 User-Friendly Interface (HTML + Flask-WTF forms)

🔒 AES File Encryption & Decryption

📂 Secure Upload and Download System

🔑 Unique Encryption Key for Each File

🧠 Basic Key Management Logic

🧾 File Integrity Verification



---

🧰 Tech Stack

Component Technology Used

Backend Python Flask
Frontend HTML, CSS, Flask-WTF
Encryption AES (Advanced Encryption Standard)
Database (optional) SQLite / File-based storage
Environment VS Code / Kali Linux / Ubuntu



---

📁 Project Structure

SecureFileShare/
│
├── app.py                # Main Flask Application
├── templates/
│   ├── upload.html        # File upload page
│   ├── download.html      # File download page
│   └── index.html         # Home page
│
├── static/
│   ├── css/
│   └── js/
│
├── uploads/              # Encrypted uploaded files
├── decrypted/            # Temporary decrypted files
├── encryption.py          # AES encryption/decryption logic
├── forms.py               # Flask-WTF forms
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies


---

⚙️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/yourusername/SecureFileShare.git
cd SecureFileShare

2️⃣ Create a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the Application

python app.py

Then open your browser and go to:

http://127.0.0.1:5000


---

🔑 How It Works

1. Upload a file → User selects a file through the upload form.


2. Encryption process → The file is encrypted using AES before saving to the server.


3. Download request → When a user requests download, the file is decrypted and provided securely.


4. Temporary storage → Decrypted files are deleted after the session to ensure security.




---

🧩 Example Workflow

Step Action Description

1️⃣ Upload file Select a file from local system
2️⃣ Encryption File encrypted with AES algorithm
3️⃣ Download file System decrypts and allows secure download
4️⃣ Cleanup Decrypted copy auto-deleted after session



---

🧠 Security Highlights

AES 256-bit Encryption

No plaintext files stored on the server

Separate directories for encrypted and decrypted files

Flask-WTF used to prevent CSRF attacks

Temporary files cleaned automatically

---

💻 Future Enhancements

Add User Authentication (Login System)

Use Database for Key Storage

Enable File Sharing via Secure Link / Token

Add Email Notification for Shared Files



---

📜 License

This project is licensed under the MIT License — feel free to use, modify, and distribute.


---

👨‍💻 Author

Vijay S R
Internship Secure File Sharing Project
📧 [srvijay.cybersec@gmail.com]
🌐 GitHub: https://github.com/srvijaycybersec-hue
