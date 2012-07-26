import csv
import sys

class ParetoAnalyzer:
    def __init__(self, csvFileName):
        dataRows = self.get_data_from_csv(csvFileName)
        self.calculate_percentiles(dataRows)


    def get_data_from_csv(self, filename):
        reader = csv.reader(open(filename, 'rb'), delimiter=',' , quotechar = '"')
        
        idDict = {}
        
        try:
            for row in reader:
                curRow = (str(row[0]),float(row[1]))
                if(curRow[0] not in idDict):
                    idDict[curRow[0]] = curRow[1]
                else:
                    idDict[curRow[0]] += curRow[1]
        
            sortedItems = sorted(idDict.items(), key = lambda x: x[1])
            return sortedItems            

        except IOError as e:
            print e


    def calculate_percentiles(self, sortedData):
        numItems = len(sortedData)

        #set totalUsers here
        self.totalUsers = numItems

        self.cdf = [0]

        curUserGroup = []
        self.userGroups = [[]]

        nextPercentile = 1
        currentCDF = 0

        for i in range(0, len(sortedData)):
            currentCDF += sortedData[i][1]
            curUserGroup.append(sortedData[i])
            if((i+1)*100/len(sortedData) == nextPercentile):
                self.cdf.append(currentCDF)
                self.userGroups.append(curUserGroup)
                curUserGroup = []
                nextPercentile += 1

        
    def get_range_info(self, lo, hi):
        if(hi < lo):
            raise Exception("Lo must not excede Hi.")
        if(hi > 100 or lo < 0):
            raise Exception("Out of bounds in range parameters.")

        rangeRev = self.cdf[hi] - self.cdf[lo]
        rangeRevPercent = rangeRev/self.cdf[100]
        
        rangeUserCounts = map(lambda x: len(x) , self.userGroups[lo: hi+1])
        rangeUserTotal = reduce(lambda a,b: a+b, rangeUserCounts)
        rangeUserPercent = float(rangeUserTotal)/self.totalUsers

        #return a dict of this stuff
        return {'revPercent' : rangeRevPercent*100,
                'revTotal' : rangeRev,
                'idPercent' : rangeUserPercent*100,
                'idTotal' : rangeUserTotal }

        
    def get_items_in_range(self, lo, hi):
        if(hi < lo):
            raise Exception("Lo must not excede Hi.")
        if(hi > 100 or lo < 0):
            raise Exception("Out of bounds in range parameters.")

        itemRange = self.userGroups[lo: hi+1]
        fullList = reduce(lambda a,b: a+b, itemRange)
        return fullList

    def save_range(self, lo, hi):
        fileName = str(lo)+'_'+str(hi)+".csv"
        fileOut = open(fileName, 'w')

        fileOut.write("ID, Value\n")
        items = self.get_items_in_range(lo, hi)
        for i in items:
            val = "%.2f" %i[1]
            fileOut.write(str(i[0])+", "+val+"\n")
        fileOut.close()
        return fileName

