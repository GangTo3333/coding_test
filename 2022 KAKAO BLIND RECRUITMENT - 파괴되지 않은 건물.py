# 2022 KAKAO BLIND RECRUITMENT - 파괴되지 않은 건물

def solution(board, skill):
    board_x, board_y = len(board[0]), len(board)

    # 공격, 회복 범위 한 칸 밖에 누적합을 위한 체크. dp를 한 칸 크게 만들면 skill unpacking 에서 범위를 제한하는 if문 생략 가능.
    dp = [[0 for i in range(board_x + 1)] for i in range(board_y + 1)]

    ''' skill unpacking. defaultdict로 좌표 범위 내에 데미지를 누적, {좌표 : 누적 데미지}를 만들어 비교하였으나,
     skill의 값이 넓어질 수록 누적합을 활용한 동시 계산이 훨씬 빠름.

     만약, 건물의 체력이 0 이하로 떨어졌을 때, 회복을 받을 수 없다는 조건이었다면 (동시 연산이 불가능)
     dp 보다는 dict 를 활용하는 것이 빠를 것.'''

    for li in skill:
        x, r1, c1, r2, c2, degree = li

        # dp에 '누적 데미지'를 기록하여, 재연산하는 과정 없이 단순 비교를 통한 답 도출 가능.
        if x == 2:
            degree = -degree

        # 2차원 배열에서의 누적합을 위한 초석
        dp[r1][c1] += degree
        dp[r2 + 1][c2 + 1] += degree
        dp[r2 + 1][c1] -= degree
        dp[r1][c2 + 1] -= degree

    # 가로로 먼저 누적합 진행. (x, y) 식의 기록을 사용해 한 번의 반복문만으로 결과를 도출할 수 있을지 고민하기.
    for y in range(board_y):
        for x in range(1, board_x):
            dp[y][x] += dp[y][x - 1]

    # 누적합이 끝난 첫 번째 줄을 먼저 비교하여 반복문에서의 예외 조건문 생략.
    answer = sum([dp[0][x] < board[0][x] for x in range(board_x)])

    # 누적 데미지와 건물의 내구도를 비교하여 결과 도출.
    for y in range(1, board_y):
        for x in range(board_x):
            dp[y][x] += dp[y - 1][x]
            answer += dp[y][x] < board[y][x]

    return answer