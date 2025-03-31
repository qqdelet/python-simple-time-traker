README on Eng and Rus lenguages, first English

## 🇬🇧 English Version

---

# Python Simple Time Tracker

A lightweight background time tracker for Windows that monitors selected applications and logs usage time to a CSV file. The app runs silently, shows a tray icon, and supports automatic startup with Windows.

---

### 🛠 How It Works

- Runs in the background with a tray icon
- Monitors selected apps (like `Code.exe`, `devenv.exe`) using process detection
- Logs when apps are running (even if minimized or not focused)
- Allows you to add apps to watch via a simple file dialog
- Stores usage logs in `usage_log.csv`
- Automatically starts with Windows using a VBS launcher (no console window)

---

### 📁 Project Structure

```
📁 tracker/
├── traker.py            # Main Python script with tray icon and process monitor
├── run_tracker.vbs      # Script to launch Python silently without console
├── config.json          # List of apps to watch
├── usage_log.csv        # Log of usage timestamps
├── README.md            # Project description
├── LICENSE              # MIT License
```

---

### 🚀 How to Add to Windows Startup

1. Press `Win + R`, enter:
   ```
   shell:startup
   ```
2. Copy a shortcut to `run_tracker.vbs` into that folder.
3. Done! The tracker will now launch silently at system startup.

---

### 📌 TODO / Roadmap

- [ ] Add GUI (graphical interface)  
- [ ] Support logging to SQLite database  
- [ ] Add config import/export  
- [ ] Add stats summaries (24h / 3 days / week)

---

## 🇷🇺 Русская версия

---

# Простой трекер времени на Python

Лёгкий фоновый трекер времени для Windows, который отслеживает работу выбранных приложений и сохраняет данные в CSV. Работает тихо, показывает значок в трее и может запускаться вместе с системой.

---

### 🛠 Как работает

- Работает в фоне и показывает значок в трее
- Следит за запуском выбранных приложений (например, `Code.exe`, `devenv.exe`)
- Фиксирует время, пока приложение работает (даже если оно не активно)
- Позволяет добавлять приложения через стандартное окно выбора файла
- Лог сохраняется в `usage_log.csv`
- Поддерживает автозапуск через VBS без появления консоли

---

### 📁 Структура проекта

```
📁 tracker/
├── traker.py            # Основной Python-скрипт с иконкой в трее и мониторингом
├── run_tracker.vbs      # Запуск без консоли
├── config.json          # Список отслеживаемых приложений
├── usage_log.csv        # CSV лог с временными метками
├── README.md            # Описание проекта
├── LICENSE              # Лицензия MIT
```

---

### 🚀 Как добавить в автозагрузку

1. Нажми `Win + R`, введи:
   ```
   shell:startup
   ```
2. Скопируй ярлык на `run_tracker.vbs` в открытую папку.
3. Готово! Трекер будет запускаться в фоне при старте Windows.

---

### 📌 TODO / Планы на развитие

- [ ] Добавить графический интерфейс  
- [ ] Поддержка логирования в SQLite  
- [ ] Импорт/экспорт конфигураций  
- [ ] Сводка статистики (за 24 часа, 3 дня, неделю)

---
