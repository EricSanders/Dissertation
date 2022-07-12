import potwan
import itertools
import multiprocessing
import sys

mypart = int(sys.argv[1])


annotationvalues = ['subjectief','sarcastisch','positief_stemadvies','negatief_stemadvies','positief','negatief','beargumenteerd','positieve_stembekenning','negatieve_stembekenning','geen_politiek','multiparty']
filtervalues = [-1,0,1,2]
#annotationvalues = ['positief','negatief','geen_politiek','multiparty']
#filtervalues = [-1,0,1,2]

count = 0
filters = {}

prediction = potwan.Prediction()
#print "importing tweets..."
prediction.importtweets()
#print "done"
electionpercentages = prediction.getpercentages(set='electionresults')


def doit(permutation):
    #print permutation
    maes = {}
    for i in range(len(permutation)):
        filters[annotationvalues[i]] = permutation[i]

    prediction.countparties(filters=filters)
    #print prediction.getpartycounts()
    tweetpercentages = prediction.getpercentages(set='partycounts')
    tweetsincount = prediction.gettweetsincount()
    #print tweetpercentages
    for year in tweetpercentages:
        if year in tweetpercentages and year in electionpercentages:
            mae = prediction.getmae(tweetpercentages[year],electionpercentages[year])
            #print mae
            maes[year] = mae,tweetsincount[year],filters

    return maes

combinations = itertools.product(filtervalues,repeat=len(annotationvalues))
combinationslist = []
for combination in combinations:
    combinationlist = []
    for nr in combination:
        combinationlist.append(nr)
    combinationslist.append(combinationlist)

parts = {}
partlength = len(combinationslist) / 32
for nr in range(31):
    parts[nr] = (nr * partlength, (nr+1) * partlength - 1)
parts[31] = (31 * partlength, len(combinationslist) - 1)

#mypart = 13
outfilename = "mae_allfilters_" + str(mypart) + ".txt"
outfile = open(outfilename,"w")
(start,end) = parts[mypart]
for i in range(start,end):
    permutation = combinationslist[i]
    result = doit(permutation)
    for year in result:
        outfile.write(str(year) + ", " + str(result[year]) + "\n")

outfile.close()

#p = multiprocessing.Pool()
#results = p.map(doit,combinationslist)

#for result in results:
    #for year in result:
        #print(year, result[year])

