import os
import subprocess
import concurrent.futures

variants_pair = [("Reno", "Reno"), ("NewReno", "Reno"), ("Vegas", "Vegas"), ("NewReno", "Vegas")]
rate = [i for i in range(1,15)]
start_time = [(0,0),(0,2),(2,0),(0,5),(5,0)]

folder = "expr2"
if not os.path.exists(folder):
    os.mkdir(folder)

def run_ns(var1, time1, var2, time2, cbr_rate, fn):
    subprocess.run(["ns", "expr2.tcl", var1, time1, var2, time2, cbr_rate, fn])
    print(fn)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for p in variants_pair:
        for r in rate:
            for t in start_time:
                fn = "{}-{}-{}-{}-{}".format(p[0], t[0], p[1], t[1], r)
                e.submit(run_ns, p[0], str(t[0]), p[1], str(t[1]), str(r), folder + "/" + fn)
