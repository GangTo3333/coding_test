# 2022 KAKAO TECH INTERNSHIP - 등산코스 정하기

from collections import defaultdict
from collections import deque

def solution(n, paths, gates, summits):
    answer = [float('inf'), float('inf')]
    dic = defaultdict(list)
    dp = [float('inf') for i in range(n + 1)]
    end = set(summits) | set(gates)

    # 각 지점별 이동할 수 있는 위치와 거리를 {현재 위치 : [이동 가능한 위치]} 의 형식으로 unpacking.
    for x, y, intensity in paths:
        dic[x].append((y, intensity))
        dic[y].append((x, intensity))

    # 모든 경로를 탐색하기 위한 bfs
    bfs = deque()

    # 시작 위치 삽입.
    for gate in gates:
        bfs.append((gate, 0))

    while bfs:
        course, intensity = bfs.popleft()

        # 각 위치별 이동 가능한 곳 탐색.
        for x, i in dic[course]:
            # 이동하는 각각의 거리 중 '가장 긴 거리' 로 갱신. ex) 1-2의 거리가 4일 경우, 2-x의 최소 거리를 4로 고정.
            i = max(i, intensity)

            # 다음 위치로 가는 경로 중 이동한 '가장 긴 거리' 가 짧을 경우.
            if dp[x] > i:
                dp[x] = i

                # 만약 도착 지점이 입구 혹은 정상일 경우 탐색 중지. (입구에서 도착 지점으로 가는 경로만 필요함.)
                if x in end:
                    continue

                # 현재 위치가 입구 혹은, 정상이 아닐 경우 계속 탐색.
                else:
                    bfs.append((x, i))

            # 다음 위치로 가는 각각의 경로 중 '가장 긴 거리' 가 더 짧을 경우 탐색 중지.
            else:
                continue

    # dp[summit] == 정상으로 가는 길 중 '가장 긴 거리' 가 최소인 경로.
    for summit in summits:
        if dp[summit] < answer[1]:
            answer = [summit, dp[summit]]

        elif dp[summit] == answer[1] and summit < answer[0]:
            answer = [summit, dp[summit]]

    return answer

''' 정상에 오른 뒤 돌아오는 제약(다른 출구로 나갈 수 없음) 또한 있었으나,
    같은 길로 되돌아오는 것이 가능하기에 정상에 도달하는 경로만 고려하면 됨.'''