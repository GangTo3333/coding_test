# 2020 KAKAO BLIND RECRUITMENT - 블록 이동하기

from collections import deque

def solution(board):
    # 지도의 끝을 넘어가는지 계속 확인해야 하므로 미리 구해놓기.
    size = len(board)

    # 위치까지 이동된 거리를 기억하기 위한 dp. 로봇의 형태를 (가로(0), 세로(1)) 구분하기 위한 3차원 dp 사용.
    dp = [[[float('inf') for i in range(size)] for i in range(size)] for i in range(2)]

    dx, dy = (0, 0, 1, -1), (1, -1, 0, 0)

    # 모든 경로를 탐색하여 최단거리를 알기 위한 bfs. (로봇의 왼쪽 좌표, 로봇의 오른쪽 좌표, 이동 거리, 가로 or 세로 형태)
    bfs = deque([[(0, 0), (0, 1), 0, 0]])
    while bfs:
        (y, x), (c, r), cnt, way = bfs.popleft()
        cnt += 1

        # 형태를 유지한 상태로 상, 하, 좌, 우 이동.
        for i in range(4):
            qy, qx = y + dy[i], x + dx[i]
            qc, qr = c + dy[i], r + dx[i]

            # 지도를 넘어가는 경우는 생각하지 않음.
            if size in {qy, qx, qc, qr} or -1 in {qy, qx, qc, qr}:
                continue

            # 경로에 벽이 없는지 혹은, 최단경로가 맞는지 확인.
            else:
                if board[qy][qx] == 0 and board[qc][qr] == 0:
                    if dp[way][qy][qx] > cnt or dp[way][qc][qr] > cnt:
                        dp[way][qy][qx] = min(dp[way][qy][qx], cnt)
                        dp[way][qc][qr] = min(dp[way][qc][qr], cnt)

                        bfs.append([(qy, qx), (qc, qr), cnt, way])

        # 로봇이 가로일 경우 세로로 회전.
        if way == 0:
            way = 1

            # 왼쪽을 축으로 오른쪽을 위로 회전.
            if 0 < y and board[c - 1][r] == 0 and board[c - 1][r - 1] == 0 and dp[way][c - 1][r - 1] > cnt:
                dp[way][c - 1][r - 1] = cnt

                # bfs 에는 항상 위, 아래의 세로 모양으로 삽입.
                bfs.append([(c - 1, r - 1), (y, x), cnt, way])

            # 왼쪽을 축으로 오른쪽을 아래로 회전.
            if y < size - 1 and board[c + 1][r] == 0 and board[c + 1][r - 1] == 0 and dp[way][c + 1][r - 1] > cnt:
                dp[way][c + 1][r - 1] = cnt
                bfs.append([(y, x), (c + 1, r - 1), cnt, way])

            # 오른쪽을 축으로 왼쪽을 위로 회전.
            if 0 < y and board[y - 1][x] == 0 and board[y - 1][x + 1] == 0 and dp[way][y - 1][x + 1] > cnt:
                dp[way][y - 1][x + 1] = cnt
                bfs.append([(y - 1, x + 1), (c, r), cnt, way])

            # 오른쪽을 축으로 왼쪽을 아래로 회전.
            if y < size - 1 and board[y + 1][x] == 0 and board[y + 1][x + 1] == 0 and dp[way][y + 1][x + 1] > cnt:
                dp[way][y + 1][x + 1] = cnt
                bfs.append([(c, r), (y + 1, x + 1), cnt, way])

        # 로봇이 세로일 경우 가로로 회전.
        elif way == 1:
            way = 0

            # 위를 축으로 아래를 왼쪽으로 회전.
            if 0 < x and board[c][r - 1] == 0 and board[c - 1][r - 1] == 0 and dp[way][c - 1][r - 1] > cnt:
                dp[way][c - 1][r - 1] = cnt

                # bfs 에는 항상 좌, 우의 가로 모양으로 삽입.
                bfs.append([(c - 1, r - 1), (y, x), cnt, way])

            # 위를 축으로 아래를 오른쪽으로 회전.
            if x < size - 1 and board[c][r + 1] == 0 and board[c - 1][r + 1] == 0 and dp[way][c - 1][r + 1] > cnt:
                dp[way][c - 1][r + 1] = cnt
                bfs.append([(y, x), (c - 1, r + 1), cnt, way])

            # 아래를 축으로 위를 왼쪽으로 회전.
            if 0 < x and board[y][x - 1] == 0 and board[y + 1][x - 1] == 0 and dp[way][y + 1][x - 1] > cnt:
                dp[way][y + 1][x - 1] = cnt
                bfs.append([(y + 1, x - 1), (c, r), cnt, way])

            # 아래를 축으로 위를 오른쪽으로 회전.
            if x < size - 1 and board[y][x + 1] == 0 and board[y + 1][x + 1] == 0 and dp[way][y + 1][x + 1] > cnt:
                dp[way][y + 1][x + 1] = cnt
                bfs.append([(c, r), (y + 1, x + 1), cnt, way])

    # 가로와 세로 중 종점에 가장 빨리 도달한 거리를 return.
    return min(dp[0][-1][-1], dp[1][-1][-1])

''' 일반적인 구현 문제. 2*1 크기의 로봇을 사용하였기에 조건이 있는 회전까지 구현해야 함.
    회전 조건과 회전을 하는 경우의 수가 너무 많아 구현에 상당한 시간 소요.
    가로, 세로의 각 형태별 4 개의 회전을 일일이 구현하지 않고, 함축할 수 있는 방법을 생각해 볼 것.'''