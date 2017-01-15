#!/usr/bin/python2
import commands
import sys

arrayofkeys = ['2414513919131215',
'2392182346014187',
'1388810510235351',
'1711832122467723',
'9713165181361518',
'2051484967516050',
'2371301941197317',
'1908912441811912',
'2181115318112250',
'2141342071812402',
'2281131311558180',
'2431942532042482',
'1451486993295149',
'6715214876986517']

print "(+) Starting Unlock"
for key in arrayofkeys:
    doit = commands.getoutput('fastboot oem unlock %s' %(key))
    if "OKAY" in doit:
        sys.exit("Done!")
    else:
        print "(-) Failed. Trying next..."
        pass
sys.exit("WTF??!")
