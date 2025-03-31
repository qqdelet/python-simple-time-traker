import psutil, os, time, json, csv
from datetime import datetime
from tkinter import filedialog, Tk, messagebox
import threading
from pystray import Icon, MenuItem as item, Menu
from PIL import Image, ImageDraw

CONFIG_FILE = "config.json"
LOG_FILE = "usage_log.csv"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"apps": []}, f)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def add_app():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="Выбери .exe файл приложения")
    if file_path:
        exe_name = os.path.basename(file_path)
        config = load_config()
        if exe_name not in config["apps"]:
            config["apps"].append(exe_name)
            save_config(config)
            messagebox.showinfo("Добавлено", f"{exe_name} добавлен.")
        else:
            messagebox.showinfo("Уже есть", f"{exe_name} уже есть.")

def is_process_running(target_names):
    running = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in target_names:
                running.append(proc.info['name'])
        except:
            continue
    return running

def log_usage(app_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([now, app_name, "Running"])

def monitor_loop():
    while True:
        config = load_config()
        running = is_process_running(config["apps"])
        for app in running:
            log_usage(app)
        time.sleep(10)

def create_image():
    # Рисуем простую иконку (глаз)
    img = Image.new("RGB", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill="black")
    d.ellipse((28, 28, 36, 36), fill="white")
    return img

def open_log():
    os.startfile(LOG_FILE)

def quit_app(icon):
    icon.stop()

def setup_tray():
    icon = Icon("AppTracker", create_image(), menu=Menu(
        item('Открыть лог', lambda: open_log()),
        item('Добавить приложение', lambda: add_app()),
        item('Выход', quit_app)
    ))
    threading.Thread(target=monitor_loop, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_tray()
