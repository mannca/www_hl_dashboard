import operator
import time

import numpy as np


class Benchmark:
    global_print_function = print

    times_averages = {}

    def __init__(self, description, verbose=True, print_function=global_print_function):
        self.description = description
        self.print_function = print_function
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            self.print_function("Starting timer:\t" + self.description)
            if self.print_function != print:
                self.print_function("\n")
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        if self.verbose:
            self.print_function("Ended timer:\t" + self.description + "\tin " + str(self.interval) + " seconds.")
            if self.print_function != print:
                self.print_function("\n")

        if self.description not in Benchmark.times_averages:
            Benchmark.times_averages[self.description] = []
        Benchmark.times_averages[self.description].append(self.interval)


def get_average_times(print_function=Benchmark.global_print_function):
    for desc, values in sorted(Benchmark.times_averages.items(), key=operator.itemgetter(0)):
        print_function(desc + "\t" + str(np.mean(values)))
        if print_function != print:
            print_function("\n")


def get_all_times(print_function=Benchmark.global_print_function):
    for desc, values in sorted(Benchmark.times_averages.items(), key=operator.itemgetter(0)):
        print_function(desc + "\t" + "\t".join([str(v) for v in values]))
        if print_function != print:
            print_function("\n")


def reset_times():
    Benchmark.times_averages.clear()