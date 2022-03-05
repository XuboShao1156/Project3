import os
import subprocess
import concurrent.futures

variants = ["Reno", "SACK"]
queue = ["DropTail", "RED"]
cbr_start = [1,3,5]
cbr_rate = 10

folder = "expr3"
if not os.path.exists(folder):
    os.mkdir(folder)

def run_ns(variant, queue, cbr_start_time, cbr_rate, fn):
    subprocess.run(["ns", "expr3.tcl", variant, queue, cbr_start_time, cbr_rate, fn])
    print(fn)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for v in variants:
        for q in queue:
            for t in cbr_start:
                for i in range(1, 6):
                    fn = "{}-{}-{}-{}".format(v, q, str(t), str(i))
                    e.submit(run_ns, v, q, str(t), str(cbr_rate), folder + "/" + fn)



