# 《算法图解》第7章 狄克斯特拉算法 7.5实现

# 需要三个散列表
# 1.graph: 表示整个图graph; 2.costs: 每个节点的开销costs; 3.parents: 存储父节点的散列表
graph = {}

costs = {}

parents = {}

# 一个数组，用于记录处理过的节点，因为对于同一个节点，你不用处理多次
processed = []

def find_lowest_cost_node(costs):
    global processed
    # global costs
    lowest_cost = float("inf") 
    lowest_cost_node = None 
    for node in costs: #←------遍历所有的节点 
        cost = costs[node] 
        if cost < lowest_cost and node not in processed: #←------如果当前节点的开销更 低且未处理过， 
            lowest_cost = cost #←------就将其视为开销最低的节点 
            lowest_cost_node = node 

    return lowest_cost_node

def dijkstra():
    global graph
    global costs
    node = find_lowest_cost_node(costs) #←------在未处理的节点中找出开销最小的节点 
    while node is not None: #←------这个while循环在所有节点都被处理过后结束
        cost = costs[node] 
        neighbors = graph[node] 
        for n in neighbors.keys(): #←------遍历当前节点的所有邻居
            new_cost = cost + neighbors[n]
            if costs[n] > new_cost: #←------如果经当前节点前往该邻居更近，
                costs[n] = new_cost #←------就更新该邻居的开销
                parents[n] = node #←------同时将该邻居的父节点设置为当前节点 
        processed.append(node) #←------将当前节点标记为处理过 
        node = find_lowest_cost_node(costs) #←------找出接下来要处理的节点，并循环

def main():
    global graph
    global costs
    global parents


    #构建测试数据
    graph["start"] = {}
    graph["start"]["a"] = 5 
    graph["start"]["b"] = 2

    graph["a"] = {}
    graph["a"]["c"] = 4
    graph["a"]["d"] = 2

    graph["b"] = {}
    graph["b"]["a"] = 8
    graph["b"]["d"] = 7

    graph["c"] = {}
    graph["c"]["d"] = 6
    graph["c"]["fin"] = 3

    graph["d"] = {}
    graph["d"]["fin"] = 1

    graph["fin"] = {}   #←------终点没有任何邻居

    infinity = float("inf")
    costs["a"] = graph["start"]["a"] 
    costs["b"] = graph["start"]["b"]
    costs["c"] = infinity
    costs["d"] = infinity
    costs["fin"] = infinity

    parents["a"] = "start"
    parents["b"] = "start"
    parents["c"] = None
    parents["d"] = None
    parents["fin"] = None

    dijkstra()

    #打印结果
    result = ["fin"]
    p = parents["fin"]
    while p is not 'start':        
        result.append(p)
        p = parents[p]
    result.append('start') 
    result.reverse()
    print(result)
    print(costs["fin"])

if __name__ == '__main__':
    main()