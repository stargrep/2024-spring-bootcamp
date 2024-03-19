# 注意 - Copy this file and rename as assignment3_{first_name}.py then complete code with a pull request(PR).

# Q1. Given a positive integer N. The task is to write a Python program to check if the number is prime or not.
from typing import Tuple

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
            return True

"""
def is_prime(n: int) -> bool:
    if n == 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
"""

# DO NOT ALTER BELOW.
assert is_prime(2)
assert not is_prime(15)
assert is_prime(17)
assert is_prime(29)
assert is_prime(7907)


# Q2 Write a function rotate(ar[], d) that rotates ar[] of size n by d elements.
# Input ar = [1,2,3,4,5,6,7], d = 2
# Output [3,4,5,6,7,1,2]

def rotate(ar: [int], d: int) -> [int]:
    if d < len(ar):
        a1 = ar[:d]
        a2 = ar[d:]
        results = a2 + a1
    elif d == len(ar):
        results = ar
    else:
        d -= len(ar)
        a1 = ar[:d]
        a2 = ar[d:]
        results = a2 + a1
    return results

"""
def rotate(ar: [int], d: int) -> [int]:
    size = len(ar)
    d = d % size
    inplace_reverse(ar, 0, d - 1)
    inplace_reverse(ar, d, size - 1)
    inplace_reverse(ar, 0, size - 1)
    return ar

def inplace_reverse(ar: [int], start: int, end: int) -> None:
    while start < end:
        ar[start], ar[end] = ar[end], ar[start]
        start += 1
        end -= 1
"""

# DO NOT ALTER BELOW.
assert rotate([1, 2, 3, 4, 5, 6, 7], 2) == [3, 4, 5, 6, 7, 1, 2]
assert rotate([1, 2, 3], 4) == [2, 3, 1]


# Q3. Selection sort - implement a workable selection sort algorithm
# https://www.runoob.com/w3cnote/selection-sort.html 作为参考
# Input students would be a list of [student #, score], sort by score ascending order.

def selection_sort(arr: [[int]]) -> [[int]]:
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j][1] < arr[min_index][1]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# 测试
data = [[1, 100], [2, 70], [3, 95], [4, 66], [5, 98]]
selection_sort(data)
print(data)

"""
def selection_sort(arr: [[int]]) -> [[int]]:
    for i in range(len(arr) - 1):
        # 记录最小数的索引
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j][1] < arr[min_index][1]:
                min_index = j
        # i 不是最小数时，将 i 和最小数进行交换
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
"""

# DO NOT ALTER BELOW.
assert selection_sort([]) == []
assert selection_sort([[1, 100], [2, 70], [3, 95], [4, 66], [5, 98]]) == [[4, 66], [2, 70], [3, 95], [5, 98], [1, 100]]


# Q4. Convert a list of Tuples into Dictionary
# tip: copy operation - copy by value, copy by reference

def convert(tup: (any), di: {any, any}) -> None:
    for i in range(0, len(tup), 2):
        a = tup[i]
        b = tup[i+1]
        di[a] = b

"""
def convert(tup: any, di: {any, any}) -> None:
    for i in range(0, len(tup), 2):
        di[tup[i]] = tup[i + 1]
"""

# DO NOT ALTER BELOW.
expected_dict = {}
convert((), expected_dict)
assert expected_dict == {}

convert(('key1', 'val1', 'key2', 'val2'), expected_dict)
assert expected_dict == {'key1': 'val1', 'key2': 'val2'}


# Q5. Find left-most and right-most index for a target in a sorted array with duplicated items.
# provided an example of slow version of bsearch_slow with O(n) time complexity.
# your solution should be faster than bsearch_slow

def bsearch_slow(arr: [int], target: int) -> tuple[int, int]:
    left = -1
    right = -1
    for i in range(len(arr)):
        if arr[i] == target and left == -1:
            left = i
        if arr[i] > target and left != -1 and right == -1:
            right = i
        if i == len(arr) - 1:
            right = len(arr) - 1
    return left, right

def create_arr(count: int, dup: int) -> [int]:
    return [dup for i in range(count)]

# Complete this
def bsearch(arr: [int], target: int) -> tuple[int, int]:
    left = arr.index(target)
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] == target:
            right = i
    return left, right

assert bsearch_slow(create_arr(10000, 5), 5) == (0, 9999)
assert bsearch(create_arr(1000, 5), 5) == (0, 999)

import timeit

"""
def bsearch(arr: [int], target: int) -> Tuple[int, int]:
    return find_leftmost(arr, target), find_rightmost(arr, target)

def find_leftmost(arr: [int], target: int) -> int:
    start = 0
    end = len(arr) - 1
    while start < end - 1:
        mid = (start + end) // 2
        if arr[mid] >= target:
            end = mid
        else:
            start = mid + 1

    if arr[start] == target:
        return start
    if arr[end] == target:
        return end
    return -1

def find_rightmost(arr: [int], target: int) -> int:
    start = 0
    end = len(arr) - 1
    while start < end - 1:
        mid = (start + end) // 2
        if arr[mid] <= target:
            start = mid
        else:
            end = mid - 1

    if arr[end] == target:
        return end
    if arr[start] == target:
        return start
    return -1

assert bsearch_slow(create_arr(10000, 5), 5) == (0, 9999)
assert bsearch(create_arr(1000, 5), 5) == (0, 999)

import timeit
"""

# slow version rnning 100 times = ? seconds
print(timeit.timeit(lambda: bsearch_slow(create_arr(10000, 5), 5), number=100))

# add your version and compare if faster.
print(timeit.timeit(lambda: bsearch(create_arr(10000, 5), 5), number=100))

# Q6.
"""
请实现2个python list的‘cross product’ function.
要求按照Numpy中cross product的效果: https://numpy.org/doc/stable/reference/generated/numpy.cross.html
只实现 1-d list 的情况即可.
x = [1, 2, 0]
y = [4, 5, 6]
cross(x, y)
> [12, -6, -3]
"""
def cross_product(x:[int], y:[int]) -> [int]:
    return [x[1]*y[2]-x[2]*y[1],
            x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0]]

assert cross_product([1,2,0], [4,5,6]) == [12,-6,-3]

# Q7.
"""
交易传输指令经常需要验证完整性，比如以下的例子
{ 
    request : 
    { 
        order# : 1, 
        Execution_details: ['a', 'b', 'c'],
        request_time: "2020-10-10T10:00EDT"
    },
    checksum:1440,
    ...
}
可以通过很多种方式验证完整性，假设我们通过判断整个文本中的括号 比如 '{}', '[]', '()' 来判断下单是否为有效的。
比如 {{[],[]}}是有效的，然而 []{[}](是无效的。 
写一个python程序来进行验证。
 def checkOrders(orders: [str]) -> [bool]:
 return a list of True or False.
checkOrders(["()", "(", "{}[]", "[][][]", "[{]{]"] return [True, False, True, True, False]
"""
def chech_orders(orders: [str]) -> [bool]:
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    outcome1 = True
    outcome2 = True
    outcome3 = True
    for i in range(len(orders)):
        if "{" in orders[i]:
            count1 += 1
        elif "}" in orders[i]:
            count2 += 1
            if count1 == count2:
                outcome1 = True
            else:
                outcome1 = False
        elif "[" in orders[i]:
            count3 += 1
        elif "]" in orders[i]:
            count4 += 1
            if count3 == count4:
                outcome2 = True
            else:
                outcome2 = False
        elif "(" in orders[i]:
            count5 += 1
        elif ")" in orders[i]:
            count6 += 1
            if count5 == count6:
                outcome3 = True
            else:
                outcome3 = False
        results = (outcome1 and outcome2) and outcome3
    return results

chech_orders(["()", "(", "{}[]", "[][][]", "[{]{]"])

"""
def check_order(order: str, patterns: {str: str}) -> bool:
    stack = []  # append, pop
    for c in order:
        if c in patterns:  # close
            if len(stack) == 0 or stack.pop() != patterns[c]:
                return False
        else:  # open
            stack.append(c)
    return len(stack) == 0


def check_orders(orders: [str]) -> [bool]:
    patterns = {")": "(", "}": "{", "]": "["}
    return [check_order(o, patterns) for o in orders]

assert check_orders(["()", "(", "{}[]", "[][][]", "[{]{]"]) == [True, False, True, True, False]
"""

# Q8.
"""
我们在进行交易的时候通常会选择一家broker公司而不是直接与交易所交易。
假设我们有20家broker公司可以选择 (broker id is [0, 19])，通过一段时间的下单表现(完成交易的时间)，我们希望找到最慢的broker公司并且考虑与其解除合约。
我们用简单的数据结构表达broker公司和下单时间: [[broker id, 此时秒数]]
[[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]
解读: 
Broker 0 使用了 2s - 0s = 2s
Broker 1 使用了 5 - 2 = 3s
Broker 2 使用了 7 - 5 = 2s
Broker 0 使用了 16 - 7 = 9s
Broker 3 使用了 19 - 16 = 3s
Broker 4 使用了 25 - 19 = 6s
Broker 2 使用了 35 - 25 = 10s
综合表现，是broker2出现了最慢的交易表现。
Def slowest(orders: [[int]]) -> int:
slowest([[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]) return 2
"""

def slowest(orders: [[int]]) -> int:
    i = 0
    slowest = 0
    for i in range(20):
        times = orders[i+1][1] - orders[i][1]
        id = orders[i][0]
        dict[id : times]
        print("Broker " + id + " 使用了 " + orders[i+1][1] + "s - " + orders[i][1] + "s = " + times + "s"+"\n")
        i += 1
        if times > slowest:
            slowest = times
            print("综合表现，是broker" + dict.keys(slowest) + "出现了最慢的交易。")

"""
def slowest_broker(orders: [[int]]) -> int:
    brokers = [0 for i in range(20)]
    prev_time = 0
    for o in orders:
        b_id = o[0]
        time_spent = o[1] - prev_time
        prev_time = o[1]
        brokers[b_id] = max(brokers[b_id], time_spent)
    (_, idx) = max((v, idx) for idx, v in enumerate(brokers))
    return idx

assert slowest_broker([[0, 2], [1, 5], [2, 7], [0, 16], [3, 19], [4, 25], [2, 35]]) == 2
"""

# Q9.
"""
判断机器人是否能返回原点
一个机器人从平面(0,0)的位置出发，他可以U(向上), L(向左), R(向右), 或者D(向下)移动一个格子。
给定一个行走顺序，问是否可以回到原点。
例子
1. moves = "UD", return True.
2. moves = "LL", return False.
3. moves = "RRDD", return False.`
4. moves = "LDRRLRUULR", return False.
def judgeRobotMove(moves: str) -> bool:
"""

def judge_robot_move(moves: str) -> bool:
    position = [0, 0]
    move_pos = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    for move in moves:
        if move in move_pos:
            position[0] += move_pos[move][0]
            position[1] += move_pos[move][1]
        else:
            print("输入错误")
    return position == [0, 0]

# Q10.
"""
假设我们获得了一只股票的每日价格, 在这一天可以执行T+1买或卖的操作, 只能做多不能做空，每次只能持仓一股。
对于给定的价格序列，只能执行最多两次交易，写一个算法计算最高获利可以是多少。
Input: prices = [2,2,6,1,2,4,2,7]
Output: 10
解释: 6 - 2 + 7 - 1 = 10
Input: prices = [5, 3, 0]
Output: 0
解释: 没有交易。
Input: prices = [1,2,3,4,5,6,7]
Output: 6
解释: 7 - 1 = 6 因为只能持仓一股，不能再没有卖出1时购买。
"""

"""
def max_profit2(prices: [float]) -> float:
    cost1, cost2 = float('inf'), float('inf')
    profit1, profit2 = 0, 0

    for p in prices:
        cost1 = min(cost1, p)
        profit1 = max(profit1, p - cost1)
        cost2 = min(cost2, p - profit1)
        profit2 = max(profit2, p - cost2)

    return profit2

assert max_profit2([2, 2, 6, 1, 2, 4, 2, 7]) == 10
"""