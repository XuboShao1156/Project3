#Create a Simulator object
set ns [new Simulator]

# Set TCP variant
set var1 [lindex $argv 0]
set var1_start [lindex $argv 1]
set var2 [lindex $argv 2]
set var2_start [lindex $argv 3]
# Set  CBR flow rate
set rate [lindex $argv 4]
# Set trace filename
set tracefile [lindex $argv 5]

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

#  n0                     n2
#   \                    /
#    \                  /
#     n1--------------n1
#    /                  \
#   /                    \
#  n3                     n4
#create links between the nodes
#$ns duplex-link node1 node2 bandwidth delay queue-type
#bandwith 10Mbps delaty 10ms
$ns duplex-link $n0 $n1 10Mb 10ms DropTail
$ns duplex-link $n4 $n1 10Mb 10ms DropTail
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n3 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail

#Setup a variant 1 TCP conncection
if {$var1 eq "Reno"} {
	set tcp1 [new Agent/TCP/Reno]
} elseif {$var1 eq "NewReno"} {
	set tcp1 [new Agent/TCP/Newreno]
} elseif {$var1 eq "Vegas"} {
	set tcp1 [new Agent/TCP/Vegas]
}

$tcp1 set class_ 1 
$ns attach-agent $n0 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n3 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 1

#Setup a variant 2 TCP conncection
if {$var2 eq "Reno"} {
    set tcp2 [new Agent/TCP/Reno]
} elseif {$var2 eq "Vegas"} {
    set tcp2 [new Agent/TCP/Vegas]
}

$tcp2 set class_ 2
$ns attach-agent $n4 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n5 $sink2
ns connect $tcp2 $sink2
$tcp2 set fid_ 2

#Set up FTP over TCP variant 1
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

#Set up FTP over TCP variant 2
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP

#set up a UDP connection 
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
set null [new Agent/Null]
$ns attach-agent $n2 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ ${rate}mb
$cbr set random_ false

#Schedule events for the CBR and FTP agents
$ns at 0 "$cbr start"
$ns at var1_start "$ftp1 start"
$ns at var2_start "$ftp2 start"
$ns at 10 "$ftp1 stop"
$ns at 10 "$ftp2 stop"
$ns at 10 "$cbr stop"

#Call the finish procedure after  seconds of simulation time
$ns at 10 "finish"

#Run the simulation
$ns run
