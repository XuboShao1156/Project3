import os
import decimal
import subprocess
import concurrent.futures

variants = ["Tahoe", "Reno", "NewReno", "Vegas"]

# generate differenet rates for experiments
def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)
rate = ["{:.1f}".format(i) for i in float_range(1, 10.1, 0.1)]

# tracefile folder
folder = "expr1"
if not os.path.exists(folder):
    os.mkdir(folder)

# run a ns experiment with given rate and tracefile
def run_ns(variant, cbr_rate, fn):
    subprocess.run(["ns", "expr1.tcl", variant, cbr_rate, fn])
    print(fn)

# run with different parameters
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for v in variants:
        for r in rate:
            fn = "{}-{}".format(v, r)
            e.submit(run_ns, v, r, folder + "/" + fn)
