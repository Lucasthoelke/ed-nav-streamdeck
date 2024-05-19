from streamdeck_sdk import (
    StreamDeck,
    Action,
    events_received_objs,
    logger,
)
import json
import pyperclip

import settings
import journal_handler as journal_handler

infoFile = "C:\\Users\\lucas\\Documents\\Projects\\ED\\sd\\xyz.thoelkle.edroute.sdPlugin\\logs\\info.txt" # This is the file used as a 'gui'
routeJson = "C:\\Users\\lucas\\Documents\\Projects\\ED\\sd\\xyz.thoelkle.edroute.sdPlugin\\routes\\97517BF8-E7D9-11EE-8510-E2449E6004CC.json" #Input json from Spansh backend
journalFolder = "C:\\Users\\lucas\\Saved Games\\Frontier Developments\\Elite Dangerous\\"


class Route():
    counter = 0
    data = None
    auto_journal = False


_route = Route()


def loadRoute():
    jsonRaw = open(routeJson, 'r')
    data = json.load(jsonRaw)
    _route.data = data['result']


def write_info_file():
    when_refuel, when_neutron = get_next_stats()

    if _route.counter <= len(_route.data['jumps']):
        current = _route.data['jumps'][_route.counter]
        current_name = current['name']
        current_refuel = current['must_refuel']
        current_neutron = current['has_neutron']
    else:
        current = None
        current_name = ""
        current_refuel = ""
        current_neutron = ""

    if _route.counter + 1 < len(_route.data['jumps']):
        next_jump = _route.data['jumps'][_route.counter + 1]
        next_name = next_jump['name']
        next_refuel = next_jump['must_refuel']

        next_neutron = next_jump['has_neutron']
    else:
        next_jump = None
        next_name = ""
        next_refuel = ""
        next_neutron = ""

    file = open(infoFile, "w")
    file.write(f"==========================================\n")
    file.write(f"JMP: {_route.counter}/{len(_route.data['jumps']) - 1}\n")
    file.write(f"CUR: {current_name}\n")
    if current_refuel:
        file.write("[REF] ")

    if current_neutron:
        file.write("{NTR}")

    file.write("\n\n")

    file.write(f"NXT: {next_name}\n")
    if next_refuel:
        file.write("[REF] ")

    if next_neutron:
        file.write("{NTR}")

    file.write(f"\n==========================================\n")
    file.write(f"N. NTR: {when_neutron}\n")
    file.write(f"N. REF: {when_refuel}")
    file.write(f"\n==========================================\n")
    file.close()


def get_next_stats():
    next_refuel = None
    next_neutron = None

    jumps = _route.data['jumps'][_route.counter:]

    index = _route.counter
    for system in jumps:
        # dbg = dbg + f"|{index}: {system['name']}\n"

        if next_refuel is None and system['must_refuel']:
            next_refuel = index - _route.counter

        if next_neutron is None and system['has_neutron']:
            next_neutron = index - _route.counter

        index = index + 1

    return next_refuel, next_neutron


def set_counter_by_name(system_name: str):
    if _route.data is None:
        return "No data"

    jumps = _route.data['jumps']
    found = False

    count = 0
    for jump in jumps:
        # print(jump)
        if jump['name'] == system_name:
            found = True
            _route.counter = count
            write_info_file()
            logger.debug(f"Found? {found}")
            return found

        count = count + 1

    logger.debug(f"Found? {found}")
    return found


class SelectNext(Action):
    UUID = "xyz.thoelke.edroute.next.action"

    def on_key_down(self, obj: events_received_objs.KeyDown):
        _route.counter = _route.counter + 1
        logger.info(f"Count: {_route.counter}")
        write_info_file()


class SelectPrev(Action):
    UUID = "xyz.thoelke.edroute.prev.action"

    def on_key_down(self, obj: events_received_objs.KeyDown):
        _route.counter = _route.counter - 1
        write_info_file()
        logger.info(f"Count: {_route.counter}")
        logger.info("Hello there")


class CopyNext(Action):
    UUID = "xyz.thoelke.edroute.copynext.action"

    def on_key_up(self, obj: events_received_objs.KeyUp):
        if _route.auto_journal:
            latest_journal = journal_handler.get_latest_journal(journalFolder)
            journal_handler.load_json(latest_journal)
            last_jump = journal_handler.get_latest('FSDJump')
            if last_jump is not None:
                set_counter_by_name(last_jump['StarSystem'])
            # logger.debug(f"Latest journal: {journal_handler.get_latest_journal(journalFolder)}")

        pyperclip.copy(_route.data['jumps'][_route.counter + 1]['name'])
        logger.info(_route.data['jumps'][_route.counter + 1]['name'])


class ToggleJournal(Action):
    UUID = "xyz.thoelke.edroute.auto_toggle.action"

    def on_key_up(self, obj: events_received_objs.KeyUp) -> None:
        if obj.payload.state == 1:
            _route.auto_journal = False
        else:
            _route.auto_journal = True


if __name__ == '__main__':
    print("start")

    loadRoute()

    StreamDeck(
        actions=[
            CopyNext(),
            SelectNext(),
            SelectPrev(),
            ToggleJournal()
        ],
        log_file=settings.LOG_FILE_PATH,
        log_level=settings.LOG_LEVEL,
        log_backup_count=1,
    ).run()

    # observer.join()
