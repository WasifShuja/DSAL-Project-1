def InsertionSort(array, start, end, col_idx):
    for i in range(start + 1, end + 1):
        current = array[i]
        j = i - 1
        while j >= start and current[col_idx] < array[j][col_idx]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = current
    return array


def MergeSort(array, start, end, col_idx):
    if start < end:
        mid = int((end + start) / 2)
        MergeSort(array, start, mid, col_idx)
        MergeSort(array, mid + 1, end, col_idx)
        Merge(array, start, mid, end, col_idx)


def Merge(array, p, q, r, col_idx):
    start = p
    mid = q
    end = r

    leftArraySize = mid - start + 1
    rightArraySize = end - mid

    leftArray = []
    rightArray = []

    for i in range(leftArraySize):
        leftArray.append(array[i + start])

    for j in range(rightArraySize):
        rightArray.append(array[j + mid + 1])

    leftIndex = 0
    rightIndex = 0
    arrayIndex = start

    while leftIndex < leftArraySize and rightIndex < rightArraySize:
        if leftArray[leftIndex][col_idx] < rightArray[rightIndex][col_idx]:
            array[arrayIndex] = leftArray[leftIndex]
            arrayIndex += 1
            leftIndex += 1
        else:
            array[arrayIndex] = rightArray[rightIndex]
            arrayIndex += 1
            rightIndex += 1

    while leftIndex < leftArraySize:
        array[arrayIndex] = leftArray[leftIndex]
        arrayIndex += 1
        leftIndex += 1

    while rightIndex < rightArraySize:
        array[arrayIndex] = rightArray[rightIndex]
        arrayIndex += 1
        rightIndex += 1


thresholdSize = 4

def HybridMergeSort(array, start, end, col_idx):
    baseCaseArraySize = end - start + 1

    if baseCaseArraySize <= thresholdSize:
        InsertionSort(array, start, end, col_idx)
    else:
        mid = int((start + end) / 2)
        HybridMergeSort(array, start, mid, col_idx)
        HybridMergeSort(array, mid + 1, end, col_idx)
        Merge(array, start, mid, end, col_idx)


def BubbleSort(array, start, end, col_idx):
    for i in range(end - start):
        swapped = False
        for j in range(start, end - i):
            if array[j][col_idx] > array[j + 1][col_idx]:
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
                swapped = True
        if not swapped:
            break


def SelectionSort(array, start, end, col_idx):
    for i in range(start, end):
        min_idx = i
        for j in range(i + 1, end + 1):
            if array[j][col_idx] < array[min_idx][col_idx]:
                min_idx = j
        temp = array[i]
        array[i] = array[min_idx]
        array[min_idx] = temp


def quick_sort(arr, col_idx):
    helper(arr, 0, len(arr) - 1, col_idx)
    return arr


def helper(items, low, high, col_idx):
    if low < high:
        pi = partition(items, low, high, col_idx)
        helper(items, low, pi - 1, col_idx)
        helper(items, pi + 1, high, col_idx)


def partition(items, low, high, col_idx):
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if items[j][col_idx] <= pivot[col_idx]:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[high] = items[high], items[i + 1]
    return i + 1


def heapify(arr, n, i, col_idx):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left][col_idx] > arr[largest][col_idx]:
        largest = left

    if right < n and arr[right][col_idx] > arr[largest][col_idx]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, col_idx)


def heap_sort(arr, col_idx):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, col_idx)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, col_idx)
        
    return arr





def compare_multi_cols(rowA, rowB, col_indices):
    
    for idx in col_indices:
        valA = rowA[idx]
        valB = rowB[idx]
        if valA < valB:
            return True   
        elif valA > valB:
            return False  
    return True  

def MultiLevelMergeSort(array, start, end, col_indices):
    
    if start < end:
        mid = (start + end) // 2
        MultiLevelMergeSort(array, start, mid, col_indices)
        MultiLevelMergeSort(array, mid + 1, end, col_indices)
        MultiLevelMerge(array, start, mid, end, col_indices)

def MultiLevelMerge(array, p, q, r, col_indices):
    start = p
    mid = q
    end = r

    leftArraySize = mid - start + 1
    rightArraySize = end - mid

    leftArray = [array[i + start] for i in range(leftArraySize)]
    rightArray = [array[j + mid + 1] for j in range(rightArraySize)]

    leftIndex = 0
    rightIndex = 0
    arrayIndex = start

    while leftIndex < leftArraySize and rightIndex < rightArraySize:
        if compare_multi_cols(leftArray[leftIndex], rightArray[rightIndex], col_indices):
            array[arrayIndex] = leftArray[leftIndex]
            leftIndex += 1
        else:
            array[arrayIndex] = rightArray[rightIndex]
            rightIndex += 1
        arrayIndex += 1

    while leftIndex < leftArraySize:
        array[arrayIndex] = leftArray[leftIndex]
        arrayIndex += 1
        leftIndex += 1

    while rightIndex < rightArraySize:
        array[arrayIndex] = rightArray[rightIndex]
        arrayIndex += 1
        rightIndex += 1




def shell_sort(arr, col_idx):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap][col_idx] > temp[col_idx]:
                arr[j] = arr[j - gap]
                j -= gap
                
            arr[j] = temp
        gap //= 2
        
    return arr


def comb_sort(arr, col_idx):
    n = len(arr)
    gap = n
    shrink_factor = 1.33
    sorted_flag = False

    while not sorted_flag:
        gap = int(gap / shrink_factor)
        
        if gap <= 1:
            gap = 1
            sorted_flag = True

        i = 0
        while i + gap < n:
            if arr[i][col_idx] > arr[i + gap][col_idx]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
            
    return arr