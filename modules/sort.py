def partition(arr, low, high, index):
    i = (low - 1)
    pivot = arr[high][1][index]

    for j in range(low, high):
        if arr[j][1][index] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high, index):
    if low < high:
        pi = partition(arr, low, high, index)
        quick_sort(arr, low, pi - 1, index)
        quick_sort(arr, pi + 1, high, index)


