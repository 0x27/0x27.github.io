---
layout: post
title:  "Tracking down spies C&C infrastructure for shits and giggles"
date:   2015-07-08 13:37:00
---

This is a quick post to splainz the methodology behind how we were able to make fingerprints for the Hacking Team and Equation Group C&C infrastructure allowing remote identification of their servers, as shown in [The Italian Job](https://github.com/0x27/TheItalianJob) and [Equation Smasher](https://github.com/0x27/EquationSmasher) releases on Github.

Myself and [March](https://twitter.com/_ta0), the rootkit wizard, have been at this kind of thing for quite some time, and have had a great deal of success in enumerating and identifying C&C infrastructure based on various oddities in how they present themselves. A fine example of this was in our [Hunting Red October](http://insecurety.net/?p=729) work prior (which resulted in the "asdic.pl" and "sonar.py" scripts).

Basically, here is a TL;DR on how you, too, can hunt down shitbag spies and other such nasties.

## Step 1: Get samples of the malware and/or IP's of some still active C&C servers.
This is often trivial. Once someone publishes a report, or you get some nasty malware, identify the C&C server (run it in a sandbox or whatever and sniff those sweet, sweet pacotes).

## Step 2: Muck about with the C&C server.
Next up, do a portscan of the C&C server(s). Of particular interest is the callback port. You want to fiddle with that port/service a bit and see if it returns a "weird" or unique banner or response, that you can chuck into [shodan](https://shodan.io) and try identify similar servers.

## Step 3: Fuck with related hosts
The third step is fairly simple. Once you have a list of hosts that also act in the same fashion and "smell" the same (much of this is based on scientific jiggerypokery and general faffing about with them), you portscan those and look for further similarities. Most oftentimes, C&C infrastructure is "cloned" across hosts, so they all will be set up in the same fashion.

## Optional Step 4: Scan the Planet
Optionally, here you can scan the entire planet with masscan or zmap looking for similar hosts that Shodan's crawler might not have hit yet. This gives you a nice list of IP's to compare against netflow logs and also to bang into online sandboxes/AV things to see if theres other samples out there calling back, so you can gather more information and link samples/campaigns together.

## Optional Step 5: Hack the Planet
I have NOT engaged in this hypothetical step, and cannot legally advocate for it, however others such as [Malware.lu in the case of APT-1](https://malware.lu/assets/files/articles/RAP002_APT1_Technical_backstage.1.0.pdf) (warning: PDF link) have done so. Somehow procure a copy of the C&C software in question, fuzz the shit out of it, find some bugs, and own the spying bastards, preferably uninfecting their victims and burning their infrastructure to the ground. I include this step for completeness only, and to point out that there is some recourse to be had.

Good sources of ~~DDoS numbers~~ IP addresses/C&C hosts to initially target for, er, interrogation are reports from [Citizen Lab](https://citizenlab.org/) and AV vendors on the latest and lamest surveillance campaigns. Also, because some espionage campaigns are cheapskates, obtaining copies of widely (ab)used RAT software sold/used by ~~APT's~~ script kiddies (such as Poison Ivy/BlackShades/DarkComet) and analysing those examples is also a fine way to find new, exciting fingerprints (and vulnerabilities...) to go forth and ruin some attackers days.

Further note: If the malware uses a web based (say, written in PHP) web panel, you might be able to fingerprint on HTTP titles or figure out a google-dork or other way of identifying the panel. Think of web panels as vulnerable webapps and apply the same thinking to locating and finding vulnerabilities in them. Quite often the bit of the web panel (the "gate") that the implant calls back to fails miserably at sanitizing inputs to databases or file outputs, so there are often some gloriously exploitable bugs there. See the [Herpesnet teardown/ownage by malware.lu](https://malware.lu/articles/2012/05/21/analysis-and-pownage-of-herpesnet-botnet.html) for some ideas on that :)

Have fun, and be safe. Remember kids - when fucking with C&C's/malware, practice safe hex and wear your balaclavas!
