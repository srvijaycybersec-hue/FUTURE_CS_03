# 🔐  FUTURE_CS_03---Secure File Sharing System (Flask + AES Encryption + HTML)

Intern Details

| Field   | Details                                |
|---------|----------------------------------------|
| Name    | Vijay S R                              |
| Role    | Cybersecurity Intern                   |
| Program | Future Interns — Cybersecurity Program |
| Task    | Secure File Sharing System |

A secure file sharing web application built using Flask and AES-GCM encryption, allowing users to upload, encrypt, download (decrypt), and delete files safely through a simple HTML interface.

This project demonstrates end-to-end encryption handling for uploaded files — protecting data both at rest (on disk) and in transit (when combined with HTTPS).



---

🧠 Features

AES-256-GCM encryption (authenticated encryption for confidentiality + integrity)

Secure file upload and encrypted storage

File download with automatic decryption

Encrypted filename masking (server never exposes real file names)

Flash message UI feedback (upload, delete, errors)

Secure environment-based key management

Simple HTML templates for upload & list view

Designed for local or enterprise security demonstrations



---

🧩 Project Structure

secure-file-sharing/
│
├── app.py                    # Main Flask app
├── encryption_utils.py       # AES-GCM encryption/decryption utilities
├── requirements.txt          # Required Python libraries
├── templates/
│   ├── upload.html           # File upload page
│   └── files.html            # File listing & download page
├── encrypted_store/          # Encrypted files stored here
├── tmp_uploads/              # Temporary plaintext uploads (auto-deleted)
└── README.md                 # Project documentation


---

⚙️ Setup Instructions (Windows 10 / Linux)

# 1️⃣  Clone or Download the Project
# git clone https://github.com/srvijaycybersec-hue/FUTURE_CS_03/secure-file-sharing.git
# cd secure-file-sharing

# 2️⃣ Create and Activate Virtual Environment
# Windows (PowerShell):
`python -m venv venv`
`.\venv\Scripts\activate`

# Linux/Mac:
`python3 -m venv venv`
`source venv/bin/activate`

# 3️⃣  Install Dependencies
`pip install -r requirements.txt`


---

🔑 Generate and Set Encryption Key

This app requires a 32-byte AES key stored in an environment variable named FILE_ENCRYPTION_KEY.

# Option 1 — Generate with Python

`python - <<'PY'`
`import os; print(os.urandom(32).hex())`
`PY`

Copy the 64-character hex output.

# Option 2 — Generate with PowerShell

`$key = -join ((1..32) | ForEach-Object { "{0:X2}" -f (Get-Random -Maximum 256) })
$key`

Set Environment Variables

# Windows (temporary):

`$env:FILE_ENCRYPTION_KEY = "paste_your_64_hex_key_here"`
`$env:FLASK_SECRET = "random_flask_secret_here"`

# Linux/Mac (temporary):

`export FILE_ENCRYPTION_KEY="paste_your_64_hex_key_here"`
`export FLASK_SECRET="random_flask_secret_here"`

> ⚠️ Never hardcode your key inside the code or commit it to GitHub.




---

▶️ Run the Application

`python app.py`

Open your browser and visit:

👉 http://127.0.0.1:5000/


---

🌐 Web Interface

Page URL Description

Home / Files / List all encrypted files, with download & delete options
Upload /upload Upload and encrypt a new file



---

🔒 Security Design

Security Aspect Implementation

Encryption Algorithm AES-256-GCM (authenticated encryption)
Key Storage Environment variable (FILE_ENCRYPTION_KEY)
Filename Protection Stored filename is random (xxxx.enc) — real name encrypted inside
Integrity GCM mode provides built-in integrity check
Transport Security Use HTTPS or a reverse proxy (e.g., Nginx + TLS)
Temporary Files Removed immediately after encryption
CSRF Protection Basic Flask form handling (add CSRF token if multi-user)
Auth Support Not included — add login & user roles for real-world use



---

📁 Example Encrypted File Structure

Each encrypted file stored in encrypted_store/ has this binary format:

nonce (12 bytes)
+ filename_length (2 bytes)
+ filename (UTF-8)
+ ciphertext (AES-GCM)

When decrypted, the original filename and content are restored.


---

🧰 Troubleshooting

Issue Cause Solution

cannot import name 'encrypt_file' Wrong filename (e.g., encryption _utils.py with a space) Rename to encryption_utils.py
RuntimeError: FILE_ENCRYPTION_KEY not set Environment variable missing Set key using PowerShell or export
File not downloading HTML missing download link Ensure download_name is used in send_file()
Memory issues Large files encrypted fully in RAM Use chunked streaming encryption (optional)



---

🚀 Future Enhancements

[ ] User authentication (login/register)

[ ] Role-based access control (admin/user)

[ ] Database integration for file metadata

[ ] Expiring or one-time download links

[ ] Streaming encryption for very large files

[ ] Frontend redesign (Bootstrap or Tailwind)



---

🧾 License

This project is released under the MIT License.
You are free to use, modify, and distribute it with attribution.


---

🧠 Author

Developed by: Vijay S R
Tech Stack: Python Flask · AES-GCM · Cryptography Library · HTML
