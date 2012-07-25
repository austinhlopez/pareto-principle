import csv
import sys

class ParetoAnalyzer:
    def __init__(self, csvFileName):

        dataRows = self.get_data_from_csv(csvFileName)
        self.dataBuckets = self.get_percentiles(dataRows)


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
            print "BULLOCKS", e


    def get_percentiles(self, sortedData):
        numItems = len(sortedData)

        cdf = [0]

        curUserGroup = []
        userGroups = [[]]

        nextPercentile = 1
        currentCDF = 0

        for i in range(0, len(sortedData)):
            currentCDF += sortedData[i][1]
            curUserGroup.append(sortedData[i])
            if((i+1)*100/len(sortedData) == nextPercentile):
                cdf.append(currentCDF)
                userGroups.append(curUserGroup)
                curUserGroup = []
                nextPercentile += 1
        
#percent of users, portion of users, percent of rev., portion of rev


testP = ParetoAnalyzer(sys.argv[1])

