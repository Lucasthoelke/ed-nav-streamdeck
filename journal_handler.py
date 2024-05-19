import os.path
import glob

import main
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import json


class JournalFileHandler(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:
        main.logger.info("File modified")
        print("File modified")
        # print(main.journalFolder)
        print(event)

        basename = os.path.basename(event.src_path)

        if not basename.startswith('Journal'):
            return

        print(basename)
        load_json(event.src_path)
        latest_jump = get_latest("FSDJump")

        if latest_jump is not None:
            aaa = main.set_counter_by_name(latest_jump['StarSystem'])
            main.logger.info(f"Set system ({latest_jump['StarSystem']}): {aaa}")

        print(main.Route.counter)


last_event = None  # TODO datetime for last event to precent accidently loading old events
json_data = []


def get_latest_journal(path):
    files = glob.glob(path + "*.log")
    latest = max(files, key=os.path.getctime)
    return latest


def load_json(path):
    global json_data

    json_objects = []

    json_raw = open(path, 'r')

    json_lines = json_raw.readlines()

    # print(json_lines)

    for line in json_lines:
        l = json.loads(line)
        # print(l['event'])
        json_objects.append(l)

    # print(json_objects)

    json_data = json_objects


def get_latest(event_name):
    global json_data

    for event in reversed(json_data):
        try:
            if event['event'] == event_name:
                return event
        except KeyError:
            pass

    return None

    # print(event_name, json_data)


def start_watch(path):
    _observer = Observer()
    event_handler = JournalFileHandler()
    _observer.schedule(event_handler, path=path, recursive=False)
    _observer.start()

    return _observer


def stop_watch(_observer: Observer):
    if _observer is not None:
        _observer.join(5)
