# 2020 KAKAO BLIND RECRUITMENT - 외벽 점검

from itertools import combinations
from collections import deque

def solution(n, weak, dist):
    # 확인해야 하는 취약점 갯수.
    end = len(weak)

    # 일꾼을 거리의 역순으로 배치하여 각 명수별 최대 효율을 가져오기 위함.
    dist.sort(reverse = True)

    # 원형의 벽면. 한 바퀴를 돌았을 경우를 접근하기 쉽게 list 확장.
    circle = weak + list(map(lambda x: x+n, weak))

    # 취약점을 한 명이 전부 확인할 수 있는지 시작과 끝을 이은 거리 확인.
    for i in range(end):
        work = dist[0]

        # 취약점의 시작과 끝을 이은 거리가 일꾼이 확인할 수 있는 최대 거리와 같거나 작은지 확인.
        if work >= circle[i+end-1] - circle[i]:
            return 1

    # 두 명 이상의 경우는 모든 경우의 수를 확인.
    for i in range(2, len(dist)+1):

        # 거리 순으로 가장 효율적인 일꾼 i명을 고름.
        work = dist[:i]

        # 일꾼 i명을 배치 할 취약점 i곳을 고르는 경우의 수.
        for case in combinations([i for i in range(end)], i):
            deq = deque(case)
            cnt = end

            # 취약점을 모두 확인할 때 일꾼 한 명당 걸어야 하는 최소 거리.
            stack = []

            while deq:
                start = deq.popleft()

                # 배치 할 일꾼이 남아 있을 시: 시작점 부터 다음 배치 지역 한 개 전까지 확인.
                if deq:
                    area = circle[start:deq[0]]

                    # 확인한 취약점 제거.
                    cnt -= len(area)

                    # 일꾼 한 명이 움직여야 하는 최소 거리.
                    stack.append(area[-1] - area[0])

                # 마지막 일꾼이면 남아있는 모든 취약점 방문.
                else:
                    stack.append(circle[start+cnt-1] - circle[start])

            # 일꾼 당 걸어야 하는 거리를 역순으로 정렬.
            stack.sort(reverse = True)

            # 모든 일꾼이 거리를 충족할 수 있으면 일꾼의 수 return.
            if all(x >= y for x, y in list(zip(work, stack))):
                return i

    # 모든 일꾼을 사용해도 취약점을 확인할 수 없으면 -1 return.
    return -1

''' 주어진 문제의 벽면이 원형으로 이루어져 있어 이동이 비교적 자유로우며,
    일꾼 또한 어디든 위치할 수 있고, 이동하는 좌 우 방향의 규제 또한 없기에 자유도가 상당함.
    
    이런 문제일 수록 너무 많은 경우의 수를 생각하지 말고 단순하며 일관성 있게 접근하는 것이 좋음.
    
    이동 거리만을 구하면 되기에 시계 방향과 반시계 방향을 둘 다 고려하지 않아도 되며,
    ex) [5-10] 과 [10-5] 는 이동하는 거리가 같다.
    
    최소 거리를 구하는 것이기에 취약점으로 시작해 취약점으로 끝나는 경우만 확인하면 됨.
    
    combination을 직접 구현하거나, 사용하지 않는 방법으로 풀어볼 것.'''