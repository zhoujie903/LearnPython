# 漫画：什么是冒泡排序？https://mp.weixin.qq.com/s/wO11PDZSM5pQ0DfbQjKRQA

array = [1, 2, 5, 4, 3, 6, 7, 8]
print('没排序前：\n', array)

count = 0  # 算法性能衡量：比较次数

# def bubble_sort(a):
#     '''
#     版本01
#     '''
#     tmp = 0
#     for i in range(0, len(a)):
#         for j in range(0, len(a) - i - 1):
#             global count
#             count += 1
#             if a[j] > a[j+1]:
#                 tmp = a[j]
#                 a[j] = a[j+1]
#                 a[j+1] = tmp


# def bubble_sort(a):
#     '''
#     版本02: 减少轮数
#     '''
#     tmp = 0
#     for i in range(0, len(a)):
#         # 有序标记，每一轮的初始是true
#         isSorted = True
#         for j in range(0, len(a) - i - 1):
#             global count
#             count += 1
#             if a[j] > a[j+1]:
#                 tmp = a[j]
#                 a[j] = a[j+1]
#                 a[j+1] = tmp
#                 # 有元素交换，所以不是有序，标记变为false
#                 isSorted = False

#         if isSorted:
#             break


def bubble_sort(a):
    '''
    版本03: 减少轮数 + 减少每轮比较次数
    '''
    # 记录最后一次交换的位置
    lastExchangeIndex = 0

    # 无序数列的边界，每次比较只需要比到这里为止
    sortBorder = len(a) - 1

    for i in range(0, len(a)):
        isSorted = True
        for j in range(0, sortBorder):
            global count
            count += 1
            if a[j] > a[j+1]:
                # 交换
                a[j], a[j+1] = a[j+1],  a[j]
                isSorted = False
                lastExchangeIndex = j

        sortBorder = lastExchangeIndex
        if isSorted:
            break

bubble_sort(array)
print('排序后：\n', array)
print('比较次数：', count)
