from inspect import trace
import pandas as pd

trace_format = ['event','time','from node','to node','pkt type','pkt size','flags','fid','src addr','dst addr','seq num','pkt id']
def load_trace(filepath):
    return pd.read_csv(filepath, sep=' ', names=trace_format)

def filter_by_from_and_to_node(trace_data, from_node, to_node):
    if from_node is not None:
        trace_data = trace_data[trace_data['from node'] == from_node]
    if to_node is not None:
        trace_data = trace_data[trace_data['to node'] == to_node]
    return trace_data

def filter_by_tcp(trace_data):
    return trace_data[(trace_data['pkt type'] == 'tcp') | (trace_data['pkt type'] == 'ack')]

def throughput(trace_data, from_node, to_node):
    trace_data = trace_data[trace_data['event'] == 'r']
    trace_data = filter_by_tcp(filter_by_from_and_to_node(trace_data, from_node, to_node))
    
    count = trace_data.size / len(trace_format)
    if count == 0:
        return 0
    elif count == 1:
        return trace_data['pkt size'].sum() / 1024**2
    else:
        return trace_data['pkt size'].sum() / 1024**2 / (trace_data['time'].max() - trace_data['time'].min())

def drop_rate(trace_data, from_node, to_node):
    trace_data = filter_by_tcp(filter_by_from_and_to_node(trace_data, from_node, to_node))
    drop_data = trace_data[trace_data['event'] == 'd']
    return 0 if drop_data.size == 0 else drop_data.size * 1.0 / trace_data.size 
    
def latency(trace_data, from_node, to_node):
    pass

data = load_trace("./expr1/NewReno-20.tr")
print(data)
print(throughput(data, 1, 2))
print(drop_rate(data, 1, 2))
print(drop_rate(data, 1, 2))