#!/bin/bash

#take the user input and determine which function to run
#init, kill

function=$1
wlan0=$2
wlan1=$3

if [ $function = "init" ];
    then

    service network-manager stop

    echo "connecting to host AP"
    #connect $wlan0 to host AP
    #copy wpa_supplicant
    cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
    #init wpa_supplicant
    wpa_supplicant -B -c /etc/wpa_supplicant/wpa_supplicant.conf -i $wlan0
    #get DHCP
    dhclient $wlan0
    echo ifconfig $wlan0 | grep inet

    echo "copying hostapd from pRepeater"
    #copy hostapd file to /etc/hostapd/hostapd.conf
    cp ./hostapd.conf /etc/hostapd/hostapd.conf

    echo "copying dnsmasq from pRepeater"
    #copy dnsmasq file to /etc/dnsmasq.conf
    cp ./dnsmasq.conf /etc/dnsmasq.conf

    # set static ip to hosting interface
    echo "setting static host ip"
    ifconfig $wlan1 192.168.123.1 netmask 255.255.255.0 up
    
    echo "init ipv4 forwarding"
    #turn on ipv4 forwarding
    sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

    echo "init ip tables"
    #setup ip tables and init
    iptables -t nat -A POSTROUTING -o $wlan0 -j MASQUERADE
    iptables -A FORWARD -i $wlan0 -o $wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -A FORWARD -i $wlan1 -o $wlan0 -j ACCEPT

    echo "hostapd and dnsmasq services"
    #start hostapd and dnsmasq services
    service hostapd start
    service dnsmasq start

fi

if [ $function = "kill" ];
    then

    #kill wpa_supplicant
    echo "killing wpa_supplicant"
    killall wpa_supplicant

    #flush iptables
    iptables -F
    
    #flush static ip
    ip addr flush dev $wlan1
    
    #stop services
    service hostapd stop
    service dnsmesq stop

    #restart network manager
    service network-manager start

fi