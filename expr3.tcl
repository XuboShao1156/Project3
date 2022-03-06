#Create a Simulator object
set ns [new Simulator]

# Set TCP variant
set var [lindex $argv 0]
# DRoptail or RED 
set queueStr [lindex $argv 1]
# Set start time of CBR
set start [lindex $argv 2]
# Set rate of cbr
set rate [lindex $argv 3]
# Set trace filename
set tracefile [lindex $argv 4]

#Open the trace file (before you start the experiment!)
set tf [open $tracefile.tr w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
 	global ns tf
 	$ns flush-trace
 	close $tf
 	exit 0
}

#Create 6 Nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

if {$queueStr ne "DropTail" && $queueStr ne "RED"} {
	puts "unknown queue style: $queueStr"
	exit
}

#  n0                     n3
#   \                    /
#    \                  /
#     n1--------------n2
#    /                  \
#   /                    \
#  n4                     n5
#create links between the nodes
#$ns duplex-link node1 node2 bandwidth delay queue-type
#bandwith 10Mbps delaty 10ms
$ns duplex-link $n0 $n1 10Mb 10ms $queueStr
$ns duplex-link $n4 $n1 10Mb 10ms $queueStr
$ns duplex-link $n1 $n2 10Mb 10ms $queueStr
$ns duplex-link $n3 $n2 10Mb 10ms $queueStr
$ns duplex-link $n5 $n2 10Mb 10ms $queueStr

#Setup a TCP conncection
if {$var eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
}  elseif {$var eq "SACK"} {
	set tcp [new Agent/TCP/Sack1]
}
$tcp set class_ 1 
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Set up FTP over TCP application
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#set up a UDP connection 
set udp [new Agent/UDP]
$ns attach-agent $n4 $udp
set null [new Agent/Null]
$ns attach-agent $n5 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${rate}mb


#Schedule events for the CBR and FTP agents
$ns at 0 "$ftp start"
$ns at $start "$cbr start"
$ns at 10 "$ftp stop"
$ns at 10 "$cbr stop"

#Call the finish procedure after  seconds of simulation time
$ns at 10.0 "finish"

#Run the simulation
$ns run