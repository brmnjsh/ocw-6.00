
def mergeSort(array):
    print array
    if len(array) > 1:
        mergeSort(array[:len(array)/2])
        mergeSort(array[len(array)/2:])
    else:
        print 'done'
    
    
array = [4,72,34,8,12]
mergeSort(array)