import os
import decimal
import subprocess
import concurrent.futures

variants_pair = [("Reno", "Reno"), ("NewReno", "Reno"), ("Vegas", "Vegas"), ("NewReno", "Vegas")]
start_time = [(0,0),(0,2),(2,0),(0,5),(5,0)]

# generate differenet rates for experiments
def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)
rate = ["{:.1f}".format(i) for i in float_range(1, 10.1, 0.1)]

# tracefile folder
folder = "expr2"
if not os.path.exists(folder):
    os.mkdir(folder)

# run a ns experiment with given variant, start tim,e rate and tracefile
def run_ns(var1, time1, var2, time2, cbr_rate, fn):
    subprocess.run(["ns", "expr2.tcl", var1, time1, var2, time2, cbr_rate, fn])
    print(fn)

# run with different parameters
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for p in variants_pair:
        for r in rate:
            for t in start_time:
                fn = "{}-{}-{}-{}-{}".format(p[0], t[0], p[1], t[1], r)
                e.submit(run_ns, p[0], str(t[0]), p[1], str(t[1]), r, folder + "/" + fn)
