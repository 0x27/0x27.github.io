---
layout: post
title:  "SSH Over SCTP (With Socat)"
date:   2015-07-27 13:37:00
---
This is a quick post, kind of a reposting of a thing I pastebinned about a year ago that has served me REALLY well in evading stupid paywalls in airports and the likes. Also in evading a ridiculous firewall at the Uni I sometimes attend.

The prerequisites are that you have a Linux box (maybe a Mac will work, idk. Not an OSX user but I can test if theres demand for it), a remote server, and a bit of familiarity with the command line.

For the remote server, any server with a public IP address will do so long as you ensure it supports the [SCTP][sctp] protocol. Look up SCTP support for your distribution, usually its the lksctp libraries that need to be installed. DigitalOcean Debian instances and Amazon EC2 Ubuntu instances seem to work fine out of the box. Your local box also needs SCTP support. Again, with Debian, Ubuntu, and Arch Linux, this never seems to be an issue. Finally, you will need SSH access to the remote box, preferably as a user with admin privs so you can set up socat on it and listen on privileged ports.

So, here goes. On the serverside (set this up BEFORE you need it), you will need to install ["socat"][socat] (should be available in your distros repos. If not, compile it from source or something!). Next, you will need to just run the following command in a screen session.

{% highlight bash %}
socat SCTP-LISTEN:80,fork TCP:localhost:22 # assuming you want the SCTP socket to listen on port 80/SCTP and sshd is on 22/TCP
{% endhighlight %}

This will spin up a socat listener on port 80/SCTP, and forward any traffic sent to it through to port 22/TCP on the listening host. Change these ports as you see fit - often I run sshd on a different port (443/TCP) to evade other firewalls and the likes.

Now, on the client side, when you want to connect, you will also need socat working with SCTP support. Same deal as making it work on the serverside. To spin up your socat proxy on local to forward to the remote server, do the following.

{% highlight bash %}
socat TCP-LISTEN:1337,fork SCTP:SERVER_IP:80 # replace SERVER_IP with IP of listening server, and 80 with whatever port the SCTP listener is on :)
{% endhighlight %}

This will spin up a TCP listener on localhost:1337/TCP, which is being forwarded over SCTP to the TCP port at the other end of the tunnel (in my example, port 22). To connect to the sshd at the other end, you just need to ssh to localhost:1337, and to get yourself some SOCKS5 for web browsing through your tunnel, do dynamic port forwarding. The following example sums it up for you.

{% highlight bash %}
ssh -lusername localhost -D 8080 -p 1337 # replace username and -p port value as needed...
{% endhighlight %}

Now you have a working tunnel! You should be ssh'd into your box, and you have a listening SOCKS5 proxy on port 8080 for tunnelling web browsing, email, etc through :)

[sctp]: https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol
[socat]: http://www.dest-unreach.org/socat/
