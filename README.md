🔐 Secure File Sharing System (Flask + AES Encryption)

A secure file sharing web application built using Flask and AES-GCM encryption, allowing users to upload, encrypt, download (decrypt), and delete files safely through a simple HTML interface.

This project demonstrates end-to-end encryption handling for uploaded files — protecting data both at rest and in transit.


---

🧠 Features

AES-256-GCM encryption (confidentiality + integrity)

Secure upload and encrypted storage

Decrypt-on-download

Hidden real filenames (randomized storage names)

Flash message feedback for all actions

Environment-based key management

Simple HTML templates

Works on Windows and Linux



---

🧩 Project Structure

secure-file-sharing/
│
├── app.py
├── encryption_utils.py
├── requirements.txt
├── templates/
│   ├── upload.html
│   └── files.html
├── encrypted_store/
├── tmp_uploads/
└── README.md


---

⚙️ Setup Instructions

1. Clone or Download the Project

git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing

2. Create and Activate Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux / macOS:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt


---

🔑 Generate and Set Encryption Key

This app needs a 32-byte AES key stored in an environment variable named FILE_ENCRYPTION_KEY.

Option 1 — Generate with Python

python - <<'PY'
import os
print(os.urandom(32).hex())
PY

Copy the 64-character hex output.

Option 2 — Generate with PowerShell

$key = -join ((1..32) | ForEach-Object { "{0:X2}" -f (Get-Random -Maximum 256) })
$key

Set Environment Variables

Windows (PowerShell):

setx FILE_ENCRYPTION_KEY "paste_your_64_hex_key_here"
setx FLASK_SECRET "random_flask_secret_here"

Linux / macOS (temporary):

export FILE_ENCRYPTION_KEY="paste_your_64_hex_key_here"
export FLASK_SECRET="random_flask_secret_here"

> ⚠️ Never hard-code your key inside the code or commit it to GitHub.




---

▶️ Run the Application

python app.py

Then open your browser at:

http://127.0.0.1:5000/


---

🌐 Web Interface

Page URL Description

Home / Files / List all encrypted files
Upload /upload Upload and encrypt new file



---

🔒 Security Design

Security Aspect Implementation

Algorithm AES-256-GCM
Key Storage Environment variable
Filename Protection Random encrypted names
Integrity AES-GCM authentication tag
Transport Security Use HTTPS / reverse proxy
Temporary Files Auto-deleted after use
Authentication Not included (add if multi-user)



---

📁 Encrypted File Format

Each file in encrypted_store/ uses this structure:

nonce (12 bytes)
+ filename_length (2 bytes)
+ filename (UTF-8)
+ ciphertext (AES-GCM)

Decryption restores the original filename and content.


---

🧰 Troubleshooting

Issue Cause Solution

cannot import name 'encrypt_file' Wrong file name (encryption _utils.py) Rename to encryption_utils.py
FILE_ENCRYPTION_KEY not set Missing environment variable Set the key using commands above
File doesn’t download Missing download_name Check send_file() line
Memory errors Very large files Use chunked encryption (optional)



---

🚀 Future Enhancements

[ ] Add login & authentication

[ ] Role-based access (admin/user)

[ ] Database for file metadata

[ ] Expiring download links

[ ] Streaming encryption for large files

[ ] UI with Bootstrap or Tailwind



---

🧾 License

Released under the MIT License.
You are free to use, modify, and distribute this project with attribution.


---

👨‍💻 Author

Developed by: Vijay S R
Stack: Flask · AES-GCM · Python · HTML · Cryptography
