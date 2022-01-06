# Unity Edge HTTP Server over TCP/IP

![screenshot3](https://github.com/TheMindVirus/metaverse/blob/main/Networking/screenshot3.png)

## Brief

This package provides HTTP Server functionality for Unity Desktop Applications \
being deployed as Edge Servers, to be connected to various WebApp and Game Engines \
forming what can be considered as a Local/Wide Area Metaverse (LAM/WAM).

## Integration

In the current state, the scripts provided by this package require minimal tweaking. \
The only tweaking that is required is that it needs to be integrated per game engine. \
By design it is interoperable with any Internet HTTP Server System using TCP/IPv4.

* Running Dedicated Game Servers on the Cloud requires Subscriptions \
and faces problems of User Isolation, Moderation and Tight Security Restrictions.
* Running the same workload on a modern Mobile Device is entirely possible \
but faces problems of Power Consumption, Signal Integrity and Privacy.
* A Desktop PC deployed as an Edge Server provides the right infrastructure \
for the Networking and Graphics API's that this workload requires.

Cluster PC's running Windows and Unity with Real Time Ray-Traced Graphics \
are recommended, along with Node-Red and other Web-based Frameworks. \
Alternative setups may include a Turing Pi running Wine or a \
Seeed Studio Odyssey with M.2 RTX Graphics inside an Alienware Alpha \
running Steam-OS or Arch Linux.

## Issues

Integration with Steam as the Dedicated Server for titles that support it is ideal, \
but it also requires Steam to support **Background Instances** for Games and Tools. \
Currently, it requires you to either only run games with built-in multiplayer servers \
once per account, or to set up several accounts with unnecessary duplicate purchases.

Addresses take the form `application.hostname.domain:10000` \
or optionally if port 80 is forwarded to port 10000 by your router, \
just `application.hostname.domain` like a normal website.

Port 80 is reserved for Traditional Web Server use by various applications. \
It is also restricted from being opened in Unity or Python by Windows Firewall. \
Other operating systems may have different routing and permissions issues to be overcome.

![screenshot4](https://github.com/TheMindVirus/metaverse/blob/main/Networking/screenshot4.png)
