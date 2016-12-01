# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab

from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.

        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        if drug in self.resistances:
            return self.resistances[drug]

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        if len(activeDrugs) == 0:
            prob = self.maxBirthProb * (1 - popDensity)
            r = random.random()
            if (r <= prob):
                newRes = {}
                for key, res in self.resistances.iteritems():
                    inherit = 1 - self.mutProb
                    mutChance = random.random()
                    if mutChance <= inherit:
                        newRes[key] = self.resistances[key]
                    elif mutChance > inherit:
                        newRes[key] = not self.resistances[key]
                return ResistantVirus(self.maxBirthProb,self.clearProb, newRes, self.mutProb)
            raise NoChildException
        else:
            for drug in activeDrugs:
                if self.resistances[drug] and self.resistances[drug] is True:
                    prob = self.maxBirthProb * (1 - popDensity)
                    r = random.random()
                    if (r <= prob):
                        newRes = {}
                        for key, res in self.resistances.iteritems():
                            inherit = 1 - self.mutProb
                            mutChance = random.random()
                            if mutChance <= inherit:
                                newRes[key] = self.resistances[key]
                            elif mutChance > inherit:
                                newRes[key] = not self.resistances[key]
                        return ResistantVirus(self.maxBirthProb,self.clearProb, newRes, self.mutProb)
                    raise NoChildException
            raise NoChildException


#v = ResistantVirus(0.1, 0.05, {'test': True, 'test2': False}, 0.5)
#print v.isResistantTo('test')
#nv = v.reproduce(0.1, ['test'])
#print nv.isResistantTo('test')
#raise SystemExit(0)

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
#        pop = 0
#        for v in self.viruses:
#            res = True
#            for drug in drugResist:
#                if v.isResistantTo(drug) is False:
#                    res = False
#            if res is True:
#                pop += 1
#
#        return pop
        # TODO
        pop = 0
        for v in self.viruses:
            res = True
            for drug in drugResist:
                if drug in v.resistances:
                    if v.resistances[drug] is False:
                        res = False
                        break
                else:
                    res = False
                    break
            if res is True:
                pop += 1
        return pop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        nv, clear_count, create_count, not_repo = list(self.viruses), 0, 0, 0
        for virus in self.viruses:
            if (virus.doesClear() == True): #virus is cleared
                nv.remove(virus)
                clear_count += 1
            else:
                try:
                    nv.append(virus.reproduce(float(len(self.viruses)) / float(self.maxPop),self.drugs))
                    create_count += 1
                except NoChildException:
                    not_repo += 1
        self.viruses = nv
        return self.getTotalPop()

#p = Patient([ResistantVirus(0.1, 0.05, {'test': False, 'test2': True}, 0.5),ResistantVirus(0.1, 0.05, {'test': True, 'test2': False}, 0.5),ResistantVirus(0.1, 0.05, {'test': True, 'test2': False}, 0.5),ResistantVirus(0.1, 0.05, {'test': False, 'test2': False}, 0.5),ResistantVirus(0.1, 0.05, {'test': True, 'test2': True}, 0.5)], 1000)
#print p.getTotalPop()
#print p.getResistPop(['test2'])
#p.addPrescription('test')
#print p.update()
#raise SystemExit(0)

#
# PROBLEM 2
#

def simulationWithDrug():
    viruses = []
    count = 0
    trials = 10
    totalPopAvg = []
    resPopAvg = []
    stepAvg = []
    while len(viruses) < 100:
        viruses.append(ResistantVirus(0.1,0.05,{'guttagonol':False},0.005))
    patient = Patient(viruses,1000)
    while (count < trials):
        count += 1
        attempt = treatmentProcess(0,150,150,viruses,patient,{'guttagonol': 150})
        totalPopAvg.append(attempt['totalPop'])
        resPopAvg.append(attempt['resistancePop'])
        stepAvg.append(attempt['totalSteps'])
    pylab.plot(stepAvg, totalPopAvg, 'b-', label='population growth over time')
    pylab.plot(stepAvg, resPopAvg, 'r-', label='resistant population growth over time')
    pylab.xlabel('trial')
    pylab.ylabel('population growth')
    pylab.title('population growth (with drugs)')
    pylab.show()


#
# PROBLEM 3
#
def simulationDelayedTreatment():
    fig = pylab.figure()
    subplot = 1
    trials = 10
    timeStepsList = [300,150,75,0]
    for timeStep in timeStepsList:
        totalVir = []
        count = 0
        ax = fig.add_subplot(2,2,subplot)
        while (count < trials):
            count += 1
            viruses = []
            while len(viruses) < 100:
                viruses.append(ResistantVirus(0.1,0.05,{'guttagonol':False},0.005))
            patient = Patient(viruses,1000)
            attempt = treatmentProcess(0,timeStep,150,viruses,patient,{'guttagonol': 150})
            totalVir.extend(attempt['totalPop'])
        ax.hist(totalVir, bins=20)
        subplot += 1
    pylab.show()


#
# PROBLEM 4
#
def simulationTwoDrugsDelayedTreatment():
    fig = pylab.figure()
    subplot = 1
    trials = 10
    timeStepsList = [300,150,75,0]
    for timeStep in timeStepsList:
        totalVir = []
        count = 0
        ax = fig.add_subplot(2,2,subplot)
        while (count < trials):
            count += 1
            viruses = []
            while len(viruses) < 100:
                viruses.append(ResistantVirus(0.1,0.05,{'guttagonol':False, 'grimpex':False},0.005))
            patient = Patient(viruses,1000)
            attempt = treatmentProcess(150,timeStep,150,viruses,patient,{'guttagonol': 150, 'grimpex': 150 + timeStep})
            totalVir.extend(attempt['totalPop'])
        ax.hist(totalVir, bins=20)
        subplot += 1
    pylab.show()


#
# PROBLEM 5
#
def simulationTwoDrugsVirusPopulations():
    viruses = []
    count = 0
    trials = 10
    totalPopAvg = []
    resPopAvg = []
    resPop2Avg = []
    resPopTotalAvg = []
    stepAvg = []
    while len(viruses) < 100:
        viruses.append(ResistantVirus(0.1,0.05,{'guttagonol':False,'grimpex':False},0.005))
    #patient = Patient(viruses,1000)
    while (count < trials):
        patient = Patient(viruses,5000)
        count += 1
        attempt = treatmentProcess(150,0,150,viruses,patient,{'guttagonol': 150,'grimpex': 450})
        totalPopAvg.append(attempt['totalPop'])
        resPopAvg.append(attempt['resistancePop'])
        resPop2Avg.append(attempt['resistancePop2'])
        resPopTotalAvg.append(attempt['resistancePopTotal'])
        stepAvg.append(attempt['totalSteps'])
    pylab.plot(numpy.mean(numpy.array(stepAvg), axis=0), numpy.mean(numpy.array(totalPopAvg), axis=0), 'b.')
    pylab.plot(numpy.mean(numpy.array(stepAvg), axis=0), numpy.mean(numpy.array(resPopAvg), axis=0), 'r.')
    pylab.plot(numpy.mean(numpy.array(stepAvg), axis=0), numpy.mean(numpy.array(resPop2Avg), axis=0), 'g.')
    pylab.plot(numpy.mean(numpy.array(stepAvg), axis=0), numpy.mean(numpy.array(resPopTotalAvg), axis=0), 'y.')
    pylab.xlabel('timestep')
    pylab.ylabel('population average at timestep')
    pylab.title('population growth (with drugs)')
    pylab.show()

def treatmentProcess(beforeStep,timeStep,afterStep,viruses,patient,drugs):
    timeSteps = beforeStep + timeStep + afterStep
    cur_step = 0
    pop = []
    resPop = []
    resPop2 = []
    resPopTotal = []
    x = []

    while cur_step < timeSteps:
        if cur_step == 150:
            print '1st step'
            patient.addPrescription('guttagonol')

        if cur_step == 150:
            print '2nd step'
            patient.addPrescription('grimpex')
#        if len(drugs) is 1:
#            if cur_step is timeStep:
#                    patient.addPrescription(drugs.keys()[0])
#        else:
#            for k,v in drugs.iteritems():
#                if cur_step is v:
#                    patient.addPrescription(k)
        p = patient.update()
        cur_step += 1
        x.append(cur_step)
        pop.append(p)
        resPop.append(patient.getResistPop(['guttagonol']))
        resPop2.append(patient.getResistPop(['grimpex']))
        resPopTotal.append(patient.getResistPop(['grimpex', 'guttagonol']))
    return {'totalPop': pop, 'resistancePop': resPop, 'resistancePop2': resPop2, 'resistancePopTotal': resPopTotal, 'totalSteps': x}


simulationTwoDrugsVirusPopulations()
