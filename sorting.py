def InsertionSort(array,start,end):
    for i in range(start+1,end+1):
        current=array[i]
        j=i-1
        while j>=start and current<array[j]:
            array[j+1]=array[j]
            j-=1
        array[j+1]=current
    return array




def MergeSort(array,start,end):
    if start<end:
        mid=int((end+start)/2)
        MergeSort(array,start,mid)

        MergeSort(array,mid+1,end)

        Merge(array,start,mid,end)



def Merge(array,p,q,r):
    start=p
    mid=q
    end=r

    leftArraySize=mid-start+1
    rightArraySize=end-mid

    leftArray=[]

    rightArray=[]

    for i in range(leftArraySize):
        leftArray.append(array[i+start])

    for j in range(rightArraySize):
        rightArray.append(array[j+mid+1])

    leftIndex=0
    rightIndex=0
    arrayIndex=start

    while(leftIndex<leftArraySize and rightIndex<rightArraySize):
        if(leftArray[leftIndex]<rightArray[rightIndex]):
            array[arrayIndex]=leftArray[leftIndex]
            arrayIndex+=1
            leftIndex+=1
        else:
            array[arrayIndex]=rightArray[rightIndex]
            arrayIndex+=1
            rightIndex+=1

    while(leftIndex<leftArraySize):
        array[arrayIndex]=leftArray[leftIndex]
        arrayIndex+=1
        leftIndex+=1



    while(rightIndex<rightArraySize):
        array[arrayIndex]=rightArray[rightIndex]
        arrayIndex+=1
        rightIndex+=1



thresholdSize=4

def HybridMergeSort(array,start,end):
    baseCaseArraySize=end-start+1

    if(baseCaseArraySize<=thresholdSize):
        InsertionSort(array,start,end)
    else:
        mid=int((start+end)/2)
        HybridMergeSort(array,start,mid)
        HybridMergeSort(array,mid+1,end)
        Merge(array,start,mid,end)


def BubbleSort(array,start,end):
    for i in range(end-start):
        swapped=False
        for j in range(start,end-i):
            if(array[j]>array[j+1]):
                temp=array[j]
                array[j]=array[j+1]
                array[j+1]=temp
                swapped=True

        if swapped==False:
            break





def SelectionSort(array,start,end):
    for i in range(start,end):
        min=i
        for j in range(i+1,end+1):
            if array[j]<array[min]:
                min=j
        temp=array[i]
        array[i]=array[min]
        array[min]=temp





def quick_sort(arr):
    helper(arr, 0, len(arr) - 1)
    return arr





def helper(items, low, high):
    if low < high:
        pi = partition(items, low, high)
        helper(items, low, pi - 1)
        helper(items, pi + 1, high)





def partition(items, low, high):
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if items[j] <= pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[high] = items[high], items[i + 1]
    return i + 1


numbers = [38, 27, 43, 3, 9, 82, 10]
sorted_numbers = quick_sort(numbers)
print(sorted_numbers) 




def counting_sort(arr):
    if not arr:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    range_of_elements = max_val - min_val + 1
    
    count = [0] * range_of_elements
    output = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
        
    return output


print(counting_sort([-5, -10, 0, -3, 8, 5,-1, 10]))  






def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr


print(radix_sort([110, 45, 65,50, 90,602, 24, 2, 66]))  








def bucket_sort(arr):
    if not arr:
        return arr
    
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    for num in arr:
        bi = int(n * num)
        if bi >= n:
            bi = n - 1
        buckets[bi].append(num)
        
     
    for bucket in buckets:
        bucket.sort()
         

    k = 0
    for bucket in buckets:
        for num in bucket:
            arr[k] = num
            k += 1
            
    return arr


print(bucket_sort([0.897, 0.565, 0.656,0.1234, 0.665, 0.3434]))  




def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
        
    return arr



def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                
            arr[j] = temp
        gap //= 2
        
    return arr


def comb_sort(arr):
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
            if arr[i] > arr[i + gap]:

                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
            
    return arr