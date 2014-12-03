---
layout: post
title:  "PHP Extension Backdoor."
date:   2014-12-08 23:00:00
---

This article is not exactly original content, but an annotated translation of [an article that appeared on a Russian site][russian], with some additions/modifications made along with some extra details on how it all works, and a client utility for accessing the backdoor.

It should be noted, my Russian is fairly fucking terrible, and this is not an *exact* translation of the original, as I took a few liberties here and there.

Today we will talk about writing a backdoor for PHP as an extension. As a rule, most hackers leave their PHP backdoors either as scripts on the server itself (C99 shells, etc), or backdoor existing scripts on the server. These kinds of backdoor are easy to find via static analysis (grep, etc) of the code, or searching for modifications. Such backdoors are also quite limited insofar as they are restricted by settings in php.ini such as disable_functions. Therefore, the benefits of backdooring via writing an extension are obvious.

* Harder to find - no scripts left in the webroot or modifications to existing scripts.
* Bypass of disable_functions
* Ability to control all of the code as opposed to relying on PHP
* Access to code execution via hidden backdoor.

Unfortunately, we still need to be able to edit the PHP configuration (php.ini) to enable such a backdoor in the PHP interpreter at this time (note: on Windows, DLL search path hijacking of an extant extension may be possible. LD_PRELOAD on Linux is another option for injecting a backdoor into PHP, but neither of those topics are to be discussed in this article).

As an example, I will write such a backdoor for Windows (note: a linux extension is also provided). To write extensions I use Visual Studio 2012 Express Edition. We also need the source code of the version of PHP we intend to target and build the PHP libraries (available in the PHP source code). For simplicitys sake download [php-5.5.15-Win32-VC11-x86][phpdl1] and [php-5.5.15-src.zip][phpdl2].

Unpack the built PHP in C:\php, and sourcecode in C:\php-src.

Next, you need to configure some settings in Visual Studio. (note: I redid the whole thing as opposed to using the Russian screenshots).

1. Add the preprocessor definitions.
{% highlight bash %}
Zend_Debug = 0
ZTS = 1
ZEND_WIN32
PHP_WIN32
{% endhighlight %}

<screenshot>

2. Add the directories for building the source.
{% highlight bash %}
C:\php-src\main;
C:\php-src\Zend;
C:\php-src\TSRM;
C:\php-src\regex;
C:\php-src;
{% endhighlight %}

<screenshot>

3. Add the additional directory for the library libphp5ts.lib
{% highlight bash %}
C:\php\dev
{% endhighlight %}

<screenshot>

4. Add the library php5ts.lib

<screenshot>

5. Specify the path for the compiled file to be output.

<screenshot>

6. 

[russian]: http://stackoff.ru/pishem-rasshirenie-bekdor-dlya-php/


