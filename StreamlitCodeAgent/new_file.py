def find_paths(n, edges):
    from collections import defaultdict

    graph = defaultdict(list)
    for s, t in edges:
        graph[s].append(t)

    def dfs(current, path):
        if current == n:
            result.append(path.copy())
            return
        for neighbor in graph[current]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()

    result = []
    dfs(1, [1])
    return result if result else [-1]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().splitlines()
    
    n, m = map(int, data[0].split())
    edges = [tuple(map(int, line.split())) for line in data[1:m+1]]
    
    paths = find_paths(n, edges)
    if paths == [-1]:
        print(-1)
    else:
        for path in paths:
            print(" ".join(map(str, path)))
