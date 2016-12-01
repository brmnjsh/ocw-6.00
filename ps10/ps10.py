# Problem Set 10
# Name:
# Collaborators:
# Time:

#Code shared across examples
import pylab, random, string, copy, math

class Point(object):
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs
    def dimensionality(self):
        return len(self.attrs)
    def getAttrs(self):
        return self.attrs
    def getOriginalAttrs(self):
        return self.unNormalized
    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5
    def getName(self):
        return self.name
    def toStr(self):
        return self.name + str(self.attrs)
    def __str__(self):
        return self.name

class County(Point):
    weights = pylab.array([1.0] * 14)
    weights[2] = 0.0
    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
#        County.weights[2] = 1.0
#        print sum(County.weights * difference * difference) ** 0.5
#        raise Exception('done')
        return sum(County.weights * difference * difference) ** 0.5

class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()
    def getCentroid(self):
        return self.centroid
    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)))
        return meanPoint
    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0
    def getPoints(self):
        return self.points
    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False
    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]
    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]



def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points,k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        #print "Starting iteration " + str(numIters)
        newClusters = []
        for c in clusters:
            newClusters.append([])
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)
        biggestChange = 0.0
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print 'Iteration count =', numIters
    maxDist = 0.0
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    #print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    #print biggestChange
    return clusters, maxDist

#US Counties example
def readCountyData(fName, numEntries = 14):
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = pylab.array([0.0]*numEntries)
    
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            #print line
            continue
        dataLine = string.split(line)
        #print dataLine
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        #print maxVals[len(features)-1]
        #raise Exception('done')
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals

def buildCountyPoints(fName):
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = pylab.array(featureList[i])
        normalizedAttrs = originalAttrs/pylab.array(maxVals)
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))
#        print originalAttrs
#        print featureList[i]
#        print normalizedAttrs
#        print nameList[i]
#        print maxVals
#        raise Exception('done')
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).

    l: The list to split
    p: The probability that an element of l will be in the first partition

    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

def getAveIncome(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.

    cluster: the Cluster object to check

    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[1]

    return float(tot) / len(cluster.getPoints())

def getAvePoverty(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.

    cluster: the Cluster object to check

    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[2]

    return float(tot) / len(cluster.getPoints())


def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAveIncome(clusters[i]))

    pylab.hist(incomes)
    pylab.xlabel('Ave. Income')
    pylab.ylabel('Number of Clusters')
    pylab.show()


points = buildCountyPoints('counties.txt')
#random.seed(123)
testPoints = random.sample(points, len(points)/10)


def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values of k.
    For details see Problem 1.
    """
    # Your Code Here
    errors = []
    test_errors = []
    for k in kvals:
        sumPoints = []
        trainingPoints, holdoutPoints = randomPartition(points, .8)
        clusters, maxDist = kmeans(trainingPoints, k, cutoff, County)
        for c in clusters:
            meanPoint = c.getCentroid()
            ps = c.getPoints()
            for p in ps:
                #print "--------------cluster points----------------------"
                #print meanPoint.distance(p)
                sumPoints.append((p.distance(meanPoint))**2)
            #print "=================================cluster end================================="
        #print "/////////////////////////////////k end/////////////////////////////////"
        errors.append(sum(sumPoints))
        print sum(sumPoints)
        print("===============trainingdone===================holdout start===============")

        sumTestPoints = []
        for hp in holdoutPoints:
            smallestDistance = (hp.distance(clusters[0].getCentroid()))**2
            for c in clusters:
                if (hp.distance(c.getCentroid()))**2 < smallestDistance:
                    smallestDistance = (hp.distance(c.getCentroid()))**2
            sumTestPoints.append(smallestDistance)
        test_errors.append(sum(sumTestPoints))
        print sum(sumTestPoints)
        print("==================================end of k======================================")
    
    #print(errors)
    pylab.figure(1)

    pylab.subplot(211)
    pylab.plot(errors)
    pylab.plot(test_errors)
    pylab.xlabel('K')
    pylab.ylabel('Error')

    pylab.subplot(212)
    pylab.plot(errors,test_errors)
    pylab.xlabel('training set')
    pylab.ylabel('holdout set')

    pylab.show()

#graphRemovedErr(points)

def countyCheck(points, kvals = [50,50,50], cutoff = 0.1):
    for k in kvals:
        clusters, maxDist = kmeans(points, k, cutoff, County)
        for c in clusters:
            print c
        
    
#countyCheck(testPoints)

def graphPredictionErr(points, dimension, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """
    kpovavg = []
    for k in kvals:
        trainingPoints, holdoutPoints = randomPartition(points, .8)
        clusters, maxDist = kmeans(trainingPoints, k, cutoff, County)
        avgPoverty = []
        for hp in holdoutPoints:
            closestCluster = None
            closestDist = None
            for c in clusters:
                dist = hp.distance(c.getCentroid())
                if closestDist == None or dist < closestDist:
                    closestCluster = c
                    closestDist = dist
#            print closestCluster,closestDist
#            print getAvePoverty(closestCluster), hp.getOriginalAttrs()[2]
#            print (hp.getOriginalAttrs()[2] - getAvePoverty(closestCluster)) **2
            avgPoverty.append((hp.getOriginalAttrs()[2] - getAvePoverty(closestCluster))**2)
        kpovavg.append(sum(avgPoverty))
    #raise Exception('done')
    print kpovavg
    pylab.figure(1)
    pylab.plot(kvals,kpovavg)
    pylab.xlabel('K')
    pylab.ylabel('Error')
    pylab.show()
    
graphPredictionErr(points,2)        
            
            
