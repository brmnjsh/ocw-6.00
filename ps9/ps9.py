# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    subjects = {}
    for line in inputFile:
        line = line.strip().split(',')
        subjects[line[0]] = (int(line[1]),int(line[2]))

    return subjects

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    if subInfo1[0] > subInfo2[0]:
        return True
    return False

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    if subInfo1[1] < subInfo2[1]:
        return True
    return False

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    if float(subInfo1[0]) / subInfo1[1] > float(subInfo2[0]) / subInfo2[1]:
        return True
    return False

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    newSubjects = {}
    currentWork = 0
    i = 0
    while i < len(subjects):
        for s in subjects:
            Found = False
            if subjects[s][1] + currentWork <= maxWork and s not in newSubjects:
                for s2 in subjects:
                    if subjects[s2][1] + currentWork <= maxWork and s2 not in newSubjects and s is not s2:
                        if comparator(subjects[s2],subjects[s]):
                            found = False
                            break
                        else:
                            found = True
                    else:
                        found = True
                if found == True:
                    currentWork = currentWork + subjects[s][1]
                    newSubjects[s] = subjects[s]
        if currentWork >= maxWork:
            i = len(subjects)
        else:
            i = i + 1
    return newSubjects

# s = loadSubjects(SHORT_SUBJECT_FILENAME)
# subjects = greedyAdvisor(s, 7, cmpValue)
# print subjects

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    return getBestCombos(bruteRecurse(subjects,{},maxWork,0,[]))

def bruteRecurse(subjects,newSubjects,maxWork,currentWork,combos):
    currentSubjects = dict(newSubjects)
    for s in subjects:
        if subjects[s][1] + currentWork < maxWork and s not in currentSubjects:
            currentSubjects[s] = subjects[s]
            combos.append(dict(currentSubjects))
            bruteRecurse(subjects,currentSubjects,maxWork,subjects[s][1] + currentWork,combos)
            del currentSubjects[s]
        elif subjects[s][1] + currentWork == maxWork and s not in currentSubjects:
            currentSubjects[s] = subjects[s]
            combos.append(dict(currentSubjects))
            del currentSubjects[s]
    return combos

def getBestCombos(combos):
    value = 0
    sCount = 0
    chosen = None
    for subjects in combos:
        lValue = 0
        lSCount = 0
        for subject in subjects:
            lValue = lValue + subjects[subject][0]
            lSCount = lSCount + 1
        if (lValue > value or (lSCount < sCount and lValue >= value)) or chosen == None:
            chosen = subjects
            value = lValue
            sCount = lSCount
    return chosen

# s = loadSubjects(SHORT_SUBJECT_FILENAME)
# #s = loadSubjects(SUBJECT_FILENAME)
# subjects = bruteForceAdvisor(s,7)
# print subjects
