

class MergeRule(object):
    def __call__(self, from_data, to_data):
        merged_data = []
        merged_data.extend(to_data)
        merged_data.extend(from_data)
        return merged_data


class NumLimitRule(MergeRule):
    def __init__(self, num_limit):
        self.num_limit = num_limit

    def __call__(self, from_data, to_data):
        merged_data = super().__call__(from_data, to_data)
        return merged_data[:self.num_limit]


class SortRule(MergeRule):
    def __init__(self, key=None, reverse=False):
        self.key = key
        self.reverse = reverse

    def __call__(self, from_data, to_data):
        merged_data = super().__call__(from_data, to_data)
        merged_data.sort(key=self.key, reverse=self.reverse)
        return merged_data


def common_rule():
    '''
    1. 合并全部数据
    2. 以新到旧顺序
    '''
    def merge(from_data, to_data):
        merge = MergeRule()
        merged_data = merge(from_data, to_data)

        merged_data = merged_data[::-1]

        return merged_data

    return merge


def limit_rule(limit=50):
    '''
    限制数据数量
    '''
    def merge(from_data, to_data):
        merge = MergeRule()
        merged_data = merge(from_data, to_data)

        rule = NumLimitRule(num_limit=limit)
        merged_data = rule([], merged_data)

        return merged_data

    return merge


def sort_rule(key=None, reverse=False):
    '''
    合并后数据排序
    '''
    def merge(from_data, to_data):
        merge = MergeRule()
        merged_data = merge(from_data, to_data)

        rule = SortRule(key=key, reverse=reverse)
        merged_data = rule([], merged_data)

        return merged_data

    return merge


def unique_rule():
    '''
    去除重复的数据
    '''
    def merge(from_data, to_data):
        merge = MergeRule()
        merged_data = merge(from_data, to_data)

        u = []
        for item in merged_data:
            if item not in u:
                u.append(item)
        merged_data = u

        return merged_data

    return merge


def chain_rule(*rules):
    def merge(from_data, to_data):
        f = from_data
        t = to_data
        merged_data = []

        for rule in rules:
            merged_data = rule(f, t)
            f = []
            t = merged_data

        return merged_data

    return merge
