graph = {'A': {'B', 'C', 'D', 'E', 'F'},
         'B': {'A', 'C', 'D', 'E', 'F'},
         'C': {'A', 'B', 'D', 'E', 'F'},
         'D': {'A', 'B', 'C', 'E', 'F'},
         'E': {'A', 'B', 'C', 'D', 'F'},
         'F': {'A', 'B', 'C', 'D', 'E'}}


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        # print(stack)
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


dfs(graph, 'A') # {'E', 'D', 'F', 'A', 'C', 'B'}


def dfs_paths(graph, start, goal):

    stack = [(start, [start])]

    while stack:
        # print("stack", stack)
        (vertex, path) = stack.pop()

        possibilities = graph[vertex] - set(path) - set(goal)

        for next in graph[vertex] - set(path):

            nodes_in_path = verifying_nodes(path, graph[vertex] - set(goal))
            if next == goal and nodes_in_path is True:
                #yield path + [next]
                return path + [next]
            else:
                stack.append((next, path + [next]))


def dfs_paths_g(G, graph, start, goal):

    stack = [(start, [start])]

    while stack:
        # print("stack", stack)
        (vertex, path) = stack.pop()

        possibilities = graph[vertex] - set(path) - set(goal)

        for next in graph[vertex] - set(path):

            nodes_in_path = verifying_nodes(path, graph[vertex] - set(goal))
            if next == goal and nodes_in_path is True:
                #yield path + [next]
                return path + [next]
            else:
                stack.append((next, path + [next]))


def verifying_nodes(path, nodes):
    for i in nodes:
        if i not in list(path):
            return False
    return True

print(list(dfs_paths(graph, 'A', 'F'))) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]