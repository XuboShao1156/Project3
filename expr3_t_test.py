import pandas as pd
from numpy import var
import decimal
from scipy.stats import ttest_ind
from analyzer import filter_by_from_and_to_node, filter_by_tcp, load_trace

expr3_reno_droptail = pd.read_csv('stats/expr3_reno_droptail_3.csv')
expr3_reno_red = pd.read_csv('stats/expr3_reno_red_3.csv')
expr3_sack_droptail = pd.read_csv('stats/expr3_sack_droptail_3.csv')
expr3_sack_red = pd.read_csv('stats/expr3_sack_red_3.csv')

box = ['expr3_reno_droptail', 'expr3_reno_red', 'expr3_sack_droptail', 'expr3_sack_red']


def ttest1(part1,part2) :
    ttest_result_tcp = ttest_ind(part1['TCP_tp'], part2['TCP_tp']);
    ttest_result_dr = ttest_ind(part1['TCP_dr'], part2['TCP_dr']);
    ttest_result_lt = ttest_ind(part1['TCP_lt'], part2['TCP_lt']);
    print(ttest_result_tcp);
    print(ttest_result_dr);
    print(ttest_result_lt);


ttest1(expr3_sack_red,expr3_reno_red)























#throughput_p_values = pd.DataFrame(columns=['TCP', 'Queue_S', 'p_value[<CBR]', 'p_value[>CBR]'])
#drop_rate_p_values = pd.DataFrame(columns=['TCP', 'Queue_S',  'p_value[<CBR]', 'p_value[>CBR]'])
#latency_p_values = pd.DataFrame(columns=['TCP', 'Queue_S', 'p_value[<CBR]', 'p_value[>CBR]'])


