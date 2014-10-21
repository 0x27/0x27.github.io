---
layout: post
title:  "2-Factor Auth for SSH using Twilio API and Python-PAM"
date:   2014-10-21 18:00:00
categories: ssh 2-factor authentication security python PAM twilio api SMS
---
So, first real post here. Inspired by a [post][chokepoint-post] over at the [Chokepoint blog][chokepoint-main], and after recently doing some reading up on the [Twilio][twilio-main] [API][twilio-api], I decided it would be fun to expand their little script to use Twilio instead of [TxtDrop][txtdrop] for the simple reason that Twilio supports a lot more countries (including Ireland and the UK, where I currently reside) than TxtDrop, and so I could have an excuse to mess with Twilio, as I need to get to grips with its API for another project currently under development. I also wanted 2 factor auth for the server I use for IRC.

First off, we have to understand how the Python API for Twilio works for sending a SMS. Below is the example code from their documentation. Please note, I could not for the fucking life of me get this to work with a free Twilio account, and resorted to paying cash fucking money for one in the end.

{% highlight python %}
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXX"
auth_token = "YYYYYYYYYYYYYYYYYY"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+12316851234", from_="+15555555555",
                                     body="Hello there!")
{% endhighlight %}

So, now we know how to send the text message. We modify this example and shove it into a function that accepts a destination phone number and the one time PIN we wish to send.

{% highlight python %}
def send_sms(phone, pin):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=phone, from_="+15555555555", body=pin)
{% endhighlight %}

Literally 2 lines of code. We can add some error handling or whatever later if we are so inclined. I am not, at this time, bothered. Now, to modify StampAuth to use our magical Twilio stuff, we simply ditch the SMS sending class, modify the function calls to the SMS sendy bit, and Bob's yer uncle - it works.

Now, we have not yet looked at the PAM parts of the code... Simply because it took me a while to figure them out!

As you may notice, the "pam" module is never imported. This *seems* to be because in the configuration, pam_python.so is explicitly called to handle the python script. This is not something I have seen before, so I decided against mucking about with it too much... I will eventually study python-pam in more detail in a future post when I figure it out a bit better!

Without further ado... Here is an example run of our little module :)

{% highlight bash %}
$ ssh -ltest unsanitized
Enter one time PIN: 
Password:

Welcome to the twilight zone...
test@unsanitized:~$
{% endhighlight %}

You can download the fork using Twilio on [the github page][twili-pam]

[chokepoint-main]: http://www.chokepoint.net/
[chokepoint-post]: http://www.chokepoint.net/2013/12/simple-ssh-2-factor-pam-python-module.html
[twilio-main]: https://www.twilio.com
[twilio-api]: https://www.twilio.com/docs/python/install
[txtdrop]: http://www.txtdrop.com
[twili-pam]: https://github.com/0x27/twilightpam
[github-0x27]: https://github.com/0x27

