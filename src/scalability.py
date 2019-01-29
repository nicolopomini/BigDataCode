from __future__ import absolute_import

import time
import matplotlib.pyplot as plt

from logic.generator import TransactionGenerator

mins = []
maxs = []
avgs = []

trees = [10, 100, 1000, 10000, 100000]
for t in trees:
    patterns = t
    avg_length = 10
    times = []
    for _ in range(10):
        start = time.time()
        generator = TransactionGenerator(t, patterns, avg_length, 10, 100, 5)
        g = generator.generate_data()
        finish = time.time()
        times.append(finish - start)
    mins.append(min(times))
    maxs.append(max(times))
    avgs.append(sum(times) / len(times))

plt.figure()
plt.title("#patterns = #transactions")
plt.xlabel("Total transactions")
plt.ylabel("Time [s]")
plt.grid()
plt.plot(trees, avgs, 'o-', color="r", label="Response time [s]")
plt.fill_between(trees, mins, maxs, color="r", alpha=0.1)
plt.legend()
plt.savefig("t.pdf")
