import os
import subprocess
import concurrent.futures

variants = ["Reno", "SACK"]
queue = ["DropTail", "RED"]
cbr_start = [3]
cbr_rate = 4

# tracefile folder
folder = "./expr3"
if not os.path.exists(folder):
    os.mkdir(folder)

# run a ns experiment with given variant, start tim,e rate and tracefile
def run_ns(variant, queue, cbr_start_time, cbr_rate, fn):
    subprocess.run(["ns", "expr3.tcl", variant, queue, cbr_start_time, cbr_rate, fn])
    print(fn)

# run with different parameters
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    for v in variants:
        for q in queue:
            for t in cbr_start:
                fn = "{}-{}-{}".format(v, q, str(t))
                e.submit(run_ns, v, q, str(t), str(cbr_rate), folder + "/" + fn)



