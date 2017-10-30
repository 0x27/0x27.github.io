---
layout: post
title:  "PureVPN - A Bunch of WTF"
date:   2017-10-30 20:54:34
categories:
- VPN
- snitches
- security
---

So I decided I'd take a look at PureVPN quickly today, because they are a VPN provider who [claim no logs but snitch on their users to the feds](https://torrentfreak.com/purevpn-logs-helped-fbi-net-alleged-cyberstalker-171009/) and frankly, its a Thursday and I am bored. Sure, they snitched on a dude who was probably a shit human being and all, but really, if you are a VPN provider and you lie about having a "No Logs" policy... You are going to get whats coming.

So after I jumped through the hoops of setting up an account there, I decided to look at the "client software" they offer. There are clients for Windows, OSX, etc, along with a DD-WRT applet. Because generally embedded things are fun, I figured I'd look at the "applet" first. I also took a quick look at the Windows client, and got lost in a maze of "what the fuck?"...

## The DD-WRT WTF

So when we go to download some nice router gubbins to make ourselves a SUPER SECURE VPN ROUTER, we see the following...

![lol fucking what](https://raw.githubusercontent.com/0x27/0x27.github.io/master/images/Screenshot_2017-10-26_11-41-19.png)

Oh boy. So what is this downloading? Well, its a shell script, that does some crap and downloads more shit.

```
PUREVPN_APPLET_URL='http://158.69.194.117'
...
PUREVPN_BRANCH='main'
ARCH=$(uname -m)
if [ -e /www/tomato.js ]; then FIRMWARE="tomato"
else FIRMWARE="ddwrt"
fi
...
PUREVPN_VERSION_URL="$PUREVPN_APPLET_URL/cgi-bin/applet-cgi.py?action=version&arch=$ARCH&firmware=$FIRMWARE&branch=$PUREVPN_BRANCH"
PUREVPN_INSTALL_URL="$PUREVPN_APPLET_URL/cgi-bin/applet-cgi.py?action=download&arch=$ARCH&firmware=$FIRMWARE&branch=$PUREVPN_BRANCH"
PUREVPN_HWCHECK_URL="$PUREVPN_APPLET_URL/cgi-bin/applet-cgi.py?action=hwcheck&arch=$ARCH&firmware=$FIRMWARE&branch=$PUREVPN_BRANCH"
...
BOOTSTRAP_ENTRY="
while ! [ -f $PUREVPN_TMP/.lock ] ; do
    mkdir -p $PUREVPN_ROOT/..;
    wget \"$PUREVPN_INSTALL_URL\" -q -O - | gunzip -c | tar -x -C $PUREVPN_ROOT/..;
    $PUREVPN_ROOT/www/scripts/purevpn_startup.sh;
    sleep 5;
done
```

So basically, it downloads more crap over plaintext HTTP from this webserver somewhere and installs it on your router. But what does it install?

```
purevpn$ ls www/
cgi-bin                             iframeResizer.min.js  logo.png    mypage2.sh  purevpn_ddwrt.css  purevpn.js  stylesRouter.css
iframeResizer.contentWindow.min.js  lang.js               mypage1.sh  mypage3.sh  purevpn_ddwrt.js   scripts     template.html
purevpn$
```

Basically a bunch of shell scripts to add web page functionality (that all run as root, just because), that call out to something in cgi-bin...

In "cgi-bin" there exists a nice ARM binary that... Well, we ran out of time. Its written in C++, has a bunch of janky shit in it, and I just wasn't in the mood to reverse it over the weekend after all.

TL;DR of Router Version:
- Installer is "Run this shell script from the internet over a plaintext connection".
- Downloads and executes more shit over the internet and installs shit over the internet that way, via plaintext.
- No code signing or checking whatsoever on the shit it does download.
- Funky ARM binary that smells funny.

## Windows. More WTF.

So I chucked their Windows installer onto a Windows 7 VM I use for testing shite software. First thing I noticed while installing it was that it dropped an absolute shitload of files, and took forever to install. Given it basically relies on OpenVPN, I decided to check out what version they ship. Its 2017, and they are shipping an OpenVPN that was built in 2015, version 2.3.8, built with OpenSSL 1.0.1p. Look these up in the CVE databases at your own pleasure for a good giggle.

![lol again](https://raw.githubusercontent.com/0x27/0x27.github.io/master/images/Screenshot_2017-10-26_11-50-23.png)

They create some services, so I figured I'd be a bit lazy and find an easy win here. So I checked with [PowerSploit's PowerUp](https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc) by doing "Invoke-AllChecks", and well, we came out with some results.

![more lol](https://raw.githubusercontent.com/0x27/0x27.github.io/master/images/Screenshot_2017-10-26_11-59-41.png)  
![even more lol](https://raw.githubusercontent.com/0x27/0x27.github.io/master/images/Screenshot_2017-10-26_12-05-16.png)  

TL;DR: use any the following to get privesc:
```
Invoke-ServiceAbuse -Name 'OpenVPNService'
Invoke-ServiceAbuse -Name 'sevpnclient'
Install-ServiceBinary -name 'sevpnclient'
```

I figured at this point, I'd just move on. BUT WAIT. THERE IS MORE!

So I had a quick look at the files it drops in ```C:\Program Files (x86)\PureVPN``` and spotted ```Injector32.exe``` and ```Injector64.exe```. What the fuck are these? Well, one way to find out... We chuck them into IDA and have a quick gander. Written in .NET, so I broke open dnSpy.

What the fuck its got a DLL injector that injects something called "Split.dll" (or "Split_64.dll") into something. I took a brief look at it, and basically, what happens is the following.

![wtf](https://raw.githubusercontent.com/0x27/0x27.github.io/master/images/Screenshot_2017-10-26_13-35-43.png)

1. It takes 1 argument, which is a process to launch.
2. It launches this process, suspends it, opens its process memory, chucks in the "Split.dll", creates a remote thread for it, and then continues execution.
3. Exits. DLL is now injected.

Effectively, if you put your "Split.dll" (for x86), or "Split_64.dll" in the same directory as "Injector$ARCH.exe" and run the injector program with a path to something to inject into, you win the game and have a DLL injected somewhere. I tested this by copying the injector to ```C:\work\```, putting a meterpreter DLL as "Split.dll" into there, and running it with the path to notepad.exe as the only argument. It worked. I got a meterpreter.

So what have we learned? PureVPN ships some awesome shit we can use for malware reasons!

I didn't bother looking any further after this. I want to spend some time reversing the DLL it injects, but somehow I ended up having some actual work to do instead. I also want to know why its injecting crap into things...
