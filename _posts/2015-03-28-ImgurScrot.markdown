---
layout: post
title:  "ImgurScrot Release"
date:   2015-03-29 02:00:00
categories:
- projects
- python
- imgur
---
So, bit of code I wrote while halfway going mad arguing with API's at [BrumHack][brumhack] in order to retain my sanity a little. This really, really, simple piece of code basically 
just takes a screenshot using [PyScreenshot][pyscreenshot] and uploads it to [imgur][imgur] using the [imgur api][imgur api].

Now, to use it, just run it. You will need "pyscreenshot" and "requests" installed, which are both available via Pip. The rest is stdlib python. All it does is take a screenshot, 
upload to imgur, and print the URL you can access the image. Grab it from [github here][imgurscrot].

I guess I will first take the time to explain how the python screenshot library is used. See the following commented code block to see how it does its magic.
{% highlight python %}
import pyscreenshot as pyscrot # import pyscreenshot module as pyscrot.
image = pyscrot.grab() # grab the full screen and store the PNG screenshot into the image variable where its kept as a PIL object
image.save("screenshot.png") # save it to the file screenshot.png in CWD.
{% endhighlight %}
Nothing complex about this, if you are interested in the hows and whys of the pyscreenshot modules inner workings, I suggest you have a look at its source code or something.

Obviously, we want to store our image for just long enough to upload it, and writing a tempfile as I originally did is really ugly and tends to be non portable across platforms as 
tempfile locations vary. So... We want our image as base64, in order to upload it. How do we do this...
{% highlight python %}
import pyscreenshot as pyscrot # import pyscreenshot module as pyscrot.
import base64 # import the base64 module
from StringIO import * # import everything from StringIO
image = pyscrot.grab() # grab the full screen and store the PNG screenshot into the image variable where its kept as a PIL object
imgstr = StringIO() # create a StringIO object named imgstr
image.save(imgstr, 'png') # save the image to the StringIO object (treating it like a file)
b64image = base64.standard_b64encode(imgstr.getvalue()) # base64 the string stored in the imgstr object :)
{% endhighlight %}

Now, because the [python imgur library][pyimgur] seems to be hideously broken at the moment and I simply could not get the bastard thing to work even with its own samples, I simply 
decided to use [python-requests][python-requests] to manually make my API calls. Seeing as we are just uploading images anonymously, the only thing we give a shit about is the fact we 
can, er, upload a screenshot.

In order to upload the screenshot, we need to send an Authorization header with our ClientID in it, as part of a POST request containing the base64 encoded image and a title for it. We 
get back a JSON response containing the URL to our image. In this example, our "image title" is Screenshot-<current time and date>.png
{% highlight python %}
import json
import requests
import time
client_id = OUR_CLIENT_ID
headers = {'Authorization': 'Client-ID '+client_id} # authorization header.
data = {'image': b64image, 'title': 'Screenshot-%s' %(time.strftime("%H:%M:%S-%d/%m/%Y"))} # our image as base64 data as the "image" var, title as... title var.
r = requests.post(url="https://api.imgur.com/3/upload.json", data=data, headers=headers) # send the request
lol = json.loads(r.text) # load the json response as ... json
print lol['data']['link'] # print the link to image stored in the json response
{% endhighlight %}

Well, that concludes the explaination of how it works. Have fun :)

[brumhack]: https://www.brumhack.co.uk/
[pyscreenshot]: https://pypi.python.org/pypi/pyscreenshot
[imgur]: https://imgur.com
[imgur api]: https://api.imgur.com
[pyimgur]: https://github.com/Imgur/imgurpython/
[python-requests]: https://pypi.python.org/pypi/requests
[imgurscrot]: https://github.com/0x27/imgurscrot
