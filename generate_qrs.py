import os
import qrcode

BASE_URL = "http://127.0.0.1:5000/menu"

# Dynamically find the path of this script's directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "app", "static", "qrcodes")

os.makedirs(OUTPUT_DIR, exist_ok=True)

tables = [f"A{i}" for i in range(1, 11)]

for table in tables:
    target_url = f"{BASE_URL}?table={table}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_path = os.path.join(OUTPUT_DIR, f"table_{table}.png")
    img.save(file_path)
    print(f"Generated QR Code for Table {table} -> {file_path}")

print(f"\nAll table QR codes successfully generated in {OUTPUT_DIR}")
