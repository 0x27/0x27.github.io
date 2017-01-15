---
layout: post
title:  "Looking back at the ElasticSearch 'Groovy' Remote Code Execution Vulnerability."
date:   2015-07-15 03:13:37
categories:
- elasticsearch
- exploit
- vulnerability
- security
---
## 4 months ago...  
I was examining using 'ElasticSearch' as a logging mechanism for recording and searching data from a network of honeypots I run. Well, a mixture of ElasticSearch and Kibana, for logging Kippo and suchlike, when I stumbled across a posting on the "Wooyun Drops" Chinese security research blog detailing a vulnerability in the (at the time current) version of ElasticSearch.

This release did not include a fully functional PoC - some details were censored - but it swiftly became apparent that the "Groovy" scripting engine in ElasticSearch could be tricked into loading an arbritary Java class and executing code thanks to Java having this Reflection trick allowing one class to load another.

Essentially, by sending a JSON request to execute a script using the "allowed" Math library, you could load in any other (not allowed) Java functionality you wanted and use functions in them to do things, such as execute shell commands using the Runtime library.

Naturally, [we wrote a functioning proof of concept and immediately published it][xrl-es-elreg], as people were becoming aware of the vulnerability ([Jordan Wright had published his analysis of it][jordan-es]), and it was considered a good way to raise awareness.

You may find the exploit code [here, including a nice Asciicast demo of exploitation in practice][xrl-es-poc]. 

Soon after, the Metasploit Framework had their own variation of the exploit (which gives a Java Meterpreter shell as opposed to my quick and dirty "pseudoshell"), and exploitation in the wild by malicious actors began in earnest.

Most of the exploit attempts we saw were dropping fairly rubbish DDoS malware, heavily documented by the "Malware Must Die" team, they even point to my PoC exploit code at one point as an example of how the vulnerability is being leveraged, and also [well documented by Jordan][jw-monitor] using his [ElasticHoney honeypot][elastichoney].

As of this point in time, there are still thousands of vulnerable instances in the wild, despite rather active exploitation and awareness of the vulnerability. [Most of the exploitation is dropping "ChinaZ.DDoS" or "XOR.DDoS" malware][xorddos], among other variants. These are the 'Chinese' DDoS bots I mentioned before. This appears to indicate that a large number of organizations have completely failed to update their (outdated) ElasticSearch instances.  

If you rely on ElasticSearch, and your ES instance is exposed to the internet, and you are running a version before 1.4.3, well, I got bad news for you - your box is hosed, as is everything connected to it. Time to burn that all down and start again. Just because a bug is not in the news this week, does not make it any less of a threat.
 
[xrl-es-elreg]: http://www.theregister.co.uk/2015/03/10/elastic_search_vuln/
[jordan-es]: http://jordan-wright.com/blog/2015/03/08/elasticsearch-rce-vulnerability-cve-2015-1427/
[xrl-es-poc]: https://github.com/XiphosResearch/exploits/tree/master/ElasticSearch
[jw-monitor]: http://jordan-wright.com/blog/2015/05/11/60-days-of-watching-hackers-attack-elasticsearch/
[elastichoney]: http://jordan-wright.com/blog/2015/05/11/60-days-of-watching-hackers-attack-elasticsearch/
[xorddos]: http://blog.malwaremustdie.org/2015/06/mmd-0034-2015-new-elf.html

