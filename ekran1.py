import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def write_to_json(event_type, file_path):
    event = {
        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Olay": event_type,
        "Dosya": file_path
    }
    json_file = "/home/ubuntu/bsm/logs/changes.json"
    try:
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        existing_data.append(event)

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    except json.JSONDecodeError:
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump([event], file, ensure_ascii=False, indent=4)

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        write_to_json("Dosya oluşturuldu.", event.src_path)

    def on_modified(self, event):
        write_to_json("Dosya değiştirildi.", event.src_path)

    def on_deleted(self, event):
        write_to_json("Dosya silindi.", event.src_path)

    def on_moved(self, event):
        write_to_json("Dosya taşındı veya adı değiştirildi.", event.src_path)

if __name__ == "__main__":
    watch_dir = "/home/ubuntu/bsm/test1"
    if not os.path.exists(watch_dir):
        print(f"Hata: {watch_dir} dizini bulunamadı.")
        exit(1)

    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()

    try:
        print(f"{watch_dir} izleniyor...")
        observer.join()
    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")
    finally:
        observer.stop()
        observer.join()
