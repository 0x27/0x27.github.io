---
layout: post
title:  "RelayCheck Release"
date:   2015-03-25 13:37:00
---
This blog post is announcing the release of a tool I wrote called [RelayCheck][relaycheck], a simple utility for testing if ones [Tor][torproject] relays are up/down and for giving 
them a good ole kill -HUP every now and then to keep it fresh.

I wrote this when in the past week due to reasons as yet undiagnosed, three of [my tor relays][myrelays] decided to shit themselves and crash for seemingly no reason. I only noticed 
when looking up how much bandwidth they offer, so I wrote this script so I could check on a whim from the commandline with ease. This blog post will outline the fairly simple details 
of the whole shebang.

# How does it work?
Well, to put it simply, it reads in details of your nodes from a JSON configuration file (either in your homedir, as ~/.relaycheck.conf, or specified on commandline), uses SSH to 
connect to them, and checks if Tor is running or sends a HUP command to restart Tor. I only have tested it against Debian hosts, as I don't run any CentOS boxes due to an ingrained 
hatred for everything RHEL. I can always add support for that if needed though :)

# JSON Configuration File
The vital part of this is the JSON configuration file, which the format for is outlined below.

{% highlight python %}
# Example JSON format for the configuration. Note, this assumes you have the same private
# key across all hosts. I will alter it later to use differing privkeys and allow for
# .torrc updating and shit once I can be arsed.
# >>> for host in configuration['hosts']:
# ...     print host['relayname']
# :)
{
    "hosts":[
            {
            "user": "root",
            "port": "22",
            "host": "127.0.0.1",
            "relayname": "Example"
        },
        {
            "user": "root",
            "port": "23",
            "host": "127.0.0.2",
            "relayname": "Example2"
        }
    ]
}
{% endhighlight %}

As you can see, it contains a list called "hosts", containing "host" objects which are dictionaries describing the "user", "port", "host" an "relayname". The "user", "port" and "host" 
are details for SSH to connect to, and the "relayname" is so you can see which relays are up/down using their friendly nicknames as opposed to their DDoS numbers.

Its fairly straightforward, it does, however, assume you have the same authorized key across all the hosts, stored in ~/.ssh/relay.key. I should get around to changing this at a later 
date :)

# SSH bits
I use Paramiko for the SSH component, as it is native python and available via pip or the package manager on virtually any sane OS/distro. I simply am using it to execute commands at 
the moment such as "ps aux | grep tor", "service tor status" and "kill -HUP $(pidof tor)". I will add more functionality such as downloading logfiles and suchlike later when I can be 
bothered to do so using its builtin SCP functionality :)

It should be noted I only am supporting public key based auth with unprotected privatekeys at the moment, I might add support for password based authentication in a later version 
which will maybe require redoing the JSON spec and breaking compatibility possibly. I also hope to add support for protected private keys in the near future once I work out how. 
However, fuck password based auth, its stupid. Public key based authentication is far superior. I have no plans as yet to support various 2FA mechanisms such as duosec or similar.

# Using it.
RelayCheck, currently, has two modes. "restart", and "status". The "restart" mode will just send a HUP to all tor instances on the nodes, and "status" will check if tor is running and 
tell you if so. Positionally, the "mode" is the first argument. The optional second argument is for a configuration file if you have not got one installed into your home directory 
under ~/.relaycheck.conf. 

I guess the best way to see how it runs is to watch this [ASCIICast Demonstration][asciicast] showing how it is working in the wild :D

# Bugs
Use the issue tracker for feature requests, suggestions, and bugs. 

Well, that concludes this software release. Don't forget to run your own tor relay and RTFM :D

[relaycheck]: https://github.com/0x27/relaycheck
[torproject]: https://torproject.org
[myrelays]: http://0x27.me/tor/
[asciicast]: https://asciinema.org/a/17999
