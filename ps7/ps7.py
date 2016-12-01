# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

        # TODO

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        r = random.random()
        if (r <= self.clearProb):
            return True
        return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        prob = self.maxBirthProb * (1 - popDensity)
        r = random.random()
        #print self.maxBirthProb, popDensity, prob, r
        #raise SystemExit(0)
        if (r <= prob):
            return SimpleVirus(self.maxBirthProb,self.clearProb)
        raise NoChildException

#v = SimpleVirus(0.5,0.5)
#print v.doesClear()
#print v.reproduce(0.5)


class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        nv = list(self.viruses)
        clear_count = 0
        create_count = 0
        not_repo = 0
        #print len(self.viruses)
        for virus in self.viruses:
            if (len(nv) < self.maxPop):
                if (virus.doesClear() == True): #virus is cleared
                    nv.remove(virus)
                    clear_count += 1
                else:
                    #print "create"
                    try:
                        #print len(nv), self.maxPop, float(len(nv)) / float(self.maxPop)
                        v = virus.reproduce(float(len(nv)) / float(self.maxPop))
                        nv.append(v)
                        create_count += 1
                    except NoChildException:
                        not_repo += 1 
            else:
                break
        self.viruses = nv
        #print create_count, clear_count, not_repo
        return self.getTotalPop()

#p = SimplePatient([SimpleVirus(0.5,0.5),SimpleVirus(0.5,0.5),SimpleVirus(0.5,0.5),SimpleVirus(0.5,0.5),SimpleVirus(0.5,0.5)], 1000)
#print p.getTotalPop()
#print p.update()
            
#
# PROBLEM 2
#
def simulationWithoutDrug():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    vir_count = 100
    time_steps = 300
    cur_step = 0
    viruses = []
    pop = []
    x = []
    
    while len(viruses) < vir_count:
        viruses.append(SimpleVirus(0.1,0.05))
        
    patient = SimplePatient(viruses,1000)
    
    while cur_step < time_steps:
        p = patient.update()
        cur_step += 1
        x.append(cur_step)
        pop.append(p)
    
#    pylab.plot(x,pop)
#    pylab.xlabel('time step')
#    pylab.ylabel('population')
#    pylab.title('population per time step')
#    pylab.show()
    return sum(pop) / float(len(pop))

avgs = []
trial = []
count = 0
while (len(avgs) <= 100):
    count += 1
    trial.append(count)
    avgs.append(simulationWithoutDrug())

pylab.plot(trial,avgs)
pylab.xlabel('trial')
pylab.ylabel('population average each trial')
pylab.title('population average per each trial')
pylab.show()
print len(avgs), avgs






















