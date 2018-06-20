import subprocess

print "Welcome to Repeater Setup"
print "-------------------"
print ""

clientcorrect = "n"
hostcorrect = "n"

while clientcorrect != "y": 
    #get data from user
    clientif = raw_input("Client Inferface: ")
    clientssid = raw_input("Client SSID: ")
    clientpsk = raw_input("Client PassKey: ")

    #print the data for verification
    clientout = clientif + " will connect to SSID " + clientssid + " using passkey " + clientpsk + "."
    print(clientout)
    clientcorrect = raw_input("Is that correct? (y/n)")


while hostcorrect != "y": 
    #get data from user
    hostif = raw_input("Host Interface: ")
    hostssid = raw_input("Hosting SSID: ")
    hostpsk = raw_input("Hosting PassKey: ")

    #print the data for verification
    hostout = hostif + " will host SSID " + hostssid + " using passkey " + hostpsk + "."
    print(hostout)
    hostcorrect = raw_input("Is that correct? (y/n)")

writefiles = raw_input("Write to files? (y/n) " )
if writefiles == "y":
    #list of needed files
    files = ['dhcpcd.conf', 'dnsmasq.conf', 'hostapd.conf', 'wpa_supplicant.conf']
    #remove the files
    for f in files:
        removefiles = ['rm', f]
        subprocess.Popen(removefiles)
    #create files
    for f in files:
        removefiles = ['touch', f]
        subprocess.Popen(removefiles)

    #write dhcpcd.conf
    file = open("dhcpcd.conf", "w")
    file.write("interface " +  hostif + "\n")
    file.write("static ip_address=192.168.123.1/24\n")
    file.write("static routers=192.168.123.0\n")
    file.close()
    
    #write dnsmasq.conf
    file = open("dnsmasq.conf", "w")
    file.write("interface=" + hostif + "\n")
    file.write("listen-address=192.168.123.1\n")
    file.write("bind-interface\n")
    file.write("server=8.8.8.8\n")
    file.write("domain-needed\n")
    file.write("bogus-priv\n")
    file.write("dhcp-range=192.168.123.100,192.168.123.120,12h\n")
    file.close()
    
    #write hostapd.conf
    file = open('hostapd.conf', 'w')
    file.write('interface=' + hostif + "\n")
    file.write('ssid=' + hostssid + '\n')
    file.write('hw_mode=g\n')
    file.write('channel=6\n')
    file.write('wmm_enabled=1\n')
    file.write('macaddr_acl=0\n')
    file.write('auth_algs=1\n')
    file.write('ignore_broadcast_ssid=0\n')
    file.write('wpa=1\n')
    file.write('wpa_passphrase=' + hostpsk + '\n')
    file.write('wpa_key_mgmt=WPA-PSK\n')
    file.write('wpa_pairwise=TKIP\n')
    file.write('rsn_pairwise=CCMP\n')
    file.close()
    
    #write wpa_supplicant
    file = open('wpa_supplicant.conf' , 'w')
    file.write('network={\n')
    file.write('    ssid="' + clientssid + '"\n')
    file.write('    psk="' + clientpsk + '"\n')
    file.write('}')
    file.close()



initRepeater = raw_input("Initilize Repater? (y/n) ")
if initRepeater == "y":
    print("Starting Repeater")
    args = ['bash', 'repeater.sh', 'init', clientif, hostif]
    subprocess.Popen(args)
