# QuakeMap-Map Documentation (v2.2.1)

# 1. Summary

> Server-side Operations (_/api/earthquake_info_)

Upon initialization of the server, the server will regularly update the earthquake information from _P2PQuake_ Server,
as well as the EEWs from _Kmoni_ and (_SVIR_ or _Iedred_) Servers.
(See _2-Server Routine Description_)

During normal times, when no EEWs are issued, the server will push previous earthquake information to the API (In _info_
section).

The server will **ALWAYS** get information from both the earthquake information API and the EEW API, no matter the EEWs
are issued or not.

During the time while EEWs are in effect, the server will choose an information from both EEW servers to push out in _
eew_ section.

> **NOTE:** The information was gzipped. In normal circumstances, the file size will **NOT** exceed 5 Mb.

> Browser-side Operations (_/map_)

The client will first set the language (Not finished yet), and initialize the map. It'll also get the server-side API (_
/api/earthquake_info_)
with an interval of **2 seconds**.

After receiving the server API's data, it'll decide whether to show EEW or earthquake information (See _3-Client Routine
Description_).

> **NOTE:** For now (version 2.2.1), the map **ONLY** supports single EEW.
> That means, when multiple EEWs with different EventIds occur,
> It'll only display them in time order, but not separating them.