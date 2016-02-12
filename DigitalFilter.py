
#Digital Filter

def select_nth(n, data):
    pivot = data[0]
    less = [datium for datium in data if datium < pivot]
    if len(less) > n:
        return select_nth(n, less)
    n -= len(less)
        
    equal = data.count(pivot)
    if equal > n:
        return pivot
    n -= equal
        
    great = [datium for datium in data if datium > pivot]
    return select_nth(n, great)

def findMedian(aList):
    if len(aList) % 2 == 1:
        #odd
        return select_nth(len(aList)/2, aList)
    else:
        #even
        return (select_nth(len(aList)/2, aList)+select_nth(len(aList)/2-1, aList))/2.0
    
def processFilter(originalSignals):
    return findMedian(originalSignals)
