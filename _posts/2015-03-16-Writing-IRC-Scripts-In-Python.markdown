---
layout: post
title:  "Writing (Basic) IRC Scripts in Python"
date:   2015-03-16 00:00:00
---
This post is intended to be a gentle introduction into the fine and glorious art of writing IRC scripts (for irssi and hexchat, weechat is on the way) in the Python programming language. In this, you will be walked through, line by line, the "shakespeare.py" plugin for various IRC clients that I wrote out of 
sheer boredom and a desire to insult people on IRC ye olde style.

Hopefully, the following will be comprehensible to all readers, as I try explain every last bit of it so even the total beginner to Python or Computer Science III in general can get 
the gist of it :)

## General Stuff
First off, lets cover some of the general purpose boilerplate crap used in all the scripts.

# So, arrays/lists, and how do they work...
Arrays, or lists, in Python, are really simple. Now, I am not a computer scientist, just a bored hacker. So I make no distinction between an array and a list as they look the same to me. Call me a pleb, but I give no fucks.

You basically have an array like the following:

{% highlight python %}
lol = ['1', '2', '3']
{% endhighlight %}

Now, you can probably see clearly that we can address this in a nice fashion. 

{% highlight python %}
>>> lol = ['1', '2', '3']
>>> print lol[0]
1
>>> print lol[2]
3
>>> print lol[1]
2
>>> print lol
['1', '2', '3']
>>> 
{% endhighlight %}

So we can select elements from our array and print them, without popping them from our array. We can also append items to our array, and remove them from our array, quite easily.

{% highlight python %}
>>> lol = ['1', '2', '3']
>>> lol.append('4')
>>> print lol
['1', '2', '3', '4']
>>> lol.pop(1)
'2'
>>> print lol
['1', '3', '4']
>>> 
{% endhighlight %}

As you can see above, we appended '4' to the array, and popped the first element (which was 2, rememeber, in programming we count from 0). This shows how simple it is to insert and delete items from an array or list. In our program, we make 3 arrays. Each including a bunch of "segments" for an insult.

# Random Selection...
In Python, we can easily do random selection with the module named "random". to randomly select an item from an array, we will simply call the random.choice() function on the array which will return a random element from it.

An example follows:
{% highlight python %}
>>> lol = ['cat', 'dog', 'mouse']
>>> import random
>>> print random.choice(lol)
mouse
>>> print random.choice(lol)
dog
>>> 
{% endhighlight %}

In our scripts, we use this random selection mechanism to select a random item from each array to construct our insult.

# Building our "Insult" from the arrays...
In order to build our insult, we need a random element from each of the arrays, so we can build a string to send.

This is actually really, really, simple. See below.

{% highlight python %}
>>> import random
>>> animals = ['cat', 'dog', 'mouse']
>>> words = ['has', 'is', 'was']
>>> emotion = ['happy', 'sad', 'indifferent']
>>> print "%s %s %s" %(random.choice(animals), random.choice(words), random.choice(emotion))
dog is indifferent
>>> print "%s %s %s" %(random.choice(animals), random.choice(words), random.choice(emotion))
cat was happy
>>> 
{% endhighlight %}

# Interesting Mathematics on how many insults we have...
Now, you may note, that we have 50 insult pieces in each of the arrays. Now, unless I am mistaken (and email me if I am, maths is not my strong suit!), we can use the following maths to work out some shit.  
P(n,r) = number of permutations  
P(50,3) = number of permutations  
50! / (50 - 3)! = number of permutations  
Number of Permutations = 117600  

So hypothetically, we can fire off 117,600 unique insults!

## irssi specific stuff

# Installing irssi-python for development
First off, don't even bother. Just spin up an Arch box, install yaourt, and install it from the fucking AUR. I wasted an entire day trying to get it to build on 2 different Debian 
boxes, and had absolutely no luck. The command to install irssi and irssi-python is as follows. You are more than welcome to try getting it working on Debian or whatever, but be 
warned, you might find yourself jumping off the nearest tall structure before long, due to the sheer amount of fuckery involved.

{% highlight bash %}
yaourt -S irssi-python irssi
{% endhighlight %}

# How irssi scripts accept arguments
IRSSI scripts are a bit fucking wierd in how they accept their arguments. They basically seem to accept them all as "data".

See the following:
{% highlight python %}
def cmd_insult(data, server, witem):
# snip
    if data:
        server.command("MSG %s %s %s" %(witem.name,data, insult))
# snip
{% endhighlight %}

Note how "data" is the first argument passed. This seems to be "all the arguments given to the command", as "server" and "witem" are built in (the current server, and current window name). Data is effectively a string object of arguments that I strongly suspect parsing is left to the user.

# Sending messages to channel
In the above code snippet, you will have noticed the "server.command" function being called. This function sends a raw IRC command to the server. So to send a message to a channel, we must send "MSG <channel> <our message>". This is rather simple, at least!

# Binding commands to functions in irssi
The final bit of importance is how the command is bound in the script, and this is really fucking simple in IRSSI. You simply do the following at the end of your script.

{% highlight python %}
irssi.command_bind('shakespeare', cmd_insult)
{% endhighlight %}

this binds the command "shakespeare" to the function "cmd_insult", and calls said function whenever the "shakespeare" command is called.

# Installing and using the script
To install, after nearly shooting yourself in the face during the compiling hell that is irssi-python, just move shakespeare.py to ~/.irssi/scripts and add "py load shakespeare" to your ~/.irssi/startup somewhere after "load python".

To use, just do /shakespeare to insult no one in particular (the open query window), or /shakespeare $nick to insult a specific user in the current channel.

## Hexchat Specific Stuff

# Installing Hexchat
Hexchat comes with the Python support built in. So... You just install Hexchat, using yaourt/pacman on Arch (I prefer yaourt), or apt on Debian. Those of you on Fedora and other 
"things I don't use" are on your own here. As for the Mac users... I guess homebrew or something?

{% highlight bash %}
yaourt -S hexchat
sudo apt-get install hexchat
{% endhighlight %}

# Module information and suchlike in Hexchat scripts
Hexchat is fucking wierd. You have to intiialize your script with a load of boilerplate bollocks giving the name, version, and description of your script. Otherwise it may complain or something. Anyways, that bullshit looks like this.

{% highlight python %}
__module_name__ = "shakespeare"
__module_version__ = "1.0"
__module_description__ = "Shakespearean Insult Generator"
{% endhighlight %}

# How Hexchat seems to accept arguments
Now, this is something I have not worked out, exactly. It kind of works. Sometimes. Sorta. Well, it takes arguments as "word", similar to "data", except, in what I think is kind of a neat feature, it treats them as an addressable list like sys.argv. So your initial command would be word[0], and first argument word[1], and so on. See the following example.

{% highlight python %}
if len(word) < 2: # we count from 0 in args, but from 1 here. fucked if I know.
    hexchat.command("MSG %s %s" %(channel, insult))
else:
    hexchat.command("MSG %s %s %s" %(channel, word[1], insult)) # see we address arg[1] basically.
{% endhighlight %}

# Sending messages to channel
In the above code snippet, you will have noticed the "hexchat.command" function being called. This function sends a raw IRC command to the server. So to send a message to a channel, we must send "MSG <channel> <our message>". This is rather simple, at least!

# Binding commands to functions in Hexchat
The final bit of importance is how the command is bound in the script, and this is really fucking simple in Hexchat as well. You simply do the following at the end of your script.

{% highlight python %}
hexchat.hook_command("shakespeare", cmd_insult)
{% endhighlight %}

this binds the command "shakespeare" to the function "cmd_insult", and calls said function whenever the "shakespeare" command is called.

# Installing and using the script
Drop it into your "addons" directory in Hexchat, and load it with "/py load shakespeare.py" or add to autoload. Reasonably painless to make work, compared to the absolute motherfuckery that was configuring irssi-python.

To use, just do /shakespeare to insult no one in particular (the open query window), or /shakespeare $nick to insult a specific user in the current channel.

## Source Codes, references.
You can find the source code for the [IRSSI Shakespearean Insult Script Here][irssi-shakespeare-insult], and source for the [Hexchat Shakespearean Insult Script Here][hexchat-shakespeare-insult]. [Hexchat][hexchat] and [IRSSI][irssi] are available at their respective websites, and the [irssi-python][irssi-python] plugin is also available. Documentation for the various clients and such are available on their respective websites.

[irssi]: http://www.irssi.org/
[irssi-python]: https://github.com/mahmoudimus/irssi-python
[hexchat]: https://hexchat.github.io/
[irssi-shakespeare-insult]: https://github.com/0x27/irssi-shakespeare-insult
[hexchat-shakespeare-insult]: https://github.com/0x27/hexchat-shakespeare-insult
