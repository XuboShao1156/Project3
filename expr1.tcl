#Create a Simulator object
set ns [new Simulator]

# Set TCP variant
set var [lindex $argv 0]
# Set  CBR flow rate
set rate [lindex $argv 1]
# Set trace filename
set tracefile [lindex $argv 2]

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
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


#create links between the nodes
#$ns duplex-link node1 node2 bandwidth delay queue-type
#bandwith 10Mbps delaty 10ms
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n6 $n3 10Mb 10ms DropTail

#Setup a TCP conncection
if {$var eq "Tahoe"} {
	set tcp [new Agent/TCP]
} elseif {$var eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
} elseif {$var eq "NewReno"} {
	set tcp [new Agent/TCP/Newreno]
} elseif {$var eq "Vegas"} {
	set tcp [new Agent/TCP/Vegas]
}

$tcp set class_ 2 
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
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
#$cbr set packet_size_ 1000
$cbr set rate_ ${rate}mb



#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 0.1 "$ftp start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"


#Call the finish procedure after  seconds of simulation time
$ns at 10.0 "finish"



#Run the simulation
$ns run


# Close the trace file (after you finish the experiment!)
close $tf
