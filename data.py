from datetime import datetime, timedelta
from pathlib import Path
import requests
import re
import json
import csv

"""
This script checks the availability of library spaces.
import data and call get_data() to get the availability data.
spaces_name and counter are the two variables returned by get_data().
spaces_name is a list of tuples containing room name and capacity.
counter is a dictionary with room id as key and number of available slots as value.
"""

LIDS = [(6539, "Langson Library"), (6579, "Gateway Study Center"), (6580, "Science Library"), (6581, "Multimedia Resources Center"), (12189, "Grunigen Medical Library")]


def slot_processor(slots, counter_dict):
    for slot in slots:
        if "className" not in slot:
            try:
                counter_dict[str(slot['itemId'])] += 1
            except KeyError:
                pass


def get_data():
    all_spaces = requests.get('https://spaces.lib.uci.edu/allspaces').text.strip()
    all_spaces = re.findall(r'resources\.push\(\s*(.*?)\s*\);', all_spaces, re.DOTALL)
    spaces_name = [(re.search(r'eid: (.*?),', space).group(1),
                    re.search(r'title: \"(.*?)\",', space).group(1).replace("\\u0020", " ").replace(
                        "\\u0028", "(").replace("\\u0029", ")").replace("\\u002D", "-")) for space in all_spaces]
    counter = {space[0]: 0 for space in spaces_name}

    for ids in LIDS:
        ids = ids[0]
        data = {
            "lid": ids,
            "gid": 0,
            "eid": -1,
            "seat": False,
            "seatId": 0,
            "zone": 0,
            "start": datetime.now().date().isoformat(),
            "end": (datetime.now() + timedelta(days = 1)).date().isoformat(),
            "pageIndex": 0,
            "pageSize": 18
        }
        headers = {
            "referer": "https://spaces.lib.uci.edu/allspaces",
        }
        grid_langson = requests.post("https://spaces.lib.uci.edu/spaces/availability/grid",
                                     data = data, headers = headers).content
        grid_langson = json.loads(grid_langson)['slots']

        slot_processor(grid_langson, counter)

    return spaces_name, counter


def print_availability_report(names, counter_dict):
    print("========Availability Report========")
    print(f"Library Checked: {', '.join([library[1] for library in LIDS])}")
    print("Report Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("===================================")
    for name in names:
        if name[0] in counter_dict:
            print(f"{name[1]}: {counter_dict[name[0]]} slots available")
        else:
            print(f"{name[1]}: No data available")
    print("===========END OF REPORT===========")
    print()

def log_data(names, counter_dict):
    now = datetime.now()
    csv_path = Path("data_pt.csv")
    if not csv_path.exists():
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Availability", "Time"])

    total_available = 0
    for name in names:
        total_available += counter_dict[name[0]]

    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        time = None
        if datetime.now().hour < 12:
            time = f"{now.month}/{now.day}: FIRST_HALF"
        else:
            time = f"{now.month}/{now.day}: LAST_HALF"
        writer.writerow([total_available, time])

if __name__ == '__main__':
    spaces_names, slot_counter = get_data()
    print_availability_report(spaces_names, slot_counter)
    log_data(spaces_names, slot_counter)
