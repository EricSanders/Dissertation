import re

prevpatfilter = ''
maes = {}
years = ["2011","2012","2015"]
#boundaries = [0,1000,2000,3000,4000,5000,999999999]
boundaries = [0,2500,3000,9999999999]
bestmaedict = {}
for year in years:
    bestmaedict[year] = {}
    bestmaedict["mean"] = {}
    for boundary in boundaries:
        bestmaedict[year][boundary] = {}
        bestmaedict["mean"][boundary] = {}

for i in range(32):
    allmaefilename = "mae_allfilters_" + str(i) + ".txt"
    allmaefile = open(allmaefilename)
    for line in allmaefile:
        #print line
        patmatch = re.search("(\d\d\d\d), \(([^,]*), ([^,]*), \{([^\}]*)",line)
        if patmatch:
            patyear = patmatch.group(1)
            patmae = float(patmatch.group(2))
            patnotweets = int(patmatch.group(3))
            patfilter = patmatch.group(4)
            #print year, mae, notweets

            #print patfilter,prevpatfilter
            if not patfilter == prevpatfilter and not prevpatfilter == '':
                totmae = 0
                totnotweets = 0
                for year in maes:
                    (mae,notweets,filter) = maes[year]
                    totmae += mae
                    totnotweets += notweets
                    for i in range(len(boundaries)):
                        if notweets >= boundaries[i] and notweets < boundaries[i+1]:
                            rightboundary = boundaries[i]
                    #print mae,notweets,rightboundary,year
                    if bestmaedict[year][rightboundary]:
                        (bestmae,bestnotweets,bestfilter) = bestmaedict[year][rightboundary]
                        if mae < bestmae:
                            bestmaedict[year][rightboundary] = (mae,notweets,filter)
                    else:
                       bestmaedict[year][rightboundary] = (mae,notweets,filter)
                meanmae = totmae/len(maes)
                meannotweets = totnotweets/len(maes)
                for i in range(len(boundaries)):
                    if meannotweets >= boundaries[i] and meannotweets < boundaries[i+1]:
                        rightboundary = boundaries[i]
                if bestmaedict["mean"][rightboundary]:
                    (bestmae,bestnotweets,bestfilter) = bestmaedict["mean"][rightboundary]
                    if meanmae < bestmae:
                        bestmaedict["mean"][rightboundary] = (meanmae,meannotweets,filter)
                else:
                    bestmaedict["mean"][rightboundary] = (meanmae,meannotweets,filter)

            maes[patyear] = (patmae,patnotweets,patfilter)
            prevpatfilter = patfilter

    allmaefile.close()

years.append("mean")

for year in years:
    for boundary in boundaries:
        if bestmaedict[year][boundary]:
            (bestmae,bestnotweets,bestfilter) = bestmaedict[year][boundary]
            print year, boundary, bestmae,bestnotweets,bestfilter
