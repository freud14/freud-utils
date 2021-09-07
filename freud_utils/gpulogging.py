import argparse
import multiprocessing as mp

import gpustat

from freud_utils.json import json_dumps


class GPUStatsLogger:

    def __init__(self, filename, *, interval=60.) -> None:
        self.filename = filename
        self.interval = interval
        self.process = None
        self.process_condition = None

    def log_gpustats(self):
        stats = gpustat.new_query().jsonify()
        formatted_stats = json_dumps(stats)

        if self.filename == '-':
            print(formatted_stats)
        else:
            with open(self.filename, 'a') as file_descriptor:
                file_descriptor.write(formatted_stats)
                file_descriptor.write('\n')
                file_descriptor.flush()

    def _log_process(self):
        stop = False
        while not stop:
            if not stop:
                self.log_gpustats()

            self.process_condition.acquire()
            stop = self.process_condition.wait(self.interval)
            self.process_condition.release()

    def start(self):
        self.process_condition = mp.Condition()
        self.process = mp.Process(target=self._log_process)
        self.process.start()

    def stop(self):
        self.process_condition.acquire()
        self.process_condition.notify()
        self.process_condition.release()
        self.process.join()

    def join(self):
        self.process.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return True


def launch(config):
    logger = GPUStatsLogger(config.filename, interval=config.interval)
    logger.start()
    logger.join()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, default='-')
    parser.add_argument('-i', '--interval', type=float, default=60.)
    return parser.parse_args()


def main():
    config = parse_args()
    launch(config)


if __name__ == '__main__':
    main()
