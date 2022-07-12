import os
import subprocess
import glob
import re
import sys
import configparser
import ast
import datetime

class Classification:
    def __init__(self, inputfile, labelfile, module_featurize, ngrams, minimum_token_frequency, featuretypes, frogconfig, module_validate, classifier_args, classifier, balance, weight, prune):
        self.inputfile = inputfile
        self.module_featurize = module_featurize
        self.ngrams = ngrams
        self.minimum_token_frequency = str(minimum_token_frequency)
        self.featuretypes = featuretypes
        self.frogconfig = frogconfig
        self.module_validate = module_validate
        self.classifier_args = classifier_args
        self.classifier = classifier
        self.balance = ''
        if balance:
            self.balance = '--balance'
        self.weight = weight
        self.prune = str(prune)

        self.inputfiledir = os.path.dirname(inputfile)
        self.inputfilebasename = os.path.basename(inputfile)
        self.inputfilebasenamenoext = os.path.splitext(self.inputfilebasename)[0]
        self.features = self.inputfilebasenamenoext + '.features.npz' 
        self.labels = self.inputfiledir + '/' + self.inputfilebasenamenoext + '.labels'
        if labelfile:
            self.labels = labelfile
        self.labelsbasename = os.path.basename(self.labels)
        self.vocabulary = self.inputfilebasenamenoext + '.vocabulary.txt'
        self.frog = self.inputfilebasenamenoext + '.frog.json'

        self.classifier_argsbasename = os.path.basename(self.classifier_args)
        
    def Featurize(self,outputdir):
        os.chdir(outputdir)

        command = 'ln -s '+ self.inputfile + ' .'
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'luiginlp Featurize --module ' + self.module_featurize + ' --inputfile ' + self.inputfilebasename + ' --ngrams ' + self.ngrams + ' --minimum-token-frequency ' + self.minimum_token_frequency + ' --featuretypes ' + self.featuretypes + ' --frogconfig ' + self.frogconfig
        commandlist = []
        commandlisttmp = command.split(" ")
        for commandpart in commandlisttmp:
            commandpart = re.sub("(\d)_(?=\d)",r"\1 ",commandpart)
            commandlist.append(commandpart)
        print(commandlist)
        subprocess.run(commandlist)


    def Validate(self,outputdir,featuresdir):
        os.chdir(outputdir)

        command = 'ln -s '+ self.inputfile + ' .'
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'ln -s '+ self.labels + ' .'
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'ln -s '+ self.classifier_args + ' .'
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'ln -s '+ featuresdir + '/' + self.features + ' .' # + n_xgram.minmintokfreq.lower_False.black_false
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'ln -s '+ featuresdir + '/' + self.vocabulary + ' .' # + n_xgram.minmintokfreq.lower_False.black_false
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        command = 'ln -s '+ featuresdir + '/' + self.frog + ' .'
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

        if self.balance:
            command = 'luiginlp Validate --module ' + self.module_validate + ' --instances ' + self.features + ' --labels ' + self.labelsbasename + ' --docs ' + self.inputfilebasename + ' --classifier ' + self.classifier + ' ' + self.balance + ' --weight ' + self.weight + ' --prune ' + self.prune  #module_nfoldcvsparse  -> module_validate etc.
        else:
            command = 'luiginlp Validate --module ' + self.module_validate + ' --instances ' + self.features + ' --labels ' + self.labelsbasename + ' --docs ' + self.inputfilebasename + ' --classifier ' + self.classifier + ' --weight ' + self.weight + ' --prune ' + self.prune  #module_nfoldcvsparse  -> module_validate etc.
        commandlist = command.split(" ")
        print(commandlist)
        subprocess.run(commandlist)

class GridSearchClassification:
    def __init__(self):
        self.performances = []
        self.parametercombinations = []

    def readconfig(self,configfile='config.ini'):
        config = configparser.ConfigParser()
        config.read(configfile)
        self.inputfile = config['IO']['inputfile']
        self.labelfile = config['IO']['labelfile']
        self.startoutputdir = config['IO']['outputdir']
        self.performanceoutputfilename = config['IO']['performancefile']
        self.performanceperparameteroutputfilename = config['IO']['performanceperparameterfile']
        self.classifiermethods = ast.literal_eval(config['Classification']['classifiermethods'])
        self.balances = ast.literal_eval(config['Classification']['balances'])
        self.weightmethods = ast.literal_eval(config['Classification']['weightmethods'])
        self.featuretypes = ast.literal_eval(config['Features']['featuretypes'])
        self.ngramsizes = ast.literal_eval(config['Features']['ngramsizes'])
        self.minimumtokenfrequencies = ast.literal_eval(config['Features']['minimumtokenfrequencies'])
        self.prunenumbers = ast.literal_eval(config['Classification']['prunenumbers'])
        self.targets = ast.literal_eval(config['Classification']['targets'])
        self.module_featurize=config['Features']['module_featurize']
        self.frogconfig=config['Features']['frogconfig']
        self.module_validate=config['Classification']['module_validate']
        self.classifier_args=config['Classification']['classifier_args']
        
        inputfilebasename = os.path.basename(self.inputfile)
        inputfilebasenamenoext = os.path.splitext(inputfilebasename)[0]
        for featuretype in self. featuretypes:
            for ngramsize in self.ngramsizes:
                for minimumtokenfrequency in self.minimumtokenfrequencies:
                    outputdir_featurize = os.path.join(self.startoutputdir,inputfilebasenamenoext,featuretype,ngramsize,str(minimumtokenfrequency))
                    for classifiermethod in self.classifiermethods:
                        for balance in self.balances:
                            baldir = 'notbalanced'
                            if balance:
                                baldir = 'balanced'
                            for weightmethod in self.weightmethods:
                                for prunenumber in self.prunenumbers:
                                    outputdir_validate = os.path.join(outputdir_featurize,classifiermethod,baldir,weightmethod,str(prunenumber))
                                    self.parametercombinations.append((outputdir_featurize,outputdir_validate,featuretype,str(ngramsize),str(minimumtokenfrequency),classifiermethod,balance,baldir,weightmethod,str(prunenumber)))

    def featurize(self):
        for (outputdir_featurize,outputdir_validate,featuretype,ngramsize,minimumtokenfrequency,classifiermethod,balance,baldir,weightmethod,prunenumber) in self.parametercombinations:
            if not os.path.exists(outputdir_validate):
                os.makedirs(outputdir_validate)
                                    
            classification = Classification(self.inputfile, self.labelfile, module_featurize=self.module_featurize, ngrams=ngramsize, minimum_token_frequency=minimumtokenfrequency, featuretypes=featuretype, frogconfig=self.frogconfig, module_validate=self.module_validate, classifier_args=self.classifier_args, classifier=classifiermethod, balance=balance, weight=weightmethod, prune=prunenumber)
            if not os.path.isfile(classification.features):
                classification.Featurize(outputdir_featurize)

    def validate(self):
        for (outputdir_featurize,outputdir_validate,featuretype,ngramsize,minimumtokenfrequency,classifiermethod,balance,baldir,weightmethod,prunenumber) in self.parametercombinations:
            if not os.path.exists(outputdir_validate):
                os.makedirs(outputdir_validate)
                                    
            classification = Classification(self.inputfile, self.labelfile, module_featurize=self.module_featurize, ngrams=ngramsize, minimum_token_frequency=minimumtokenfrequency, featuretypes=featuretype, frogconfig=self.frogconfig, module_validate=self.module_validate, classifier_args=self.classifier_args, classifier=classifiermethod, balance=balance, weight=weightmethod, prune=prunenumber)
            if not os.path.isfile(classification.features):
                print("Features missing!")
                exit(1)
            classification.Validate(outputdir_validate,outputdir_featurize)

    def readperformances(self):
        ngramsizeseen = {}
        for (outpudir_featurize,outputdir_validate,featuretype,ngramsize,minimumtokenfrequency,classifiermethod,balance,baldir,weightmethod,prunenumber) in self.parametercombinations:
            performancefiles = glob.glob(outputdir_validate+'/**/performance.csv',recursive=True)
            for performancefile in performancefiles:
                performancefiledir = os.path.dirname(performancefile)
                if not performancefiledir.find('fold') > 0:
                    if not ngramsize in ngramsizeseen:
                        ngramsizeseen[ngramsize] = True
                        print(datetime.datetime.now(),ngramsize)
                    confusionmatrixfile = performancefiledir + '/confusion_matrix.csv'
                    performance = ClassificationPerformance(featuretype,ngramsize,minimumtokenfrequency,classifiermethod,baldir,weightmethod,prunenumber)
                    performance.read(confusionmatrixfile,performancefile)
                    self.performances.append(performance) 

    def writeperformances(self):
        performanceoutputfile = open(self.performanceoutputfilename,'w')
        for performance in self.performances:
            performance.write(performanceoutputfile)
        performanceoutputfile.close()

    def writeperformanceperparameter(self):
        nrcombinations = 0
        sumfscore = {}
        sumfscore['featuretype'] = {}
        sumfscore['ngramsize'] = {}
        sumfscore['minimumtokenfrequency'] = {}
        sumfscore['classifiermethod'] = {}
        sumfscore['balance'] = {}
        sumfscore['weightmethod'] = {}
        sumfscore['prunenumber'] = {}
        minfscore = {}
        minfscore['featuretype'] = {}
        minfscore['ngramsize'] = {}
        minfscore['minimumtokenfrequency'] = {}
        minfscore['classifiermethod'] = {}
        minfscore['balance'] = {}
        minfscore['weightmethod'] = {}
        minfscore['prunenumber'] = {}
        maxfscore = {}
        maxfscore['featuretype'] = {}
        maxfscore['ngramsize'] = {}
        maxfscore['minimumtokenfrequency'] = {}
        maxfscore['classifiermethod'] = {}
        maxfscore['balance'] = {}
        maxfscore['weightmethod'] = {}
        maxfscore['prunenumber'] = {}
        for performance in self.performances:
            nrcombinations += 1
            if performance.featuretype not in sumfscore['featuretype']:
                sumfscore['featuretype'][performance.featuretype] = 0
                minfscore['featuretype'][performance.featuretype] = 101
                maxfscore['featuretype'][performance.featuretype] = 0
            sumfscore['featuretype'][performance.featuretype] += performance.meanfscore
            if performance.meanfscore < float(minfscore['featuretype'][performance.featuretype]):
                minfscore['featuretype'][performance.featuretype] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['featuretype'][performance.featuretype]):
                maxfscore['featuretype'][performance.featuretype] = "%.2f" % (performance.meanfscore)
            if performance.ngramsize not in sumfscore['ngramsize']:
                sumfscore['ngramsize'][performance.ngramsize] = 0
                minfscore['ngramsize'][performance.ngramsize] = 101
                maxfscore['ngramsize'][performance.ngramsize] = 0
            sumfscore['ngramsize'][performance.ngramsize] += performance.meanfscore
            if performance.meanfscore < float(minfscore['ngramsize'][performance.ngramsize]):
                minfscore['ngramsize'][performance.ngramsize] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['ngramsize'][performance.ngramsize]):
                maxfscore['ngramsize'][performance.ngramsize] = "%.2f" % (performance.meanfscore)

            if performance.minimumtokenfrequency not in sumfscore['minimumtokenfrequency']:
                sumfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] = 0
                minfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] = 101
                maxfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] = 0
            sumfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] += performance.meanfscore
            if performance.meanfscore < float(minfscore['minimumtokenfrequency'][performance.minimumtokenfrequency]):
                minfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['minimumtokenfrequency'][performance.minimumtokenfrequency]):
                maxfscore['minimumtokenfrequency'][performance.minimumtokenfrequency] = "%.2f" % (performance.meanfscore)
            if performance.classifiermethod not in sumfscore['classifiermethod']:
                sumfscore['classifiermethod'][performance.classifiermethod] = 0
                minfscore['classifiermethod'][performance.classifiermethod] = 101
                maxfscore['classifiermethod'][performance.classifiermethod] = 0
            sumfscore['classifiermethod'][performance.classifiermethod] += performance.meanfscore
            if performance.meanfscore < float(minfscore['classifiermethod'][performance.classifiermethod]):
                minfscore['classifiermethod'][performance.classifiermethod] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['classifiermethod'][performance.classifiermethod]):
                maxfscore['classifiermethod'][performance.classifiermethod] = "%.2f" % (performance.meanfscore)
            if performance.baldir not in sumfscore['balance']:
                sumfscore['balance'][performance.baldir] = 0
                minfscore['balance'][performance.baldir] = 101
                maxfscore['balance'][performance.baldir] = 0
            sumfscore['balance'][performance.baldir] += performance.meanfscore
            if performance.meanfscore < float(minfscore['balance'][performance.baldir]):
                minfscore['balance'][performance.baldir] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['balance'][performance.baldir]):
                maxfscore['balance'][performance.baldir] = "%.2f" % (performance.meanfscore)
            if performance.weightmethod not in sumfscore['weightmethod']:
                sumfscore['weightmethod'][performance.weightmethod] = 0
                minfscore['weightmethod'][performance.weightmethod] = 101
                maxfscore['weightmethod'][performance.weightmethod] = 0
            sumfscore['weightmethod'][performance.weightmethod] += performance.meanfscore
            if performance.meanfscore < float(minfscore['weightmethod'][performance.weightmethod]):
                minfscore['weightmethod'][performance.weightmethod] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['weightmethod'][performance.weightmethod]):
                maxfscore['weightmethod'][performance.weightmethod] = "%.2f" % (performance.meanfscore)
            if performance.prunenumber not in sumfscore['prunenumber']:
                sumfscore['prunenumber'][performance.prunenumber] = 0
                minfscore['prunenumber'][performance.prunenumber] = 101
                maxfscore['prunenumber'][performance.prunenumber] = 0
            sumfscore['prunenumber'][performance.prunenumber] += performance.meanfscore
            if performance.meanfscore < float(minfscore['prunenumber'][performance.prunenumber]):
                minfscore['prunenumber'][performance.prunenumber] = "%.2f" % (performance.meanfscore)
            if performance.meanfscore > float(maxfscore['prunenumber'][performance.prunenumber]):
                maxfscore['prunenumber'][performance.prunenumber] = "%.2f" % (performance.meanfscore)
        meanfscore = {}
        meanfscore['featuretype'] = {}
        meanfscore['ngramsize'] = {}
        meanfscore['minimumtokenfrequency'] = {}
        meanfscore['classifiermethod'] = {}
        meanfscore['balance'] = {}
        meanfscore['weightmethod'] = {}
        meanfscore['prunenumber'] = {}
        performanceperparameteroutputfile = open(self.performanceperparameteroutputfilename,'w')
        performanceperparameteroutputfile.write('fscores per parameter (mean (min, max)):\n\n')
        performanceperparameteroutputfile.write('featuretype:\n')
        for featuretype in self.featuretypes:
            meanfscore['featuretype'][featuretype] = "%.2f" % (sumfscore['featuretype'][featuretype] / (nrcombinations / len(self.featuretypes)))
            performanceperparameteroutputfile.write(featuretype+': '+str(meanfscore['featuretype'][featuretype])+' ('+str(minfscore['featuretype'][featuretype])+', '+str(maxfscore['featuretype'][featuretype])+')\n')
        performanceperparameteroutputfile.write('\nngramsize:\n')
        for ngramsize in self.ngramsizes:
            meanfscore['ngramsize'][ngramsize] = "%.2f" % (sumfscore['ngramsize'][str(ngramsize)] / (nrcombinations / len(self.ngramsizes)))
            performanceperparameteroutputfile.write(str(ngramsize)+': '+str(meanfscore['ngramsize'][ngramsize])+' ('+str(minfscore['ngramsize'][str(ngramsize)])+', '+str(maxfscore['ngramsize'][str(ngramsize)])+')\n')
        performanceperparameteroutputfile.write('\nminimumtokenfrequency:\n')
        for minimumtokenfrequency in self.minimumtokenfrequencies:
            meanfscore['minimumtokenfrequency'][minimumtokenfrequency] = "%.2f" % (sumfscore['minimumtokenfrequency'][str(minimumtokenfrequency)] / (nrcombinations / len(self.minimumtokenfrequencies)))
            performanceperparameteroutputfile.write(str(minimumtokenfrequency)+': '+str(meanfscore['minimumtokenfrequency'][minimumtokenfrequency])+' ('+str(minfscore['minimumtokenfrequency'][str(minimumtokenfrequency)])+', '+str(maxfscore['minimumtokenfrequency'][str(minimumtokenfrequency)])+')\n')
        performanceperparameteroutputfile.write('\nclassifiermethod:\n')
        for classifiermethod in self.classifiermethods:
            meanfscore['classifiermethod'][classifiermethod] = "%.2f" % (sumfscore['classifiermethod'][classifiermethod] / (nrcombinations / len(self.classifiermethods)))
            performanceperparameteroutputfile.write(classifiermethod+': '+str(meanfscore['classifiermethod'][classifiermethod])+' ('+str(minfscore['classifiermethod'][classifiermethod])+', '+str(maxfscore['classifiermethod'][classifiermethod])+')\n')
        performanceperparameteroutputfile.write('\nbalance:\n')
        for balancebool in self.balances:
            balance = 'notbalanced'
            if balancebool:
                balance = 'balanced'
            meanfscore['balance'][balance] = "%.2f" % (sumfscore['balance'][balance] / (nrcombinations / len(self.balances)))
            performanceperparameteroutputfile.write(balance+': '+str(meanfscore['balance'][balance])+' ('+str(minfscore['balance'][balance])+', '+str(maxfscore['balance'][balance])+')\n')
        performanceperparameteroutputfile.write('\nweightmethod:\n')
        for weightmethod in self.weightmethods:
            meanfscore['weightmethod'][weightmethod] = "%.2f" % (sumfscore['weightmethod'][weightmethod] / (nrcombinations / len(self.weightmethods)))
            performanceperparameteroutputfile.write(weightmethod+': '+str(meanfscore['weightmethod'][weightmethod])+' ('+str(minfscore['weightmethod'][weightmethod])+', '+str(maxfscore['weightmethod'][weightmethod])+')\n')
        performanceperparameteroutputfile.write('\nprunenumber:\n')
        for prunenumber in self.prunenumbers:
            meanfscore['prunenumber'][prunenumber] = "%.2f" % (sumfscore['prunenumber'][str(prunenumber)] / (nrcombinations / len(self.prunenumbers)))
            performanceperparameteroutputfile.write(str(prunenumber)+': '+str(meanfscore['prunenumber'][prunenumber])+' ('+str(minfscore['prunenumber'][str(prunenumber)])+', '+str(maxfscore['prunenumber'][str(prunenumber)])+')\n')
        performanceperparameteroutputfile.close()
        
    def sortperformances(self):
        for performancenr1 in range(0,len(self.performances)-1):
            for performancenr2 in range(performancenr1,len(self.performances)):
                if self.performances[performancenr2].meanfscore > self.performances[performancenr1].meanfscore:
                    temp = self.performances[performancenr2]
                    self.performances[performancenr2] = self.performances[performancenr1]
                    self.performances[performancenr1] = temp
        
class ClassificationPerformance:
    def __init__(self,featuretype,ngramsize,minimumtokenfrequency,classifiermethod,baldir,weightmethod,prunenumber):
        self.featuretype = featuretype
        self.ngramsize = ngramsize
        self.minimumtokenfrequency = minimumtokenfrequency
        self.classifiermethod = classifiermethod
        self.baldir = baldir
        self.weightmethod = weightmethod
        self.prunenumber = prunenumber
        self.targets = []
        self.confusions = {}
        self.precisions = {}
        self.recalls = {}
        self.fscores = {}
        self.aucs = {}
        self.clfs = {}
        self.cors = {}
        self.meanfscore=0
        
    def read(self,confusionmatrix,performancefile):
        conf = open(confusionmatrix)
        targetline = False
        confusionline = False
        for line in conf:
            line = line.rstrip()
            if targetline:
                self.targets = re.findall('([^\s]+)',line)
                targetline = False
                confusionline = True
            elif confusionline:
                confusionparts = re.findall('([^\s]+)',line)
                self.confusions[confusionparts[0]] = confusionparts[1:]

            emptymatch = re.search('^$',line)
            if emptymatch:
                targetline = True
                
        conf.close()
        perf = open(performancefile)
        nolines = 0
        fscoresum = 0
        for line in perf:
            line = line.rstrip()
            fields = line.split(',')
            if fields[0] in self.targets:
                self.precisions[fields[0]] = fields[1]
                self.recalls[fields[0]] = fields[2]
                self.fscores[fields[0]] = fields[3]
                fscoresum += float(fields[3])
                nolines += 1
                self.aucs[fields[0]] = fields[6]
                self.clfs[fields[0]] = fields[8]
                self.cors[fields[0]] = fields[9]

        if nolines > 0:
            self.meanfscore = fscoresum/nolines
        perf.close()

    def write(self,outputfile):
        targetwidth = len(max(self.targets,key=len))+2
        precisionwidth = len('precision') + 2
        recallwidth = len('recall') + 2
        fscorewidth = len('fscore') + 2
        aucwidth = len('auc') + 3
        
        outputfile.write('= = = = = = = = = = = = = = =\n')
        outputfile.write('featuretype='+self.featuretype+', ngramsize='+self.ngramsize+', minimumtokenfrequency='+self.minimumtokenfrequency+', classifiermethod='+self.classifiermethod+', balance='+self.baldir+', weightmethod='+self.weightmethod+', prunenumber='+self.prunenumber)
        outputfile.write('\n\n')
        outputfile.write('{0:{align}{width}}'.format('',width=targetwidth,align='>'))
        for target in self.targets:
            outputfile.write('{0:{align}{width}}'.format(target,width=len(target)+2,align='>'))
        outputfile.write('{0:{align}{width}}'.format('precision',width=precisionwidth,align='>'))
        outputfile.write('{0:{align}{width}}'.format('recall',width=recallwidth,align='>'))
        outputfile.write('{0:{align}{width}}'.format('fscore',width=fscorewidth,align='>'))
        outputfile.write('{0:{align}{width}}'.format('auc',width=aucwidth,align='>'))
        outputfile.write('\n')
        for target in self.targets:
            outputfile.write('{0:{align}{width}}'.format(target,width=targetwidth,align='<'))
            for target2 in self.targets:
                outputfile.write('{0:{align}{width}}'.format(self.confusions[target][self.targets.index(target2)],width=len(target2)+2,align='>'))
            outputfile.write('{0:{align}{width}}'.format(self.precisions[target],width=precisionwidth,align='>'))
            outputfile.write('{0:{align}{width}}'.format(self.recalls[target],width=recallwidth,align='>'))
            outputfile.write('{0:{align}{width}}'.format(self.fscores[target],width=fscorewidth,align='>'))
            outputfile.write('{0:{align}{width}}'.format(self.aucs[target],width=aucwidth,align='>'))
            outputfile.write('\n')
