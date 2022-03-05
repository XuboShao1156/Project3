import os
import subprocess
import concurrent.futures

variants = ["Tahoe", "Reno", "NewReno", "Vegas"]
rate = [i for i in range(1,11)]

folder = "expr1"
if not os.path.exists(folder):
    os.mkdir(folder)

def run_ns(variant, cbr_rate, fn):
    subprocess.run(["ns", "expr1.tcl", variant, cbr_rate, fn])
    print(fn)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for v in variants:
        for r in rate:
            for i in range(1, 6):
                fn = "{}-{}-{}".format(v, str(r), str(i))
                e.submit(run_ns, v, str(r), folder + "/" + fn)
