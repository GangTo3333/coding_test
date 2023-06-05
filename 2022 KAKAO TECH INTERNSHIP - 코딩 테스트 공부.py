# 2022 KAKAO TECH INTERNSHIP - 코딩 테스트 공부

def solution(alp, cop, problems):
    max_alp = alp
    max_cop = cop

    # 알고리즘 공부, 코딩 테스트 공부 케이스 추가.
    problems.extend([[0, 0, 1, 0, 1], [0, 0, 0, 1, 1]])

    for problem in problems:
        # 필요한 알고력, 필요한 코딩력, 획득 알고력, 획득 코딩력, 소요 시간의 형태.
        alp_req, cop_req, alp_rwd, cop_rwd, cost = problem

        # 문제를 모두 해결하기 위해 필요한 알고력과 코딩력 찾기. 최소값은 기본으로 가지고 있는 알고력과 코딩력.
        if alp_req > max_alp:
            max_alp = alp_req
        if cop_req > max_cop:
            max_cop = cop_req

    # 각각의 (알고력, 코딩력) 까지 도달하는데 걸리는 최소 시간을 담을 dp.
    dp = [[float('inf') for j in range(max_cop + 1)] for i in range(max_alp + 1)]

    # 현재 위치를 0 으로 하여 시작.
    dp[alp][cop] = 0

    for i in range(alp, max_alp + 1):
        for j in range(cop, max_cop + 1):
            for problem in problems:
                alp_req, cop_req, alp_rwd, cop_rwd, cost = problem

                # 문제를 풀고 축적된 알고력과 코딩력 갱신. dp의 범위를 벗어날 경우를 대비하여 상한선을 만듦.
                a = i + alp_rwd if i + alp_rwd < max_alp else max_alp
                c = j + cop_rwd if j + cop_rwd < max_cop else max_cop

                # (알고력[i], 코딩력[j]) 까지 도달하는 최소 시간이면 값 갱신. 다익스트라 알고리즘과 비슷함.
                if i >= alp_req and j >= cop_req:
                    dp[a][c] = min(dp[a][c], dp[i][j] + cost)

    return dp[-1][-1]

''' 처음에는 효율성 점수가 따로 존재하여 모든 경우를 대입해보는 것이 아닌, problems 배열 내의 획득 알고력, 코딩력을 소요 시간으로 나누어
    각 문제들의 알고력, 코딩력, 알고력과 코딩력 세 가지의 시간별 효율을 계산하고,
    현재 필요한 알고력과 코딩력을 통해 우선 순위를 매겨 최적의 방법을 선택, 해결하는 방식을 생각함.
    
    그러나 구현을 함에 있어 생각할 것들이 너무 많고, 예외 사항이 없다는 확신 또한 없었음.
    
    하여, problems 배열 내의 문제들을 하나씩 대입하되 이미 더 빠른 방법이 존재할 경우 더 찾지 않는 방식으로
    각 점수별 최소 시간만을 구하였으나, 어림잡아 계산해도 2,250,000 의 시간 복잡도가 계산되었으나 무난하게 해결함.
    
    컴퓨터는 초당 1억 번의 연산이 가능하다고 하니, 반복 대상과 주어진 제한사항을 통해 시간 복잡도를 계산해보고,
    반복에 대한 극심한 거부감은 오히려 독이 된다는 것을 느낌.'''