# 漫画：什么是计数排序？ https://mp.weixin.qq.com/s/WGqndkwLlzyVOHOdGK7X4Q


def countSort(a):
    # 1.得到数列的最大值和最小值，并算出差值d
    max = a[0]
    min = a[0]
    for item in a:
        if item > max:
            max = item

        if item < min:
            min = item

    d = max - min
    # 2.创建统计数组并统计对应元素个数
    countArray = [0] * (d+1)
    for item in a:
        countArray[item - min] += 1

    # 3.统计数组做变形，后面的元素等于前面的元素之和
    sum = 0
    for i, item in enumerate(countArray):
        sum += item
        countArray[i] = sum

    # 4.倒序遍历原始数列，从统计数组找到正确位置，输出到结果数组
    sortedArray = [0] * len(a)
    for item in reversed(a):
        sortedArray[countArray[item - min] - 1] = item
        countArray[item-min] -= 1
    return sortedArray


def main():
    array = [95, 94, 91, 98, 99, 90, 90, 93, 91, 92]
    sortedArray = countSort(array)
    print(sortedArray)


if __name__ == '__main__':
    main()
