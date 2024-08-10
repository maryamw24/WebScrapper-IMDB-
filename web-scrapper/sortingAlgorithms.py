import math
###################################################################################################################################################


def insertionSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    for i in range(start+1, end+1):
        key = movies[i]
        j = i - 1
        if isAscending:
            while j >= start and isLower(key, movies[j], attribute):
                movies[j+1] = movies[j]
                j -= 1
        else:
            while j >= start and isHigher(key, movies[j], attribute):
                movies[j+1] = movies[j]
                j -= 1
        movies[j+1] = key

###################################################################################################################################################


def bubbleSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    for i in range(start, end+1):
        for j in range(start, (start+end)-i):
            if isAscending:
                if isHigher(movies[j], movies[j+1], attribute):
                    movies[j], movies[j+1] = movies[j+1], movies[j]
            else:
                if isLower(movies[j], movies[j+1], attribute):
                    movies[j], movies[j+1] = movies[j+1], movies[j]

###################################################################################################################################################


def selectionSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    for i in range(start, end+1):
        key = i
        for j in range(i+1, end+1):
            if isAscending:
                if isLower(movies[j], movies[key], attribute):
                    key = j
            else:
                if isHigher(movies[j], movies[key], attribute):
                    key = j
        movies[key], movies[i] = movies[i], movies[key]

###################################################################################################################################################


def mergeSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    if start < end:
        mid = (start+end) // 2
        mergeSort(movies, attribute, isAscending, start, mid)
        mergeSort(movies, attribute, isAscending, mid+1, end)
        merge(movies, start, mid, end, attribute, isAscending)


def merge(movies: list, start: int, mid: int, end: int, attribute, isAscending: bool) -> None:
    left = movies[start:mid+1]
    right = movies[mid+1:end+1]
    idx, idx1, idx2 = start, 0, 0

    while idx1 < len(left) and idx2 < len(right):
        if isAscending:
            if isLower(left[idx1], right[idx2], attribute):
                movies[idx] = left[idx1]
                idx1 += 1
            else:
                movies[idx] = right[idx2]
                idx2 += 1
        else:
            if isHigher(left[idx1], right[idx2], attribute):
                movies[idx] = left[idx1]
                idx1 += 1
            else:
                movies[idx] = right[idx2]
                idx2 += 1
        idx += 1

    while idx1 < len(left):
        movies[idx] = left[idx1]
        idx += 1
        idx1 += 1

    while idx2 < len(right):
        movies[idx] = right[idx2]
        idx += 1
        idx2 += 1
###################################################################################################################################################


def partition(movies: list, start: int, end: int, attribute, isAscending: bool) -> None:
    pivot = movies[end]
    i = start-1
    for j in range(start, end):
        if (isAscending and isLower(movies[j], pivot, attribute)) or (not isAscending and isHigher(movies[j], pivot, attribute)):
            i += 1
            movies[i], movies[j] = movies[j], movies[i]
    i += 1
    movies[i], movies[end] = movies[end], movies[i]
    return i


def quickSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    if start < end:
        pivotIndex: int = partition(movies, start, end, attribute, isAscending)

        quickSort(movies, attribute, isAscending, start, pivotIndex-1,)
        quickSort(movies, attribute, isAscending, pivotIndex+1, end)

###################################################################################################################################################


def heapify(movies: list, size: int, index: int, attribute: str, isAscending: bool) -> None:
    largest = index
    leftChild = 2 * index + 1
    rightChild = 2 * index + 2

    if isAscending:
        if leftChild < size and isHigher(movies[leftChild], movies[largest], attribute):
            largest = leftChild
        if rightChild < size and isHigher(movies[rightChild], movies[largest], attribute):
            largest = rightChild
    else:
        if leftChild < size and isLower(movies[leftChild], movies[largest], attribute):
            largest = leftChild
        if rightChild < size and isLower(movies[rightChild], movies[largest], attribute):
            largest = rightChild

    if largest != index:
        movies[index], movies[largest] = movies[largest], movies[index]
        heapify(movies, size, largest, attribute, isAscending)


def heapSort(movies: list, attribute, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    size = end - start + 1

    for i in range(size // 2 - 1, -1, -1):
        heapify(movies, size, i, attribute, isAscending)

    for i in range(size - 1, 0, -1):
        movies[start], movies[start + i] = movies[start + i], movies[start]
        heapify(movies, i, 0, attribute, isAscending)

###################################################################################################################################################


def countSort(movies: list, attribute: list, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies)-1 if end == None else end
    minValue = min(getattr(movie, attribute[0])
                   for movie in movies[start:end+1])
    maxValue = max(getattr(movie, attribute[0])
                   for movie in movies[start:end+1])

    countArray = [0] * (maxValue - minValue + 1)
    outputArray = [None] * (end - start + 1)

    for movie in movies[start:end+1]:
        countArray[getattr(movie, attribute[0]) - minValue] += 1

    for i in range(1, len(countArray)):
        countArray[i] += countArray[i - 1]

    for i in range(end, start - 1, -1):
        movie = movies[i]
        index = getattr(movie, attribute[0]) - minValue
        outputArray[countArray[index] - 1] = movie
        countArray[index] -= 1

    for i in range(start, end + 1):
        movies[i] = outputArray[i - start]

    if not isAscending:
        movies[start:end+1] = movies[start:end+1][::-1]

###################################################################################################################################################


def countingSortRadix(movies: list, attribute: list, placeValue: int, start: int = 0, end: int = None) -> None:

    n = len(movies)
    output = [None] * n
    count = [0] * 10

    for i in range(start, end + 1):
        index = getattr(movies[i], attribute[0]) // placeValue
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = end
    while i >= start:
        index = getattr(movies[i], attribute[0]) // placeValue
        output[count[index % 10] - 1] = movies[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(start, end + 1):
        movies[i] = output[i - start]


def radixSort(movies: list, attribute: list, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies) - 1 if end is None else end
    maxValue = max(getattr(movie, attribute[0])
                   for movie in movies[start:end + 1])
    placeValue = 1
    while maxValue // placeValue > 0:
        countingSortRadix(movies, attribute, placeValue, start, end)
        placeValue *= 10

    if not isAscending:
        movies[start:end+1] = movies[start:end+1][::-1]

###################################################################################################################################################


def bucketSort(movies: list, attribute: list, isAscending: bool = True, start: int = 0, end: int = None) -> None:
    end = len(movies) - 1 if end is None else end

    values = movies[start:end + 1]
    minValue = math.floor(getattr(min(values, key=lambda movie: getattr(
        movie, attribute[0]), default=None), attribute[0]))
    maxValue = math.floor(getattr(max(values, key=lambda movie: getattr(
        movie, attribute[0]), default=None), attribute[0]))
    bucketsSize = maxValue-minValue+1
    buckets = [[] for _ in range(bucketsSize)]
    for value in values:
        buckets[math.floor(getattr(value, attribute[0])) -
                minValue].append(value)
    sortedValues = []
    for bucket in buckets:
        bucket.sort(key=lambda movie: getattr(movie, attribute[0]))
        sortedValues.extend(bucket)
    movies[start:end + 1] = sortedValues

    if not isAscending:
        movies[start:end + 1] = sortedValues[start:end + 1][::-1]

###################################################################################################################################################


def oddEvenSort(arr, attributes, isAscending=True):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, len(arr) - 1, 2):
            if isAscending:
                if isHigher(arr[i], arr[i + 1], attributes):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted = False
            else:
                if isLower(arr[i], arr[i + 1], attributes):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted = False
        for i in range(1, len(arr) - 1, 2):
            if isAscending:
                if isHigher(arr[i], arr[i + 1], attributes):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted = False
            else:
                if isLower(arr[i], arr[i + 1], attributes):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted = False

###################################################################################################################################################


def timSort(movies, attribute, isAscending=True):
    minimumRuns = 32
    n = len(movies)

    for start in range(0, n, minimumRuns):
        end = min(start + minimumRuns - 1, n - 1)
        insertionSort(movies, attribute, isAscending, start, end)

    size = minimumRuns
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min(n - 1, mid + size)
            merge(movies, start, mid, end, attribute, isAscending)

        size *= 2

    return movies

###################################################################################################################################################


def shellSort(movies, attributes, isAscending=True):
    n = len(movies)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = movies[i]
            j = i
            while j >= gap and ((isAscending and isLower(temp, movies[j - gap], attributes)) or
                                (not isAscending and isHigher(temp, movies[j - gap], attributes))):
                movies[j] = movies[j - gap]
                j -= gap
            movies[j] = temp
        gap //= 2

###################################################################################################################################################


def isLower(movieOne, movieTwo, attributes):
    isLower = False
    for attribute in attributes:
        if getattr(movieOne, attribute) < getattr(movieTwo, attribute):
            isLower = True
            break
        elif getattr(movieOne, attribute) > getattr(movieTwo, attribute):
            break
    return isLower


def isHigher(movieOne, movieTwo, attributes):
    isHigher = False
    for attribute in attributes:
        if getattr(movieOne, attribute) > getattr(movieTwo, attribute):
            isHigher = True
            break
        elif getattr(movieOne, attribute) < getattr(movieTwo, attribute):
            break

    return isHigher

###################################################################################################################################################
