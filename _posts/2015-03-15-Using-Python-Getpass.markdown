---
layout: post
title:  "Using the Python 'getpass' module"
date:   2015-03-15 20:54:34
---
Clifford Sullivan (@cliffsull on twitter) recently asked how to go about safely accepting password input from an interactive program in python.

As you may know, password inputs are generally "masked", so the password is not echoed back to the screen. This is "kind of fucking important" as an attempt at defending against shoulder surfers and other evildoers.

Anyway, in python, there is a module named "getpass" that serves this exact purpose. It is part of the python standard library, so no need to go pip installing it or anything just yet.

I figured it might be useful to make note of it here just so you can see how trivial it is to safely accept user input, and perhaps write a demo app using python-paramiko showing how this might be used in practice.

{% highlight python %}
#!/usr/bin/python2
"""
Example use of "getpass" in python to accept user input
of sensitive information such as passwords without echoing
them back to the screen.

Example Run:
$ python test.py 
Example Getpass Use Script
Input Your Credentials (password will not be echoed)
USER: this is a test username
PASS: 
Printing Your Credentials
{+} USER: this is a test username
{+} PASS: this is a test password
$

As you can see, the "password" input did not echo back
my input. This is useful as it prevents against shoulder
surfers and such evil creatures (well, assuming they dont
just look at the bloody keys you are pressing!!)

- infodox
"""
import getpass # import getpass module

def main():
    print "Example Getpass Use Script"
    print "Input Your Credentials (password will not be echoed)"
    username = raw_input("USER: ") # doesnt matter if we echo username so use raw_input()
    password = getpass.getpass("PASS: ") # use getpass to get passwd without echoing it back
    print "Printing Your Credentials"
    print "{+} USER: %s" %(username) # print username
    print "{+} PASS: %s" %(password) # print the password

if __name__ == "__main__":
    main()
{% endhighlight %}

Now, to show use with Paramiko, say we want to write a program that logs into a remote host, checks uptime, and displays the uptime for you.

In this example, we use raw_input to do this. raw_input is not a good idea for accepting passwords as it echoes back to the terminal, but it is fine for usernames.

{% highlight python %}
#!/usr/bin/python2
import paramiko

def run_ssh_cmd(host, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print "(+) Connecting via SSH to %s" %(ip)
        ssh.connect(ip, username=user, password=passwd)
    except paramiko.AuthenticationException:
	sys.exit("(-) Password or username incorrect!")
    except Exception:
        sys.exit("(-) Connection Failed perhaps?")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read()
    return output

def main():
    address = raw_input("host: ")
    username = raw_input("user: ")
    password = raw_input("pass: ")
    command = "uptime"
    print "(*) Running %s on %s" %(command, address)
    output = run_ssh_cmd(host=address, user=username, passwd=password, cmd=command)
    print output

if __name__ == "__main__":
    main()
{% endhighlight %}

See? it echoes back to the terminal!

{% highlight bash %}
$ python ssh_exec_insecure.py
host: 127.0.0.1
user: packetforger
pass: lolpassword
(*) Running uname on 127.0.0.1
(+) Connecting via SSH to 127.0.0.1
Linux
$ 
{% endhighlight %}


So instead, we use getpass.getpass to do this, and it is a far more safe way to accept the password.

{% highlight python %}
#!/usr/bin/python2
import paramiko
import getpass
 
def run_ssh_cmd(host, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print "(+) Connecting via SSH to %s" %(ip)
        ssh.connect(ip, username=user, password=passwd)
    except paramiko.AuthenticationException:
	sys.exit("(-) Password or username incorrect!")
    except Exception:
        sys.exit("(-) Connection Failed perhaps?")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read()
    return output
 
def main():
    address = raw_input("host: ")
    username = raw_input("user: ")
    password = getpass.getpass("pass: ")
    command = "uptime"
    print "(*) Running %s on %s" %(command, address)
    output = run_ssh_cmd(host=address, user=username, passwd=password, cmd=command)
    print output
 
if __name__ == "__main__":
    main()
{% endhighlight %}


As you can see, it does NOT echo back the password to the terminal!

{% highlight bash %}
$ python ssh_exec_secure.py
host: 127.0.0.1
user: packetforger
pass:
(*) Running uname on 127.0.0.1
(+) Connecting via SSH to 127.0.0.1
Linux
$ 
{% endhighlight %}


Hopefully you will understand the point of all this, and use safer ways to accept user input into your applications :)

Footnote: Currently importing old stuff from old blogs and stuff to one centralized location, which is why you may recognise this from elsewhere. Little identity crisis caused a fragmenting of online presence :P
