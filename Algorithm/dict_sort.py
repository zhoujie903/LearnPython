# 漫画：什么是字典序算法？https://mp.weixin.qq.com/s/_mIeGKdvTOH-1jleJ4aADg


# 返回最近一个大于自身的相同数字组成的整数
def findNearestNumber(a):
    tmp = a.copy()
    # 1.从后向前查看逆序区域，找到逆序区域的前一位，也就是数字置换的边界
    index = findTransferPoint(tmp)
    if index == 0:
        return None

    # 2.把逆序区域的前一位和逆序区域中刚刚大于它的数字交换位置
    exchangeHead(tmp, index)

    # //3.把原来的逆序区域转为顺序
    reverse(tmp, index)
    return tmp


def findTransferPoint(a):
    for i in range(len(a)-1, 0, -1):
        if a[i] > a[i-1]:
            return i
    return 0


def exchangeHead(a, index):
    head = a[index-1]
    for i in range(len(a)-1, 0, -1):
        if head < a[i]:
            a[index-1] = a[i]
            a[i] = head
            break
    return a


def reverse(a, index):
    i = index
    j = len(a) - 1
    while i < j:
        tmp = a[i]
        a[i] = a[j]
        a[j] = tmp
        i += 1
        j -= 1
    return a


def main():
    a = [1, 2, 3, 5, 4]
    reslut = findNearestNumber(a)
    print(reslut)


if __name__ == '__main__':
    main()
