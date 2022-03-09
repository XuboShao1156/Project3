import pandas as pd
import os
import analyzer
from pathlib import Path

headers = ['TCP Variant', 'CBR Rate', 'Throughput', 'Drop Rate', 'Latency']
stats = pd.DataFrame(columns=headers)

source_folder = 'expr1'
for path in Path(source_folder).glob("*"):
    print('processing {}...'.format(path))

    tokens = path.name[:-len(path.suffix)].split('-')
    variant = tokens[0]
    cbr_rate = float(tokens[1])

    trace_data = analyzer.filter_by_tcp(analyzer.load_trace(path))
    stats.loc[len(stats)] = [variant, cbr_rate,
        analyzer.average_throughput(trace_data, 1, 2),
        analyzer.average_drop_rate(trace_data, 1, 2),
        analyzer.average_latency(trace_data, 1, 2)]

stats = stats.sort_values(headers[:3])
print(stats)

folder = 'stats'
if not os.path.exists(folder):
    os.mkdir(folder)

stats.to_csv(folder + "/expr1.csv", index=False)