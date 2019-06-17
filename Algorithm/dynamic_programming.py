# 白话算法之【动态规划入门】 https://blog.csdn.net/u013445530/article/details/45645307
def dynamic_programming(sum):
    '''如果我们有面值为1元、3元和5元的硬币若干枚，如何用最少的硬币凑够11元？'''
    coins = [1, 3, 5]
    # 我们假设存在1元的硬币那么i元最多只需要i枚1元硬币，当然最好设置dp[i]等于无穷大
    dp = [i for i in range(sum+1)]
    print(dp)
    for i in range(1,sum+1):
        for j in range(len(coins)):
            if i >= coins[j] and dp[i - coins[j]] < dp[i]:
                dp[i] = dp[i- coins[j]] + 1
                print(i, dp[i])
    return dp[sum]


def main():
    sum = 11
    count = dynamic_programming(sum)
    print('最少{}枚硬币凑够{}元'.format(count,sum))


if __name__ == '__main__':
    main()
