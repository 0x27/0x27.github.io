---
layout: post
title:  "Proposal for a Key Revokation Procedure for Tor Hidden Services"
date:   2014-11-13 23:00:00
---

Warning in advance: I am not a proper cryptographer, and I am not a tor developer. I am just some gobshite on the internet who is going to make some probably incredibly stupid statements in this short posting that might be of interest to people far more intelligent than myself. Also, this is not exactly providing much in the lines of "implementation", it is merely chucking an idea out there for the clever fuckers to figure out the details of ;)

So in light of the recent [FBI/Europol takedowns of a number of tor hidden services][tor takedown], and subsequent [reseizure of the doxbin hidden service][loldoxbin] by persons unknown (nachash was [quite adamant][lolnachash] that it was not him, and that he had given the keys to an interested party), it suddenly came to mind that there might be a need for a key revokation mechanism for tor hidden services - similar to the [revokation method in use with PGP][lolpgp]. Except, obviously, better. 

Anyways. So onions are stored in a [distributed hash table][loldht], which, as the name suggests, is distributed. The hidden service domain is calculated from the public key of a private-public keypair. From what I can understand (and I may be very, very fucking wrong), the DHT basically holds the public key identifiers for each hidden service. Much like a keyserver in the PGP mechanism.

So, what I am proposing is an extension to the DHT protocol to not only allow publishing a hidden service descriptor to the DHT, but a secure revokation mechanism (based on the private key) that would allow a hidden service operator to "kill" a hidden service. Furthermore, a mechanism wherin prior to killing a HS, perhaps the ability to create new keys, sign with the old ones, pop it in the DHT, wait for a consensus mechanism to accept the new service, and then kill the old keys. This would, probably, be needlessly complex, however, so it would likely be best to just go with the revokation mechanism.

Uses for the revokation mechanism would include killing a HS post-compromise (by LE, Government, or malicious hackers) to defend the users of it from impersonation, amongst other things. 


[tor takedown]: http://www.wired.com/2014/11/operation-onymous-dark-web-arrests/
[loldoxbin]: http://www.dailydot.com/politics/doxbin-dark-net/
[lolnachash]: https://twitter.com/loldoxbin/status/531907010158419968
[lolpgp]: https://security.ias.edu/how-revoke-gnupgpgp-signature-key
[loldht]: https://www.torproject.org/docs/hidden-services.html.en
