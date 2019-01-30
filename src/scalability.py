from __future__ import absolute_import

import time
import matplotlib.pyplot as plt

from logic.generator import TransactionGenerator

mins = []
maxs = []
avgs = []
# change color in graph!!
# use "g" for factor = 0.5, "b" for factor = "0.8"
trees = [10, 100, 1000]
pattern_factor = 0.2
# try with 0.5, 0.8
for t in trees:
    patterns = int(t * pattern_factor)
    avg_length = 10
    times = []
    for i in range(10):
        start = time.time()
        generator = TransactionGenerator(t, patterns, avg_length, 10, 100, 5)
        g = generator.generate_data()
        finish = time.time()
        times.append(finish - start)
        print("Done dimension %d, iteration %d" % (t, i))
    mins.append(min(times))
    maxs.append(max(times))
    avgs.append(sum(times) / len(times))

plt.figure()
plt.title("#patterns = %f * #transactions" % pattern_factor)
plt.xlabel("Total transactions")
plt.ylabel("Time [s]")
plt.grid()
plt.plot(trees, avgs, 'o-', color="r", label="Response time [s]")
plt.fill_between(trees, mins, maxs, color="r", alpha=0.1)
plt.legend()
plt.savefig("t.pdf")
