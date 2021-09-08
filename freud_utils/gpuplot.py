import os
import sys
import argparse
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

from freud_utils.json import json_loads

KEYS = [
    'temperature.gpu', 'fan.speed', 'utilization.gpu', 'power.draw', 'enforced.power.limit', 'memory.used',
    'memory.total'
]
EXTRA_KEYS = ['processes']
ALL_KEYS = KEYS + EXTRA_KEYS


def launch(config):
    with sys.stdin if config.filename == '-' else open(config.filename, 'r') as fd:
        entries = [json_loads(line) for line in fd]

    query_times = np.array([np.datetime64(entry['query_time']) for entry in entries])

    GPU = namedtuple('GPU', ['index', 'uuid', 'name'])
    gpus = sorted(
        set(
            GPU(index=gpu_entry['index'], uuid=gpu_entry['uuid'], name=gpu_entry['name']) for entry in entries
            for gpu_entry in entry['gpus']))

    gpus_stats = {gpu.uuid: {key: np.zeros(len(query_times)) for key in ALL_KEYS} for gpu in gpus}
    for i, entry in enumerate(entries):
        for gpu_entry in entry['gpus']:
            for key in KEYS:
                gpus_stats[gpu_entry['uuid']][key][i] = gpu_entry[key]

            # Processing special keys (only 'processes' for the moment)
            gpus_stats[gpu_entry['uuid']]['processes'][i] = len(gpu_entry['processes'])

    os.makedirs(config.directory, exist_ok=True)
    for key in ALL_KEYS:
        fig, ax = plt.subplots(dpi=150)
        for gpu in gpus:
            ax.plot(query_times, gpus_stats[gpu.uuid][key], label=f'{gpu.index} - {gpu.name}')
        ax.set_title(key)
        ax.tick_params(axis='x', labelrotation=90)
        fig.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(config.directory, f'{key}.png'))
        fig.savefig(os.path.join(config.directory, f'{key}.pdf'))
        plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, default='-')
    parser.add_argument('directory', type=str)
    return parser.parse_args()


def main():
    config = parse_args()
    launch(config)


if __name__ == '__main__':
    main()
