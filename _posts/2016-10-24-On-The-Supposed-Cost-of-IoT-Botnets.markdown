---
layout: post
title:  "On the supposed 'Cost' of IoT Botnets... "
date:   2016-10-24 20:54:34
categories:
- security
- IoT
- botnets
- mirai
---
*Note: The following article is intended to be highly tongue-in-cheek as it points out the glaringly obvious. I do not condone following any of the hypothetical "instructions" outlined in the thought experiment provided. This information is already known to the crooks out there who are doing nasty things to our internet, so its not like writing about it is going to do anyone any harm... The views expressed here are probably my own (on Tuesdays, at least) and do not represent the views of my cat, my employer, or my priest.*

I happened to read [an article][zh-article] today on the supposed "cost" of obtaining your very own IoT (Internet of Trash) botnet, with which you can do a whole bunch of nasty criminal things, including, but not limited to, launching absolutely massive DDoS (Distributed Denial of Service) attacks.

This article I read proclaims that you, yes, you, can have your very own DDoS botnet made of IoT devices for $7,500! All you have to do is go shopping on the "dark net" (lol) with some bitcoins, have a decent amount of ill-will towards someone you want to packet into the stone ages, and hey presto, botnet!

Now, on reading this, I laughed a bit. I happen to [know a few things, maybe][steelconvideo], about the absolutely atrocious state of IoT security, and how trivially abuseable it is.

Anyway, in this bit of writing, I am going to explain why, exactly, the $7,500 figure is an absolute load of bollocks. The real sum of currency required is far, far less. So, to illustrate this, lets step through a hypothetical scenario.

*So you want to build an IoT botnet to DDoS your competitors on Xbox Live...*  

Step 1, obviously, is going to be downloading yourself a copy of the [leaked Mirai source code][miraisrc].

Step 2, you go shopping around for a nice, big, server to host your C&C (command and control) server on, at a hosting provider that does not really give a toss about what you do with it. I won't provide any links to providers, but I found some really, really decent ones for about €40/month that don't really care what you do with them. I, personally, have used them for internet-scale scanning projects in the past. They also, conveniently, accept Bitcoin. Buy two or three of these, from different providers (there is no shortage!), using different aliases/accounts. This way you can have failover C&C servers.

Step 3, is the "slightly hard bit". So you have set up your C&C servers with the handy instructions provided in the Mirai source code. You have a nice, redundant setup that should withstand the oncoming onslaught of abuse reports (more on those in a followup post) for a good while. Now you need to have a think about how to gain a competitive edge over literally every single other script kiddie (just like you!) out there who is intending on running their own IoT botnet.

So what do you do, to get a competitive edge? Well, firstly, you [tweak the scanner source a bit][tweaksrc] so that your bots scan faster, and harder, than everyone else. This gives you a slight competitive edge over the other, unmodified botnets, in terms of getting more infections faster.

Next, you look around at some user-manuals for various IoT rubbish that uses Telnet, by using some [deeply advanced Google queries][googlehax], find some more default user/pass combinations to add to the [huge list provided in Mirai already][mirailist]. This will allow you to infect exciting new devices that no one else is infecting! Bored 14 year old script-kiddies are already up to this, based on my honeypot logs, so why aren't you?

For an even greater competitive edge, for the more discerning hacker with an abundance of free time (read as: a couple of days), you could go as far as to make a modified Mirai to scan for SSH as well as Telnet! Suddenly a whole new world of "stuff to infect" is available to you! You can even reuse the same password list! All you have to do is figure out how to cross compile and link libssh, something that a bit of googling stackoverflow should help you accomplish in minutes :)

Step 4, now, Step 4 is the big, scary part. This is where you, young script kiddie, intent on DDoSing the entire planet, get to put on the big-boy pants and unleash fire and brimstone across the entire cybers by launching your malware! However! You need to get yourself some hosts to act as the "patient zeroes" to launch your infection from!

The cheapest - and simplest - way to go about this is to simply hack yourself a few webservers to launch attacks from. Pick a recent Wordpress Plugin exploit, your favourite DirtyCow localroot exploit, a bit of google dorking, and you will have a handful of webservers to use as a base of infection within minutes! You can either simply infect them with the appropriately compiled Mirai binary (yes, it works on badly secured servers too, not just shitty embedded devices), or use them to do telnet/SSH scanning and infecting yourself. With a couple of boxes that have fat pipes as a base of infection, your botnet will grow to absurd numbers in no time!

Step 5, in which you sit back maniacally cackling and stroking a fluffy white cat, commanding your armies of zombified toasters, and demanding "one beeeeelion dollars" to make the DDoS of whatever stop, is left to your imagination.

Step 6 is really quite simple. Stop postponing the inevitable, and just phone your national police department and hand yourself in, you filthy criminal scum.

So, total cost: 1 week of faffing about (at most), and probably less than €200 in total. Maybe a bit more if you order a heap of pizza while doing it. €200 is a lot less than $7,500, and you get your very own botnet of boxes to launch crimes with.

In conclusion: We are going to see an absolute metric shitload of new Mirai variants cropping up over the next while, as it is an incredibly low-cost and low-effort way to get yourself some absolutely incredible DDoS powers. We are probably also going to see a whole load of poorly thought out and poorly researched articles on "how much an IoT botnet costs". With this article, I intended to simply head off some of those at the pass by pointing out what every script kiddie out there knows - this stuff is super cheap, super nasty, and, unfortunately, super effective.

f you happen to make some kind of internet connected widget or gizmo that probably shouldn't have an IP address attached to it but does because it increases its sale value or whatever, maybe you should consider getting its security tested by people who are good at breaking such things. Maybe me? Maybe someone else? Just get it done by someone, before you end up being one of the vendors that is responsible for the next big onslaught of packets screaming across the wire, and are forever remembered for being yet another criminally negligent bunch of incompetents.

[zh-article]: http://www.zerohedge.com/news/2016-10-24/want-hack-planet-iot-cannon-bring-down-web-can-be-yours-7500
[steelconvideo]: https://www.youtube.com/watch?v=15ZMWldUIx8
[miraisrc]: https://github.com/0x27/linux.mirai
[tweaksrc]: https://github.com/0x27/linux.mirai/blob/master/mirai/bot/scanner.h#L11,L12
[googlehax]: http://lmgtfy.com/?q=filetype%3Apdf+%22default+password%22+%22telnet%22
[mirailist]: http://github.com/0x27/linux.mirai/blob/master/mirai/bot/scanner.c#L123,L185

