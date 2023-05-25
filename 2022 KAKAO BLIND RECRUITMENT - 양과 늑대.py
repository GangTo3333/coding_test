# 2022 KAKAO BLIND RECRUITMENT - 양과 늑대

from collections import defaultdict

def solution(info, edges):
    answer = 0
    dic = defaultdict(list)

    ''' 최대 16 개의 노드들로 구성된 이진 트리에서 중복 방문을 방지하기 위한 집합.
        방문한 위치를 비트 연산을 활용해 1로 변환. ex) [0, 5, 2] 방문 시 100101를 10진수로 변환하여 방문했는지 확인.'''

    check = set()

    # [부모 노드, 자식 노드] 형식으로 이루어진 배열 edges를 {부모 노드 : [자식 노드]}의 dict 형식으로 unpacking
    for p, c in edges:
        dic[p].append(c)

    # '깊이 우선 탐색' 활용. (현재 노드, 양의 개수, 늑대의 개수, [이동 가능한 노드], 현재까지 방문한 길을 비트 마스킹)
    dfs = [(0, 0, 0, [], 0)]

    while dfs:
        node, sheep, wolf, next_node, mask = dfs.pop()

        # sheep += info[node] ^ 1 형식의 xor 사용 가능하나, 확인하는 수가 많을 수록 if - else 문이 빠름.
        if info[node]:
            wolf += 1
        else:
            sheep += 1

        # 늑대의 수가 양과 같아지는 순간 진행 불가능. 백트래킹
        if wolf == sheep:
            continue

        # 한 번 탐색했던 경로와 동일하면 탐색하지 않음.
        if mask in check:
            continue
        else:
            check.add(mask)

        # [이동 가능한 노드]에 현재 위치의 자식 노드 추가.
        next_node.extend(dic[node])

        # [이동 가능한 노드] 중 한 곳으로 이동. 이후 나머지는 [이동 가능한 노드]에 두고 dfs
        for i in next_node:
            new = next_node[:]
            new.remove(i)

            # 왼쪽 shift를 사용하여 masking.
            dfs.append((i, sheep, wolf, new, mask + (1 << i)))

        # 얻을 수 있는 양의 최댓값이 바뀌면 answer 갱신.
        answer = max(answer, sheep)

    return answer

''' 단일 위치가 아닌 경로를 재탐색하지 않기 위한 방법을 고민하던 중 비트 마스킹을 사용.
    아직 재귀 함수를 사용하여 dfs를 구현하는 것이 익숙하지 않아, 코드를 깔끔하게 정리하는 것에 한계가 있음.
    재귀 함수를 익히고 난 뒤 가독성이 좋은 코드를 만들어 볼 것.'''