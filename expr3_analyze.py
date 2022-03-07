import os
from pathlib import Path
import analyzer
import numpy as np
import pandas as pd

# time granylarity of a batch for one average value
granularity = 0.1

time_series = [format(i + granularity * 1.0 / 2, '.2f') for i in np.arange(0, 10, granularity)]
headers = ['Variant', 'Queuing', 'CBR Start Time'] \
    + ['TCP Throughput ' + i + 's' for i in time_series] \
    + ['TCP Drop Rate ' + i + 's' for i in time_series] \
    + ['TCP Latency ' + i + 's' for i in time_series] \
    + ['CBR Throughput ' + i + 's' for i in time_series] \
    + ['CBR Drop Rate ' + i + 's' for i in time_series] \
    + ['CBR Latency ' + i + 's' for i in time_series]
stats = pd.DataFrame(columns=headers)

source_folder = 'expr3'
for path in Path(source_folder).glob("*"):
    print('processing {}...'.format(path))

    tokens = path.name[:-len(path.suffix)].split('-')
    variant = tokens[0]
    queuing = tokens[1]
    cbr_start_time = int(tokens[2])

    trace_data = analyzer.load_trace(path)
    tcp_data = analyzer.filter_by_tcp(trace_data)
    cbr_data = analyzer.filter_by_cbr(trace_data)

    tcp_over_time_throughput = []
    tcp_over_time_drop_rate = []
    tcp_over_time_latency = []

    cbr_over_time_throughput = []
    cbr_over_time_drop_rate = []
    cbr_over_time_latency = []

    for start_time in np.arange(0, 10, granularity):
        tcp_parition = tcp_data[(tcp_data['time'] < start_time + granularity) & (tcp_data['time'] >= start_time)]
        tcp_over_time_throughput.append(analyzer.average_throughput(tcp_parition, 1, 2))
        tcp_over_time_drop_rate.append(analyzer.average_drop_rate(tcp_parition, 1, 2))
        tcp_over_time_latency.append(analyzer.average_latency(tcp_parition, 1, 2))

        cbr_parition = cbr_data[(cbr_data['time'] < start_time + granularity) & (cbr_data['time'] >= start_time)]
        cbr_over_time_throughput.append(analyzer.average_throughput(cbr_parition, 1, 2))
        cbr_over_time_drop_rate.append(analyzer.average_drop_rate(cbr_parition, 1, 2))
        cbr_over_time_latency.append(analyzer.average_latency(cbr_parition, 1, 2))

    stats.loc[len(stats)] = [variant, queuing, cbr_start_time] \
        + tcp_over_time_throughput + tcp_over_time_drop_rate + tcp_over_time_latency \
        + cbr_over_time_throughput + cbr_over_time_drop_rate + cbr_over_time_latency

stats = stats.sort_values(headers[:3])
print(stats)
print(stats.loc[:, 'TCP Throughput {}s'.format(granularity/2):'TCP Throughput {}s'.format(10 - granularity/2)])
print(stats.loc[:, 'TCP Drop Rate {}s'.format(granularity/2):'TCP Drop Rate {}s'.format(10 - granularity/2)])
print(stats.loc[:, 'TCP Latency {}s'.format(granularity/2):'TCP Latency {}s'.format(10 - granularity/2)])
print(stats.loc[:, 'CBR Throughput {}s'.format(granularity/2):'CBR Throughput {}s'.format(10 - granularity/2)])
print(stats.loc[:, 'CBR Drop Rate {}s'.format(granularity/2):'CBR Drop Rate {}s'.format(10 - granularity/2)])
print(stats.loc[:, 'CBR Latency {}s'.format(granularity/2):'CBR Latency {}s'.format(10 - granularity/2)])

folder = 'stats'
if not os.path.exists(folder):
    os.mkdir(folder)

stats.to_csv(folder + "/expr3.csv", index=False)

