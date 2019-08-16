# 漫画：什么是二叉堆？https://mp.weixin.qq.com/s/NJmGs5rLkxiKfYsipx5jCQ
# 漫画：什么是二叉堆？（修正版）https://mp.weixin.qq.com/s/cq2EhVtOTzTVpNpLDXfeJg
# 漫画：什么是堆排序？https://mp.weixin.qq.com/s/8Bid1naBLtEjPoP-R4HkBg


def upAdjust(array):
    '''
    上浮调整
    '''
    childIndex = len(array) - 1
    parentIndex = (childIndex-1) // 2
    # temp保存插入的叶子节点值，用于最后的赋值
    temp = array[childIndex]
    while childIndex > 0 and temp < array[parentIndex]:
        # 无需真正交换，单向赋值即可
        array[childIndex] = array[parentIndex]
        childIndex = parentIndex
        parentIndex = (childIndex-1) // 2

    array[childIndex] = temp


def downAdjust(array, parentIndex, length):
    '''
    下沉调整
    parentIndex     要下沉的父节点
    length          堆的有效大小
    '''
    # temp保存父节点值，用于最后的赋值
    temp = array[parentIndex]
    childIndex = 2 * parentIndex + 1
    while childIndex < length:
        # 如果有右孩子，且右孩子小于左孩子的值，则定位到右孩子
        if childIndex + 1 < length and array[childIndex + 1] < array[childIndex]:
            childIndex += 1

        # 如果父节点小于任何一个孩子的值，直接跳出
        if temp <= array[childIndex]:
            break

        # 无需真正交换，单向赋值即可
        array[parentIndex] = array[childIndex]
        parentIndex = childIndex
        childIndex = 2 * parentIndex + 1

    array[parentIndex] = temp


def buildHeap(array):
    for i in range(len(array)//2, -1, -1):
        heapify(array, len(array)-1, i)
        

def heapify(array, lastIndex, i):
    while True:
        maxPos = i
        if i * 2 + 1 <= lastIndex and array[i] < array[i * 2 + 1]: 
            maxPos = i * 2 + 1
        if i * 2 + 2 <= lastIndex and array[maxPos] < array[i * 2 + 2]:
            maxPos = i * 2 + 2
        if maxPos == i:
            break
        array[i], array[maxPos] = array[maxPos], array[i]
        i = maxPos  


def heap_short(array):
    # 1. 把无序数组构建成二叉堆
    buildHeap(array)
    k = len(array) - 1
    while k > 0:
        array[0], array[k] = array[k], array[0]
        k -= 1        
        heapify(array, k, 0)
        

def main():
    array = [1, 3, 2, 6, 5, 7, 8, 9, 10, 0]
    print("排序前：", array)
    heap_short(array)
    print("排序后：", array)

    array = [7, 1, 3, 10, 5, 2, 8, 9, 6]
    print("排序前：", array)
    heap_short(array)
    print("排序后：", array)



if __name__ == '__main__':
    main()
