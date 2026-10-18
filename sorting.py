def BubbleSort(array, start, end, col_idx):
    comparisons = 0
    swaps = 0
    for i in range(end - start):
        swapped = False
        for j in range(start, end - i):
            comparisons += 1
            if array[j][col_idx] > array[j + 1][col_idx]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return comparisons, swaps



def SelectionSort(array, start, end, col_idx):
    comparisons = 0
    swaps = 0
    for i in range(start, end):
        min_idx = i
        for j in range(i + 1, end + 1):
            comparisons += 1
            if array[j][col_idx] < array[min_idx][col_idx]:
                min_idx = j
        if min_idx != i:
            array[i], array[min_idx] = array[min_idx], array[i]
            swaps += 1
    return comparisons, swaps



def InsertionSort(array, start, end, col_idx):
    comparisons = 0
    swaps = 0
    for i in range(start + 1, end + 1):
        current = array[i]
        j = i - 1
        while j >= start:
            comparisons += 1
            if current[col_idx] < array[j][col_idx]:
                array[j + 1] = array[j]
                swaps += 1
                j -= 1
            else:
                break
        array[j + 1] = current
    return comparisons, swaps



def MergeSort(array, start, end, col_idx, stats=None):
    if stats is None:
        stats = {"comps": 0, "swaps": 0}
    if start < end:
        mid = (start + end) // 2
        MergeSort(array, start, mid, col_idx, stats)
        MergeSort(array, mid + 1, end, col_idx, stats)
        Merge(array, start, mid, end, col_idx, stats)
    return stats["comps"], stats["swaps"]


def Merge(array, p, q, r, col_idx, stats):
    start, mid, end = p, q, r
    leftArray = array[start:mid + 1]
    rightArray = array[mid + 1:end + 1]
    
    i = j = 0
    k = start
    while i < len(leftArray) and j < len(rightArray):
        stats["comps"] += 1
        if leftArray[i][col_idx] <= rightArray[j][col_idx]:
            array[k] = leftArray[i]
            i += 1
        else:
            array[k] = rightArray[j]
            j += 1
            stats["swaps"] += 1
        k += 1

    while i < len(leftArray):
        array[k] = leftArray[i]
        i += 1
        k += 1

    while j < len(rightArray):
        array[k] = rightArray[j]
        j += 1
        k += 1



thresholdSize = 4

def HybridMergeSort(array, start, end, col_idx, stats=None):
    if stats is None:
        stats = {"comps": 0, "swaps": 0}
    baseCaseArraySize = end - start + 1

    if baseCaseArraySize <= thresholdSize:
        c, s = InsertionSort(array, start, end, col_idx)
        stats["comps"] += c
        stats["swaps"] += s
    else:
        mid = (start + end) // 2
        HybridMergeSort(array, start, mid, col_idx, stats)
        HybridMergeSort(array, mid + 1, end, col_idx, stats)
        Merge(array, start, mid, end, col_idx, stats)
    return stats["comps"], stats["swaps"]



import random

def quick_sort(arr, col_idx):
    stats = {"comps": 0, "swaps": 0}
    _quick_sort_helper(arr, 0, len(arr) - 1, col_idx, stats)
    return stats["comps"], stats["swaps"]


def _quick_sort_helper(items, low, high, col_idx, stats):
    if low < high:
        pi = partition(items, low, high, col_idx, stats)
        _quick_sort_helper(items, low, pi - 1, col_idx, stats)
        _quick_sort_helper(items, pi + 1, high, col_idx, stats)


def partition(items, low, high, col_idx, stats):
    rand_pivot_idx = random.randint(low, high)
    items[rand_pivot_idx], items[high] = items[high], items[rand_pivot_idx]
    stats["swaps"] += 1

    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        stats["comps"] += 1
        if items[j][col_idx] <= pivot[col_idx]:
            i += 1
            items[i], items[j] = items[j], items[i]
            stats["swaps"] += 1
    items[i + 1], items[high] = items[high], items[i + 1]
    stats["swaps"] += 1
    return i + 1



def shell_sort(arr, col_idx):
    comparisons = 0
    swaps = 0
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap:
                comparisons += 1
                if arr[j - gap][col_idx] > temp[col_idx]:
                    arr[j] = arr[j - gap]
                    swaps += 1
                    j -= gap
                else:
                    break
            arr[j] = temp
        gap //= 2
        
    return comparisons, swaps



def comb_sort(arr, col_idx):
    comparisons = 0
    swaps = 0
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
            comparisons += 1
            if arr[i][col_idx] > arr[i + gap][col_idx]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swaps += 1
                sorted_flag = False
            i += 1
            
    return comparisons, swaps



def counting_sort(arr, col_idx):
    comparisons = 0
    swaps = 0
    if not arr:
        return comparisons, swaps
    
    try:
        keys = [int(row[col_idx]) for row in arr]
    except ValueError:
        keys = [int(float(row[col_idx])) if str(row[col_idx]).strip() != '' else 0 for row in arr]
        
    min_val = min(keys)
    max_val = max(keys)
    range_of_elements = max_val - min_val + 1
    
    count = [0] * range_of_elements
    output = [None] * len(arr)

    for key in keys:
        count[key - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        key = keys[i]
        output[count[key - min_val] - 1] = arr[i]
        count[key - min_val] -= 1
        swaps += 1

    for i in range(len(arr)):
        arr[i] = output[i]
        
    return comparisons, swaps



def counting_sort_for_radix(arr, exp, col_idx, stats):
    n = len(arr)
    output = [None] * n
    count = [0] * 10
    
    keys = []
    for row in arr:
        try:
            val = int(row[col_idx])
        except ValueError:
            val = int(float(row[col_idx])) if str(row[col_idx]).strip() != '' else 0
        keys.append(val)
        
    for i in range(n):
        index = (keys[i] // exp) % 10
        count[index] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    for i in range(n - 1, -1, -1):
        index = (keys[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        stats["swaps"] += 1
        
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr, col_idx):
    stats = {"comps": 0, "swaps": 0}
    if not arr:
        return stats["comps"], stats["swaps"]
    
    keys = []
    for row in arr:
        try:
            val = int(row[col_idx])
        except ValueError:
            val = int(float(row[col_idx])) if str(row[col_idx]).strip() != '' else 0
        keys.append(val)
        
    max_val = max(keys)
    if max_val < 0:
        min_val = min(keys)
        for i in range(len(keys)):
            keys[i] -= min_val
        max_val = max(keys)
        
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp, col_idx, stats)
        exp *= 10
        
    return stats["comps"], stats["swaps"]



def bucket_sort(arr, col_idx):
    comparisons = 0
    swaps = 0
    if not arr:
        return comparisons, swaps if 'swapes' in locals() else swaps
        
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    vals = []
    for row in arr:
        try:
            v = float(row[col_idx])
        except ValueError:
            v = 0.0
        vals.append(v)
        
    min_v = min(vals)
    max_v = max(vals)
    span = max_v - min_v if max_v != min_v else 1.0
    
    for idx, row in enumerate(arr):
        normalized = (vals[idx] - min_v) / span
        bi = int(n * normalized)
        if bi >= n:
            bi = n - 1
        buckets[bi].append(row)
        
    for bucket in buckets:
        if len(bucket) > 1:
            bucket.sort(key=lambda x: float(x[col_idx]) if str(x[col_idx]).replace('.','',1).isdigit() else str(x[col_idx]))
            swaps += len(bucket)

    k = 0
    for bucket in buckets:
        for row in bucket:
            arr[k] = row
            k += 1
            swaps += 1
            
    return comparisons, swaps