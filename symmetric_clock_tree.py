import random
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


class Sink:
    def __init__(self, x, y):
        self.location = [x, y]

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def setCentroid(centroid_x, centroid_y):
        self.centroid_location = [centroid_x, centroid_y]

class Centroid:
    def __init__(self, x, y):
        self.location = [x, y]
        # self.num_sinks = n

    def set_number_of_sinks(self, n):
        self.num_sinks = n

class SymmetricClockTree:
    def __init__(self, num_sinks, num_levels):
        # Can't handle multiple levels just yet.
        self.num_levels = num_levels
        self.num_sinks = num_sinks
        self.sinks = []
        self.centroids = []
        self.sinkGroups = {}
        self.minXCoordinate = 0
        self.maxXCoordinate = 2500
        self.minYCoordinate = 0
        self.maxYCoordinate = 2500

    def addCentroid(self, centroid, i):
        self.centroids.append(centroid)

    def createSinkGroup(self, centroid, i):
        sinkGroupDict = {
            "centroid_location": [centroid.location[0], centroid.location[1]],
            "sinks": []
        }

        self.sinkGroups[i] = sinkGroupDict

    def addSinksToGroups(self, group_ids):
        for i, group_id in enumerate(group_ids):
            self.sinkGroups[group_id]["sinks"].append(self.sinks[i])

        pprint(self.sinkGroups)

    def groupSinks(self):
        sinks = self.getSinkLocations()
        kmeans = KMeans(n_clusters=4).fit(sinks)
        centroids = kmeans.cluster_centers_

        for i, location in enumerate(centroids):
            centroid = Centroid(location[0], location[1])
            self.addCentroid(centroid, i)
            self.createSinkGroup(centroid, i)

        self.addSinksToGroups(kmeans.labels_)

    def findAllFactors(self):
        n = self.num_sinks
        return sorted(set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

    def getSinkLocations(self):
        locations = []
        for sink in self.sinks:
            locations.append(sink.location)
        return locations

    def makePlot(self):
        self.plotSinks()
        self.plotCentroids()
        self.setAxis()
        self.showPlot()

    def plotSinks(self):
        for sink in self.sinks:
            plt.plot(sink.location[0], sink.location[1], 'ro')

    def setAxis(self):
        plt.axis([self.minXCoordinate, self.maxXCoordinate, self.minYCoordinate, self.maxYCoordinate])


    def showPlot(self):
        plt.show()

    def plotCentroids(self):
        for centroid in self.centroids:
            plt.plot(centroid.location[0], centroid.location[1], 'go')


    def generateRandomSinkLocations(self):
        radius = 200
        rangeX = (self.minXCoordinate, self.maxXCoordinate)
        rangeY = (self.minYCoordinate, self.maxYCoordinate)
        qty = self.num_sinks  # or however many points you want

        # Generate a set of all points within 200 of the origin, to be used as offsets later
        # There's probably a more efficient way to do this.
        deltas = set()
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if x*x + y*y <= radius*radius:
                    deltas.add((x,y))

        excluded = set()
        i = 0
        while i<qty:
            x = random.randrange(*rangeX)
            y = random.randrange(*rangeY)
            if (x,y) in excluded: continue
            self.sinks.append(Sink(x, y))
            i += 1
            excluded.update((x+dx, y+dy) for (dx,dy) in deltas)


tree = SymmetricClockTree(10, 1)
tree.generateRandomSinkLocations()
tree.groupSinks()
#tree.makePlot()
