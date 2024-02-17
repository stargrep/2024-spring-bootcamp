# showcase how to debug a python recursion program.

def binary_search_1(arr: [], target: int) -> int:
    start = 0
    end = len(arr)
    while start < end:
        mid = (start + end) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    return -1


def binary_search_2(arr: [], target: int) -> int:
    start = 0
    end = len(arr)
    return binary_search_helper(arr, target, start, end)


def binary_search_helper(arr, target, low, high):
    if low > high:
        return -1  # interval is empty; no match
    else:
        mid = (low + high) // 2
    if target == arr[mid]:  # found a match
        return mid
    elif target < arr[mid]:
        # recur on the portion left of the middle
        return binary_search_helper(arr, target, low, mid - 1)
    else:
        # recur on the portion right of the middle
        return binary_search_helper(arr, target, mid + 1, high)


# assert(binary_search_1([1, 2, 4, 6, 10], 1) == 0)
assert (binary_search_2([1, 2, 4, 6, 10], 1) == 0)
