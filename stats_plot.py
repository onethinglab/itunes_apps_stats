# (c) onethinglab.com
# Plot applications size statistics generated by stats_parser.py

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import json
import os

from time import strptime
from time import mktime
from datetime import datetime
from operator import itemgetter

DATE_FORMAT = "%b %d, %Y"
# default output folder
APPS_DATA_PATH = "./apps_stats"

def get_app_stats(app_data):
    dates = list()
    sizes = list()
    for date_str, size_str in data:
        dt = datetime.fromtimestamp(
            mktime(strptime(date_str, DATE_FORMAT)))
        dates.append(mdates.date2num(dt))
        # exclude units
        app_size = float(size_str.split()[0])
        sizes.append(app_size)
    return dates, sizes

# change matplotlib output style
plt.style.use("bmh")
apps_stats_files = os.listdir(APPS_DATA_PATH)
figure, axes = plt.subplots(len(apps_stats_files), 1, figsize=(10,60))
for app_file, ax in zip(apps_stats_files, axes):
    with open(os.path.join(APPS_DATA_PATH, app_file)) as fp:
        data = json.load(fp)
        # sort by date
        data.sort(key=lambda value: strptime(value[0], DATE_FORMAT))
        dates, sizes = get_app_stats(data)
        text = ax.set_title(app_file.split(".")[0])
        text.set_color("#C70039")
        ax.plot_date(x=dates, y=sizes, fmt="-")
        ax.set_xlabel("Release Date")
        ax.set_ylabel("Size in MB")
        ax.tick_params(axis='x', colors='MAROON')
        ax.tick_params(axis='y', colors='MAROON')
figure.tight_layout()
plt.savefig("./apps_stats.png")
