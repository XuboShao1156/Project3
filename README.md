# Project3

Anlaysis
Through the official [analysis example](http://nile.wpi.edu/NS/analysis.html) for the trace data,
we learnt the format and metrics which we can use to derive some general used properties: throughput, packet drop rate, latency.

## Throughput
The overall formula is `throughput = total bytes / duration`.
From the trace data, we can directly access `packet size` and `sequence number`.
Then `total bytes = packet size * max(sequence number)`.
As for the `duration`, it is what we set in the code.

## Packet Drop Rate
The overall formula is `drop rate = # of drop packets / # of total packets`.
For each drop packet, a drop flag will appear at the start of the line.
Therefore, we can count how many drop packets are in total and use `max(sequence num)` as the total number of packets.

## Latency
For each packet (exclude the dropped ones), there will be two records with the same `packet id`:
one for the send node and one for the receiver node.
The diff of the time in these two records are the latency for that packet.
We can store the latency for all packets so later we can do more anlaysis like average, lowest, highest, 50%, 99%, etc.

## Collect Data
For each TCP variant and CBR configuration, run the script for ten to fifteen times.
Gather the trace data for further analysis.

## Construct Relation
Draw scatter plots to get intuition about the relation between throughput, packet drop rate, latency and CBR flow bandwidth.
Then if possible according the intuition, use statistics method (maybe linear or logistic regression) to conclude the relation.

# Experiment 1: TCP Performance Under Congestion
## Configuration
Configure CBR flow in 1,2,3,etc. until we reach the bottlenect capacity or throughput stop increasing.
In this approach, the CBR flow saturates the network which is the general scenarios for TCP.
The bandwitdh for TCP needs to be test where the throughput stops increasing


## Analysis
Analyze throughput, latency, drop rate as mentioned in [General Anlaysis] part.

# Experiment 2: Fairness Between TCP variants
## Configuration
Same CBR configure as experiment 1.
Add a CBR source at N2 and a sink at N3, then N1 will implement a TCP variant and another TCP variant is implemented in N5.
There will be two TCP streams from N1 to N4 and N5 to N6 and these two flows share the same link between N2 to N3.

## Time Window
For one CBR and each two TCP variants pair,
to make it general, we will overlap the time window in such two ways:
1. CBR starts -> TCP 1 starts -> TCP 2 starts -> both TCP variants end
2. CBR starts -> TCP 2 starts -> TCP 1 starts -> both TCP variants end

## Analysis
We can analyze the average throughput to make sure if one specific variant have higher priority over another.
We can also analyze drop rates and average latency by comparing the result of circumstances that only one variant in the network.
Because we are only able to test two variants in one iteration so we have to run experiment on each possible combination of variants.

# Experiment 3 Infulence of Queuing
## Configuration
Although CBR is no longer varying, but we will need to find a CBR bandwith which causes queueing.
This could be half bandwidth of the network and leave the other half for TCP.
Have one TCP flow (N1-N4) and one CBR/UDP (N5-N6) flow.

