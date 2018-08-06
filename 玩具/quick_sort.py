# 漫画：什么是快速排序？（上）https://mp.weixin.qq.com/s/wXvs98RGumzFHvQlC1dOeA

# right
#     right > pivot:  移动right指针
#     right < pivot:  填坑[赋值]、index = right、移动left指针、换方向

# left
#     left < pivot:   移动left指针
#     left > pivot:   填坑[赋值]、index = left、移动right指针、换方向


def quick_sort(a, startIndex, endIndex):
    # 递归结束条件：startIndex大等于endIndex的时候
    if startIndex >= endIndex:
        return a

    # 得到基准元素位置
    pivotIndex = partition(a, startIndex, endIndex)

    # 用分治法递归数列的两部分
    quick_sort(a, startIndex, pivotIndex-1)
    quick_sort(a, pivotIndex+1, endIndex)
    return a


def partition(a, startIndex, endIndex):
    # 取第一个位置的元素作为基准元素
    pivot = a[startIndex]
    left = startIndex
    right = endIndex
    # 坑的位置，初始等于pivot的位置
    index = startIndex

    # 大循环在左右指针重合或者交错时结束
    while right >= left:
        # right指针从右向左进行比较
        while right >= left:
            if a[right] < pivot:
                a[left] = a[right]  # 填坑[赋值]
                index = right  # index = right
                left += 1  # 移动left指针
                break

            right -= 1

        # left指针从左向右进行比较
        while right >= left:
            if a[left] > pivot:
                a[right] = a[left]  # 填坑[赋值]
                index = left  # index = left
                right -= 1  # 移动right指针
                break

            left += 1

    a[index] = pivot
    return index


def main():
    a = [4, 7, 6, 5, 3, 2, 8, 1]
    print('没排序前：\n', a)
    reslut = quick_sort(a, 0, len(a)-1)
    print('排序后：\n', reslut)


if __name__ == '__main__':
    main()
