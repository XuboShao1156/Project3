#Create a Simulator object
set ns [new Simulator]

# Set TCP variant
set var [lindex $argv 0]
# DRoptail or RED 
set queueStr [lindex $argv 1]

#Open the trace file (before you start the experiment!)
set tf [open my_experimenta3_output.tr w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
 	global ns tf
 	$ns flush-trace
 	close $tf
 	exit 0
}

#Create 6 Nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


#create links between the nodes
#$ns duplex-link node1 node2 bandwidth delay queue-type
#bandwith 10Mbps delaty 10ms
$ns duplex-link $n1 $n2 10Mb 10ms ${queueStr}
$ns duplex-link $n5 $n2 10Mb 10ms ${queueStr}
$ns duplex-link $n2 $n3 10Mb 10ms ${queueStr}
$ns duplex-link $n4 $n3 10Mb 10ms ${queueStr}
$ns duplex-link $n6 $n3 10Mb 10ms ${queueStr}


#Setup a TCP conncection
if {$var eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
}  elseif {$var eq "SACK"} {
	set tcp [new Agent/TCP/Sack1]
}
$tcp set class_ 1 
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Set up FTP over TCP application
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#set up a UDP connection 
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
#$cbr set packet_size_ 1000
$cbr set rate_ 1mb



#Schedule events for the CBR and FTP agents
$ns at 0.1 "$ftp start"
$ns at 3.1 "$cbr start"
$ns at 9.9 "$ftp stop"
$ns at 10.0 "$cbr stop"


#Call the finish procedure after  seconds of simulation time
$ns at 10.0 "finish"



#Run the simulation
$ns run


# Close the trace file (after you finish the experiment!)
close $tf
