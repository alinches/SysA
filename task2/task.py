from collections import defaultdict
import csv


def main(var: str) -> str:
    
    edges = []
    for line in var.strip().split('\n'):
        if line.strip():
            parent_str, child_str = line.strip().split(',')
            parent, child = int(parent_str), int(child_str)
            edges.append((parent, child))
    
    nodes = set()
    for p, c in edges:
        nodes.add(p)
        nodes.add(c)
    nodes = sorted(nodes)
    
    children = {node: [] for node in nodes}
    parent = {node: None for node in nodes}
    for p, c in edges:
        children[p].append(c)
        parent[c] = p
    
    def get_ancestors(n):
        result = []
        cur = parent[n]
        while cur is not None:
            result.append(cur)
            cur = parent[cur]
        return result
    
    def get_descendants(n):
        result = []
        def dfs(u):
            for ch in children[u]:
                result.append(ch)
                dfs(ch)
        dfs(n)
        return result
    
    results = []
    for n in nodes:
        r1 = len(children[n])
        r2 = 1 if parent[n] is not None else 0
        desc = get_descendants(n)
        r3 = len(desc) - len(children[n])
        anc = get_ancestors(n)
        if parent[n] is not None:
            r4 = len(anc[1:]) if len(anc) > 1 else 0
        else:
            r4 = 0
        if parent[n] is not None:
            siblings = [x for x in children[parent[n]] if x != n]
            r5 = len(siblings)
        else:
            r5 = 0
        results.append([r1, r2, r3, r4, r5])
    
    output_lines = []
    for row in results:
        output_lines.append(",".join(str(x) for x in row))
    
    return "\n".join(output_lines)


if __name__ == "__main__":
    var = "1,2\n1,3\n3,4\n3,5"
    result = main(var)
    print(result)

