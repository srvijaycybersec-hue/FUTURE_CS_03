# app.py
import os
import pathlib
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from io import BytesIO
from encryption_utils import load_key_from_env, encrypt_file, decrypt_file_to_bytes

UPLOAD_FOLDER = "encrypted_store"
TEMP_FOLDER = "tmp_uploads"
ALLOWED_EXTENSIONS = None  # allow all by default, can restrict

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB limit - adjust if needed
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(16))

def allowed_file(filename):
    if ALLOWED_EXTENSIONS is None:
        return True
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

try:
    KEY = load_key_from_env("FILE_ENCRYPTION_KEY")
except Exception as e:
    KEY = None
    print("Warning: encryption key not loaded:", e)

@app.route("/")
def index():
    files = []
    for p in sorted(pathlib.Path(UPLOAD_FOLDER).iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if p.is_file():
            files.append(p.name)
    return render_template("files.html", files=files)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    # POST
    if KEY is None:
        flash("Server encryption key not configured. Set FILE_ENCRYPTION_KEY environment variable.", "danger")
        return redirect(url_for("index"))

    if "file" not in request.files:
        flash("No file part", "warning")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "warning")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("File type not allowed", "warning")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    tmp_path = os.path.join(TEMP_FOLDER, filename)
    file.save(tmp_path)

    # encrypted filename: use random hex to avoid leaking original filename
    enc_name = f"{os.urandom(8).hex()}.enc"
    enc_path = os.path.join(UPLOAD_FOLDER, enc_name)
    try:
        encrypt_file(tmp_path, enc_path, KEY, original_filename=filename)
    finally:
        # remove plaintext temp
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    flash(f"Uploaded and encrypted as {enc_name}", "success")
    return redirect(url_for("index"))

@app.route("/download/<enc_filename>", methods=["GET"])
def download(enc_filename):
    enc_path = os.path.join(UPLOAD_FOLDER, secure_filename(enc_filename))
    if not os.path.isfile(enc_path):
        flash("File not found", "danger")
        return redirect(url_for("index"))

    if KEY is None:
        flash("Server encryption key not configured.", "danger")
        return redirect(url_for("index"))

    # decrypt to memory and send as attachment with original filename
    try:
        plaintext, orig_name = decrypt_file_to_bytes(enc_path, KEY)
    except Exception as e:
        flash(f"Decrypt failed: {e}", "danger")
        return redirect(url_for("index"))

    bio = BytesIO()
    bio.write(plaintext)
    bio.seek(0)
    return send_file(
        bio,
        as_attachment=True,
        download_name=orig_name
    )

@app.route("/delete/<enc_filename>", methods=["POST"])
def delete(enc_filename):
    enc_path = os.path.join(UPLOAD_FOLDER, secure_filename(enc_filename))
    if os.path.isfile(enc_path):
        os.remove(enc_path)
        flash("Deleted.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    if KEY is None:
        print("ERROR: FILE_ENCRYPTION_KEY not set. Generate a 32-byte key (hex) and set environment variable FILE_ENCRYPTION_KEY.")
        print("Quick generate (PowerShell): [System.BitConverter]::ToString((New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes(32)).Replace('-', '')")
    app.run(host="0.0.0.0", port=5000, debug=True)