import pandas as pd
from numpy import var
import decimal
from scipy.stats import ttest_ind
from analyzer import filter_by_from_and_to_node, filter_by_tcp, load_trace

# variants_pair = [("Reno", "Reno"), ("NewReno", "Reno"), ("Vegas", "Vegas"), ("NewReno", "Vegas")]
variants_pair = [("NewReno", "Vegas")]

def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)

data = pd.read_csv('Project3/stats/expr2.csv')
rate = [i for i in float_range(1, 10.1, 0.1)]

throughput_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', \
    't-statistic[<CBR]', 'p_value[<CBR]','t-statistic[>CBR]', 'p_value[>CBR]'])
drop_rate_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', \
    't-statistic[<CBR]', 'p_value[<CBR]','t-statistic[>CBR]', 'p_value[>CBR]'])
latency_p_values = pd.DataFrame(columns=['Var 1', 'Var 2', 'CBR', \
    't-statistic[<CBR]', 'p_value[<CBR]','t-statistic[>CBR]', 'p_value[>CBR]'])

def filter_by_pair(var1, var2):
    return data[(data['Variant 1'] == var1) & (data['Variant 2'] == var2)]
    
for p in variants_pair:
    for r in rate:
        var1, var2 = p[0], p[1]
        pair_data = filter_by_pair(var1, var2)

        smaller = ttest_ind(pair_data[pair_data['CBR Rate'] < r]['Throughput 1'], \
            pair_data[pair_data['CBR Rate'] < r]['Throughput 2'])
        larger = ttest_ind(pair_data[pair_data['CBR Rate'] > r]['Throughput 1'], \
            pair_data[pair_data['CBR Rate'] > r]['Throughput 2'])
        throughput_p_values.loc[len(throughput_p_values)] = [var1, var2, r, \
            smaller[0], smaller[1], larger[0], larger[1]]

        smaller = ttest_ind(pair_data[pair_data['CBR Rate'] < r]['Drop Rate 1'], \
            pair_data[pair_data['CBR Rate'] < r]['Drop Rate 2'])
        larger = ttest_ind(pair_data[pair_data['CBR Rate'] > r]['Drop Rate 1'], \
            pair_data[pair_data['CBR Rate'] > r]['Drop Rate 2'])
        drop_rate_p_values.loc[len(drop_rate_p_values)] = [var1, var2, r, \
            smaller[0], smaller[1], larger[0], larger[1]]

        smaller = ttest_ind(pair_data[pair_data['CBR Rate'] < r]['Latency 1'], \
            pair_data[pair_data['CBR Rate'] < r]['Latency 2'])
        larger = ttest_ind(pair_data[pair_data['CBR Rate'] > r]['Latency 1'], \
            pair_data[pair_data['CBR Rate'] > r]['Latency 2'])
        latency_p_values.loc[len(latency_p_values)] = [var1, var2, r, \
            smaller[0], smaller[1], larger[0], larger[1]]

throughput_p_values.to_csv('expr2-t-test.csv', index=False)
drop_rate_p_values.to_csv('expr2-t-test.csv', index=False)
latency_p_values.to_csv('expr2-t-test.csv', index=False)
pass