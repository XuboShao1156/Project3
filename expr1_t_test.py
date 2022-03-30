import pandas as pd
from numpy import var
import decimal
from scipy.stats import ttest_ind
from analyzer import filter_by_from_and_to_node, filter_by_tcp, load_trace

variants = ["Tahoe", "Reno", "NewReno", "Vegas"]

#using tt_test packages in analyzing.
def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)

data = pd.read_csv('stats/expr1.csv')
rate = [i for i in float_range(1, 10.1, 0.1)]

throughput_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', 'p_value[<CBR]', 'p_value[>CBR]'])
drop_rate_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', 'p_value[<CBR]', 'p_value[>CBR]'])
latency_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', 'p_value[<CBR]', 'p_value[>CBR]'])

for r in rate:
    for i in range(len(variants)):
        for j in range(len(variants)):
            if j <= i:
                continue
            var1, var2 = variants[i], variants[j]

            smaller = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] < r)]['Throughput'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] < r)]['Throughput'])
            larger = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] > r)]['Throughput'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] > r)]['Throughput'])
            throughput_p_values.loc[len(throughput_p_values)] = [var1, var2, r, smaller[1], larger[1]]

            smaller = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] < r)]['Drop Rate'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] < r)]['Drop Rate'])
            larger = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] > r)]['Drop Rate'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] > r)]['Drop Rate'])
            drop_rate_p_values.loc[len(drop_rate_p_values)] = [var1, var2, r, smaller[1], larger[1]]

            smaller = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] < r)]['Latency'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] < r)]['Latency'])
            larger = ttest_ind(data[(data['TCP Variant'] == var1) & (data['CBR Rate'] > r)]['Latency'],
                                data[(data['TCP Variant'] == var2) & (data['CBR Rate'] > r)]['Latency'])
            latency_p_values.loc[len(latency_p_values)] = [var1, var2, r, smaller[1], larger[1]]

throughput_p_values.to_csv('expr1-t-test.csv', index=False)
drop_rate_p_values.to_csv('expr1-t-test.csv', index=False)
latency_p_values.to_csv('expr1-t-test.csv', index=False)
pass
