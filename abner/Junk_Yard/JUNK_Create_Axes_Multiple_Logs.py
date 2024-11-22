from functools import reduce
import matplotlib.pyplot as plt

max_num_log_per_track = 10
num_tracks = 4
num_logs_per_track = [1, 4, 2, 1]

num_logs = reduce(lambda x, y: x + y, num_logs_per_track)


axs = []
fig = plt.figure()
for t in range(num_tracks):
    base = t * max_num_log_per_track
    print(f"{base=}")
    for n in range(num_logs_per_track[t]):
        axs_tk = base + n
        axs.append(axs_tk)

print(axs)
