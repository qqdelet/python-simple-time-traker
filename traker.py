import psutil, os, time, json, csv
from datetime import datetime, timedelta
from tkinter import filedialog, Tk
import threading
from pystray import Icon, MenuItem as item, Menu
from PIL import Image, ImageDraw
import shutil
from plyer import notification
import pandas as pd

CONFIG_FILE = "config.json"
LOG_FILE = "usage_log.csv"
BACKUP_FOLDER = "backups"

last_report_date = None  # Для предотвращения многократной генерации отчета

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"apps": [], "auto_back_up": False}, f)
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
            notification.notify(title="Добавлено", message=f"{exe_name} добавлен.", timeout=3)
        else:
            notification.notify(title="Уже есть", message=f"{exe_name} уже есть.", timeout=3)

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

def calculate_time_report(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = ['timestamp', 'application', 'status']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp')
    df = df[df['status'] == 'Running']
    df['time_diff'] = df['timestamp'].diff()
    df['app_shift'] = df['application'].shift()
    df.loc[df['application'] != df['app_shift'], 'time_diff'] = pd.Timedelta(0)
    summary = df.groupby('application')['time_diff'].sum()
    summary_hours = summary.apply(lambda x: round(x.total_seconds() / 3600, 2))
    return summary_hours

def generate_monthly_report():
    global last_report_date
    now = datetime.now()
    if now.day == 1 and now.hour == 0 and (last_report_date is None or last_report_date.date() != now.date()):
        generate_report(now)
        last_report_date = now

def generate_report(date=None):
    if date is None:
        date = datetime.now()
    if os.path.exists(LOG_FILE):
        config = load_config()
        month_name = date.strftime("%B")
        backup_dir = os.path.join(BACKUP_FOLDER, month_name)
        os.makedirs(backup_dir, exist_ok=True)

        if config.get("auto_back_up", False):
            backup_path = os.path.join(backup_dir, f"log_backup_{date.strftime('%Y-%m-%d')}.csv")
            shutil.copy(LOG_FILE, backup_path)

        report = calculate_time_report(LOG_FILE)
        report_path = os.path.join(backup_dir, f"report_{date.strftime('%Y-%m')}.csv")
        report.to_csv(report_path, header=['Hours'], index_label='Application')

        notification.notify(
            title="Отчёт собран",
            message=f"Отчёт за {month_name} сохранён.",
            timeout=5
        )

def monitor_loop():
    while True:
        config = load_config()
        running = is_process_running(config["apps"])
        for app in running:
            log_usage(app)

        generate_monthly_report()
        time.sleep(10)

def create_image():
    img = Image.new("RGB", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill="black")
    d.ellipse((28, 28, 36, 36), fill="white")
    return img

def open_log():
    os.startfile(LOG_FILE)

def test_notification():
    notification.notify(
        title="Тестовое уведомление",
        message="Это пример системного уведомления от трекера.",
        timeout=5
    )

def manual_report():
    generate_report()

def quit_app(icon):
    icon.stop()

def setup_tray():
    icon = Icon("AppTracker", create_image(), menu=Menu(
        item('Открыть лог', lambda: open_log()),
        item('Добавить приложение', lambda: add_app()),
        item('Тестовое уведомление', lambda: test_notification()),
        item('Создать отчёт вручную', lambda: manual_report()),
        item('Выход', quit_app)
    ))
    threading.Thread(target=monitor_loop, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_tray()
