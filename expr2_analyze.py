import pandas as pd
import os
import analyzer
from pathlib import Path

headers = ['Variant 1', 'Start Time 1', 'Variant 2', 'Start Time 2', 'CBR Rate',
            'Throughput 1', 'Drop Rate 1', 'Latency 1',
            'Throughput 2', 'Drop Rate 2', 'Latency 2']
stats = pd.DataFrame(columns=headers)

source_folder = 'expr2'
for path in Path(source_folder).glob("*"):
    print('processing {}...'.format(path))

    tokens = path.name[:-len(path.suffix)].split('-')
    variant1 = tokens[0]
    time1 = int(tokens[1])
    variant2 = tokens[2]
    time2 = int(tokens[3])
    cbr_rate = int(tokens[4])

    trace_data = analyzer.filter_by_tcp(analyzer.load_trace(path))
    variant_data1 = trace_data[trace_data['fid'] == 1]
    variant_data2 = trace_data[trace_data['fid'] == 2]

    stats.loc[len(stats)] = [variant1, time1, variant2, time2, cbr_rate,
        analyzer.average_throughput(variant_data1, 1, 2),
        analyzer.average_drop_rate(variant_data1, 1, 2),
        analyzer.average_latency(variant_data1, 1, 2),
        analyzer.average_throughput(variant_data2, 1, 2),
        analyzer.average_drop_rate(variant_data2, 1, 2),
        analyzer.average_latency(variant_data2, 1, 2)]

stats = stats.sort_values(headers[:5])
print(stats)

folder = 'stats'
if not os.path.exists(folder):
    os.mkdir(folder)

stats.to_csv(folder + "/expr2.csv", index=False)