import time
time_start = time.time()
S = 0
for i in range(1000):
    for j in range(1000):
            S += i + j
time_fin = time.time()
print(time_start)
print(time_fin)
print(time_fin - time_start)