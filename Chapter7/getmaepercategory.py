import re
import glob
from collections import OrderedDict

startdir = "/vol/tensusers2/esanders/VoxPopuli/5LXions/MAEs"

maetot = OrderedDict()
maetot['nr days'] = OrderedDict()
maetot['mono/multi party'] = OrderedDict()
maetot['in/exclude urls'] = OrderedDict()
maetot['in/exclude retweets'] = OrderedDict()
maetot['all/elected parties'] = OrderedDict()
lowmaemeans = OrderedDict()
lowmaemeans['nr days'] = OrderedDict()
lowmaemeans['mono/multi party'] = OrderedDict()
lowmaemeans['in/exclude urls'] = OrderedDict()
lowmaemeans['in/exclude retweets'] = OrderedDict()
lowmaemeans['all/elected parties'] = OrderedDict()
lowestmae = {'2011': 9999, '2012':9999, '2015': 9999, '2017':9999, '2019': 9999}
lowestconf = {}
lowestmaeallyears = 9999


maefilenames = glob.glob(startdir+'/*.txt')
#maefilenames.sort()
for maefilename in maefilenames:
    maeallyears = 0
    #print(maefilename)
    match = re.search('mae_([^_]+)_([^_]+)_([^_]+)_([^_]+)_([^_]+).txt',maefilename)
    if match:
        maeallyears = 0
        nrdays = match.group(1)
        mpname = match.group(2)
        euname = match.group(3)
        ername = match.group(4)
        enname = match.group(5)
        #print(nrdays,monomultipary,inexcludeurls,parties)
        if not nrdays in maetot['nr days']:
            maetot['nr days'][nrdays] = OrderedDict()
        if not mpname in maetot['mono/multi party']:
            maetot['mono/multi party'][mpname] = OrderedDict()
        if not euname in maetot['in/exclude urls']:
            maetot['in/exclude urls'][euname] = OrderedDict()
        if not ername in maetot['in/exclude retweets']:
            maetot['in/exclude retweets'][ername] = OrderedDict()
        if not enname in maetot['all/elected parties']:
            maetot['all/elected parties'][enname] = OrderedDict()

        maefile = open(maefilename)
        for line in maefile:
            linematch = re.search('(\d\d\d\d) \d+ \-\-\-\-\-\-\-\-\-\-\-\- ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+)',line)
            if linematch:
                year = linematch.group(1)
                toterrpercentage = float(linematch.group(2))
                toterrseats = int(linematch.group(3))
                maepercentage = float(linematch.group(4))
                maeseats = float(linematch.group(5))
                if not year in maetot['nr days'][nrdays]:
                    maetot['nr days'][nrdays][year] = []
                if not year in lowmaemeans['nr days']:
                    lowmaemeans['nr days'][year] = 999
                if not year in maetot['mono/multi party'][mpname]:
                    maetot['mono/multi party'][mpname][year] = []
                if not year in lowmaemeans['mono/multi party']:
                    lowmaemeans['mono/multi party'][year] = 999
                if not year in maetot['in/exclude urls'][euname]:
                    maetot['in/exclude urls'][euname][year] = []
                if not year in lowmaemeans['in/exclude urls']:
                    lowmaemeans['in/exclude urls'][year] = 999
                if not year in maetot['in/exclude retweets'][ername]:
                    maetot['in/exclude retweets'][ername][year] = []
                if not year in lowmaemeans['in/exclude retweets']:
                    lowmaemeans['in/exclude retweets'][year] = 999
                if not year in maetot['all/elected parties'][enname]:
                    maetot['all/elected parties'][enname][year] = []
                if not year in lowmaemeans['all/elected parties']:
                    lowmaemeans['all/elected parties'][year]= 999

                maeortotpercentage = toterrpercentage
                #maeortotpercentage = maepercentage
                    
                maetot['nr days'][nrdays][year].append(maeortotpercentage)
                maetot['mono/multi party'][mpname][year].append(maeortotpercentage)
                maetot['in/exclude urls'][euname][year].append(maeortotpercentage)
                maetot['in/exclude retweets'][ername][year].append(maeortotpercentage)
                maetot['all/elected parties'][enname][year].append(maeortotpercentage)

                if maeortotpercentage < lowestmae[year]:
                    lowestmae[year] = maeortotpercentage
                    lowestconf[year] = (nrdays,mpname,euname,ername,enname)
                maeallyears += maeortotpercentage
                
    if maeallyears < lowestmaeallyears:
        lowestmaeallyears = maeallyears
        lowestmaeallyearsconf = (nrdays,mpname,euname,ername,enname)

print("best configuration overall: ",lowestmaeallyearsconf)
print("best configuration per year:")
for year in ('2011','2012','2015','2017','2019'):
    print(year,lowestmae[year],lowestconf[year])
print('- - - - - - -')
        
for category in maetot:
    for value in maetot[category]:
        for year in maetot[category][value]:
            maemean = sum(maetot[category][value][year]) / len(maetot[category][value][year])
            if maemean < lowmaemeans[category][year]:
                lowmaemeans[category][year] = maemean
            
for category in maetot:
    for value in maetot[category]:
        print(category, value)
        for year in maetot[category][value]:
            maemean = sum(maetot[category][value][year]) / len(maetot[category][value][year])
            if maemean == lowmaemeans[category][year]:
                print("%s: %.2f <- lowest" % (year, maemean))
            else:
                print("%s: %.2f" % (year, maemean))
        print('- - - - - - -')
