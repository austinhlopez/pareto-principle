import csv
import sys

class ParetoAnalyzer:
    def __init__(self, csvFileName):

        self.rows = self.get_data_from_csv(csvFileName)

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

            print sortedItems[::-1][:50]

        except IOError as e:
            print "BULLOCKS", e





testP = ParetoAnalyzer(sys.argv[1])

