# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import sys
import ps6_visualize
import pylab

sys.setrecursionlimit(10000)
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        width: an integer > 0
        height: an integer > 0
        """
        self.width, self.height, self.tiles, w = width, height, {}, 0
        while (w < self.width):
            h = 0
            while (h < self.height):
                self.tiles[(w,h)] = 0
                h += 1
            w += 1

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.
        pos: a Position
        """
        self.tiles[(int(pos.getX()), int(pos.getY()))] = 1
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (self.tiles[(int(m), int(n))] == 1):
            return True
        return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return len(self.tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        returns: an integer
        """
        cleanTiles = 0
        for t in self.tiles:
            if (self.tiles[t] == 1):
                cleanTiles += 1
        return cleanTiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        returns: a Position object.
        """
        i = (random.uniform(0,self.width),random.uniform(0,self.height))
        pos = Position(i[0], i[1])
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if ((int(pos.getX()),int(pos.getY())) not in self.tiles.keys()):
            return False
        return True

#r = RectangularRoom(5,5)
#pos = Position(3.456,4.3)
#r.cleanTileAtPosition(pos)
#print r.isTileCleaned(pos.getX(),pos.getY())
#print r.getNumTiles()
#print r.getNumCleanedTiles()
#rpos = r.getRandomPosition()
#print rpos.getX(), rpos.getY()
#print r.isPositionInRoom(rpos)
#raise SystemExit(0)

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.
        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.uniform(0, 360)
        self.position = room.getRandomPosition()

    def getRobotPosition(self):
        """
        Return the position of the robot.
        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.
        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.
        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(self.position.getNewPosition(self.getRobotDirection(),self.speed))
        self.room.cleanTileAtPosition(self.getRobotPosition())
        

#room = RectangularRoom(5,5)
#robot = Robot(room, 2)
#robot_pos = robot.getRobotPosition()
#print robot_pos.getX(), robot_pos.getY()
#print robot.getRobotDirection()
#robot.updatePositionAndClean()
#robot_pos = robot.getRobotPosition()
#print robot_pos.getX(), robot_pos.getY()
#print room.isTileCleaned(robot_pos.getX(),robot_pos.getY())
#print room.tiles
#robot.setRobotPosition(Position(2,3))
#robot_pos = robot.getRobotPosition()
#print robot_pos.getX(), robot_pos.getY()
#robot.setRobotDirection(145.234)
#print robot.getRobotDirection()
#raise SystemExit(0)

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.position.getNewPosition(self.getRobotDirection(),self.speed)
        
        if ((pos.getX() < 0 or pos.getX() >= self.room.width) or (pos.getY() < 0 or pos.getY() >= self.room.height)):
            self.setRobotDirection(random.uniform(0, 360))
            self.updatePositionAndClean()
        else:
            self.setRobotPosition(pos)
            self.room.cleanTileAtPosition(self.getRobotPosition())

#room = RectangularRoom(5,5)
#robot = StandardRobot(room,2)
#pos = robot.getRobotPosition()
#print pos.getX(), pos.getY(), ' set pos'
#robot.updatePositionAndClean()
#pos = robot.getRobotPosition()
#print pos.getX(), pos.getY(), robot.getRobotDirection(), ' result pos'
#raise SystemExit(0)
        
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <facedfasdasdtttttttasdasdas= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    time_steps = []
    for i in range(num_trials): #trial count
        #anim = ps6_visualize.RobotVisualization(num_robots,width,height)
        anim = ''
        room = RectangularRoom(width,height)
        robots = createRobots(room,speed,robot_type,num_robots)
        time_steps.append(runRobots(robots,room,0,min_coverage,anim))
    return (num_robots, sum(time_steps) / len(time_steps))

def runRobots(robots,room,time_step_count,min_coverage,anim):
    tsc = time_step_count
    min_tiles = room.getNumTiles() * min_coverage
    while (room.getNumCleanedTiles() < min_tiles):
        for robot in robots:
            robot.updatePositionAndClean()
        tsc += 1
        #anim.update(room,robots)
    #anim.done()
    return tsc
#recursive solution
#    for robot in robots:
#        robot.updatePositionAndClean()
#    if (room.getNumCleanedTiles() < room.getNumTiles()): 
#        tsc += 1
#        runRobots(robots,room,tsc)
#    else:
#        #print room.getNumCleanedTiles(), room.getNumTiles()
#        #print room.tiles
#        print tsc
#        return tsc
    
def createRobots(room,speed,robot_type,num_robots):
    robots = []
    for i in range(num_robots):
        robots.append(robot_type(room,speed))
    return robots

#runSimulation(1,1,100,6,0.80,10,StandardRobot)
#runSimulation(1,1,6,100,0.80,10,StandardRobot)
#raise SystemExit(0)
    
# === Problem 4
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    robots = 10
    num_trials = []
    times = []
    for i in range(robots):
        trial = runSimulation(i + 1,1,20,20,0.80,10,StandardRobot)
        num_trials.append(trial[0])
        times.append(trial[1])
    pylab.plot(num_trials, times)
    pylab.xlabel('number of robots')
    pylab.ylabel('time to finish 80% of 20x20 room')
    pylab.title('time taken to complete 80% of 20x20 room with 1-10 robots')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    num_trials = []
    times = []
    area = ['20x20','25x16','40x10','50x8','80x5','100x4']
    
    trial = runSimulation(2,1,20,20,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    trial = runSimulation(2,1,25,16,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    trial = runSimulation(2,1,40,10,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    trial = runSimulation(2,1,50,8,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    trial = runSimulation(2,1,80,5,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    trial = runSimulation(2,1,100,4,0.80,10,StandardRobot)
    num_trials.append(trial[0])
    times.append(trial[1])
    
    x = [1,2,3,4,5,6]
    pylab.xticks(x,area)
    pylab.plot(x,times)
    pylab.show()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        pos = self.position.getNewPosition(self.getRobotDirection(),self.speed)
        self.setRobotDirection(random.uniform(0, 360))

        if ((pos.getX() < 0 or pos.getX() >= self.room.width) or (pos.getY() < 0 or pos.getY() >= self.room.height)):
            self.updatePositionAndClean()
        else:
            self.setRobotPosition(pos)
            self.room.cleanTileAtPosition(self.getRobotPosition())

       
        
# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    num_trials = []
    times = []
    
#    t1 = runSimulation(1,1,5,5,1,10,RandomWalkRobot) 
#    pylab.plot()
#    t2 = runSimulation(1,1,5,5,1,10,RandomWalkRobot) 
#    
#    pylab.xlabel('number of robots')
#    pylab.ylabel('time to finish 80% of 20x20 room')
#    pylab.title('comparison of efficieny between "standard" robot and "random walk" robot')
#    pylab.show()

#room = RectangularRoom(5,5)
#robot = StandardRobot(room,2)
#t = runSimulation(1,1,5,5,1,10,StandardRobot) 
#print t
#t = runSimulation(1,1,5,5,1,10,RandomWalkRobot) 
#print t
#showPlot1()   
#showPlot2()
raise SystemExit(0) 