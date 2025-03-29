import subprocess
import sys
import importlib

# Required libraries
required_libraries = [
    "asyncio", "websockets", "pyautogui", "json", "qrcode", "io",
    "flask", "threading", "ip_lib", "PIL", "base64", "tkinter"
]

# Auto-install missing libraries
for lib in required_libraries:
    try:
        if lib == "PIL":
            importlib.import_module("PIL.Image")
        elif lib == "tkinter":
            import tkinter  # some Python installations already include it
        else:
            importlib.import_module(lib)
    except ImportError:
        package = "pillow" if lib == "PIL" else lib
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Actual imports
import asyncio
import websockets
import pyautogui
import json
import qrcode
from io import BytesIO
from flask import Flask, send_from_directory
from threading import Thread
from ip_lib import get_local_ip as ip
from PIL import Image, ImageTk
import base64
import tkinter as tk

# Configuration
HOST = "0.0.0.0"
WS_PORT = 1626
HTTP_PORT = 1625
static_dir = "static"

# Colors
COLORS = {
    "primary": "#2196F3",
    "accent": "#FF4081",
    "background": "#FAFAFA",
    "text": "#212121"
}

# Flask app
flask_app = Flask(__name__, static_folder=static_dir)

@flask_app.route('/')
def serve_index():
    return send_from_directory(static_dir, "index.html")

@flask_app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(static_dir, path)

# WebSocket handler
async def handle_ws_client(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            if data[0] == "btn":
                pyautogui.press(data[1])
        except Exception as e:
            print(f"WS Error: {e}")

def run_websockets():
    async def server_main():
        async with websockets.serve(handle_ws_client, HOST, WS_PORT):
            await asyncio.Future()
    asyncio.run(server_main())

def run_flask():
    flask_app.run(host=HOST, port=HTTP_PORT, debug=False, use_reloader=False)

# QR Code generator
def generate_qr_image(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=COLORS["primary"], back_color="white")
    return img

# Start servers
Thread(target=run_websockets, daemon=True).start()
Thread(target=run_flask, daemon=True).start()

# --- TKINTER GUI ---
server_url = f"http://{ip()}:{HTTP_PORT}"
qr_img = generate_qr_image(server_url)

# GUI
root = tk.Tk()
root.title("Remote Server Control")
root.geometry("320x420")
root.configure(bg=COLORS["background"])

# URL Label
url_label = tk.Label(root, text="Remote Server Running", font=("Helvetica", 16), bg=COLORS["background"], fg=COLORS["text"])
url_label.pack(pady=10)

url_display = tk.Label(root, text=server_url, font=("Helvetica", 12), bg=COLORS["background"], fg=COLORS["text"])
url_display.pack()

# Convert PIL to ImageTk
qr_tk = ImageTk.PhotoImage(qr_img)
qr_label = tk.Label(root, image=qr_tk, bg=COLORS["background"])
qr_label.pack(pady=20)

# Exit button
def stop_server():
    root.destroy()

exit_btn = tk.Button(root, text="Stop Server", command=stop_server, bg=COLORS["primary"], fg="white", padx=10, pady=5)
exit_btn.pack(pady=10)

# Start the GUI
root.mainloop()
