import json

def main(varA: str, varB: str) -> str:
    rankingA = json.loads(varA)
    rankingB = json.loads(varB)
    
    def extract_objects(ranking):
        result = []
        for elem in ranking:
            if isinstance(elem, list):
                for x in elem:
                    result.append(x)
            else:
                result.append(elem)
        return result
    
    objsA = set(extract_objects(rankingA))
    objsB = set(extract_objects(rankingB))
    if objsA != objsB:
        raise ValueError("The two rankings do not have the same set of objects.")
    
    all_objs = sorted(list(objsA))
    index = {obj: i for i, obj in enumerate(all_objs)}
    
    def build_position_map(ranking):
        pos_map = {}
        current_rank = 0
        for elem in ranking:
            if isinstance(elem, list):
                for x in elem:
                    pos_map[x] = current_rank
                current_rank += 1
            else:
                pos_map[elem] = current_rank
                current_rank += 1
        return pos_map
    
    posA = build_position_map(rankingA)
    posB = build_position_map(rankingB)
    
    n = len(all_objs)
    Y_A = [[0]*n for _ in range(n)]
    Y_B = [[0]*n for _ in range(n)]
    
    for i_obj in all_objs:
        for j_obj in all_objs:
            i_idx = index[i_obj]
            j_idx = index[j_obj]
            # Для A
            if posA[j_obj] <= posA[i_obj]:
                Y_A[i_idx][j_idx] = 1
            else:
                Y_A[i_idx][j_idx] = 0
            
            # Для B
            if posB[j_obj] <= posB[i_obj]:
                Y_B[i_idx][j_idx] = 1
            else:
                Y_B[i_idx][j_idx] = 0
    
    def transpose(M):
        return list(map(list, zip(*M)))
    
    Y_A_T = transpose(Y_A)
    Y_B_T = transpose(Y_B)
    
    def mat_and(M1, M2):
        return [[1 if (M1[i][j] == 1 and M2[i][j] == 1) else 0 for j in range(n)] for i in range(n)]
    
    def mat_or(M1, M2):
        return [[1 if (M1[i][j] == 1 or M2[i][j] == 1) else 0 for j in range(n)] for i in range(n)]
    
    Y_AB = mat_and(Y_A, Y_B)
    Y_AB_prime = mat_and(Y_A_T, Y_B_T)
    Y_final = mat_or(Y_AB, Y_AB_prime)
    
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for i_obj in range(n):
        for j_obj in range(i_obj+1, n):
            if Y_final[i_obj][j_obj] == 0 and Y_final[j_obj][i_obj] == 0:
                graph[i_obj].append(j_obj)
                graph[j_obj].append(i_obj)
    
    visited = [False]*n
    def bfs(start):
        q = deque([start])
        visited[start] = True
        comp = [all_objs[start]]
        while q:
            u = q.popleft()
            for w in graph[u]:
                if not visited[w]:
                    visited[w] = True
                    comp.append(all_objs[w])
                    q.append(w)
        return comp
    
    kernels = []
    for i in range(n):
        if not visited[i] and i in graph:
            comp = bfs(i)
            if len(comp) == 1:
                continue
            comp.sort()
            kernels.append(comp)
    
    if not kernels:
        kernels = []
    
    return json.dumps(kernels, ensure_ascii=False)


if __name__ == "__main__":
    A_json = '[1,[2,3],4,[5,6,7],8,9,10]'
    B_json = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    print(main(A_json, B_json))
