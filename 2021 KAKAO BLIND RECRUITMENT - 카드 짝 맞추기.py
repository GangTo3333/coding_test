# 2021 KAKAO BLIND RECRUITMENT - 카드 짝 맞추기

from collections import defaultdict
from collections import deque

# 각 위치로 이동하는 최소 거리가 담긴 배열 생성 함수.
def distance(start, board):
    a, b = start

    # 시작점 부터 각 칸 까지 거리를 담을 배열.
    m = [[float('inf') for i in range(4)] for i in range(4)]
    r, c = [0, 0, 1, -1], [1, -1, 0, 0]

    m[a][b] = 0

    # 최대한 빠르게 배열 내에 적은 수를 펼치기 위해 bfs 사용.
    bfs = deque([[(a, b), 0]])

    while bfs:
        (x, y), cnt = bfs.popleft()

        # 상, 하, 좌, 우로 한 칸씩 이동.
        for i in range(4):
            dx, dy = x + r[i], y + c[i]
            if dx >= 0 and dy >= 0 and dx <= 3 and dy <= 3 and m[dx][dy] > cnt + 1:
                m[dx][dy] = cnt + 1
                bfs.append([(dx, dy), cnt + 1])

        Ctrl_x = x
        Ctrl_y = y

        # Ctrl 키를 사용한 빈 공간 건너뛰기 구현.
        while Ctrl_x > 0:
            Ctrl_x -= 1
            if (Ctrl_x, y) in board or Ctrl_x == 0:
                if m[Ctrl_x][y] > cnt + 1:
                    m[Ctrl_x][y] = cnt + 1
                    bfs.append([(Ctrl_x, y), cnt + 1])
                Ctrl_x = x
                break

        while Ctrl_x < 3:
            Ctrl_x += 1
            if (Ctrl_x, y) in board or Ctrl_x == 3:
                if m[Ctrl_x][y] > cnt + 1:
                    m[Ctrl_x][y] = cnt + 1
                    bfs.append([(Ctrl_x, y), cnt + 1])
                Ctrl_x = x
                break

        while Ctrl_y > 0:
            Ctrl_y -= 1
            if (x, Ctrl_y) in board or Ctrl_y == 0:
                if m[x][Ctrl_y] > cnt + 1:
                    m[x][Ctrl_y] = cnt + 1
                    bfs.append([(x, Ctrl_y), cnt + 1])
                Ctrl_y = y
                break

        while Ctrl_y < 3:
            Ctrl_y += 1
            if (x, Ctrl_y) in board or Ctrl_y == 3:
                if m[x][Ctrl_y] > cnt + 1:
                    m[x][Ctrl_y] = cnt + 1
                    bfs.append([(x, Ctrl_y), cnt + 1])
                Ctrl_y = y
                break

    return m


def solution(board, r, c):
    answer = float('inf')

    # 같은 짝을 쉽게 찾기 위한 {카드 : {위치}} 형식의 dict.
    dic = defaultdict(set)

    # 남은 카드들을 담은 set.
    card_set = set()

    # board 를 돌며 카드가 있는 좌표를 형식에 맞게 정리.
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                dic[board[i][j]].add((i, j))
                card_set.add((i, j))

    # 백트래킹을 사용하기 위한 dfs. [카드 번호, 현재 위치, 남은 카드들(이동할 위치), 이동한 거리]
    dfs = [[board[r][c], (r, c), card_set.copy() - {(r, c)}, 0]]

    while dfs:
        card, start, check, cnt = dfs.pop()

        # 더이상 남은 카드가 없으면 종료.
        if not check:
            answer = min(answer, cnt)

        # 도착한 경우 보다 거리가 크면 구하지 않음. 백트래킹.
        if cnt >= answer:
            continue

        # 카드를 선택한 경우: 무조건 나머지 카드를 선택. 이후 카드 소멸.
        if card != 0:
            for other in dic[card] - {start}:
                x, y = other
                go = cnt + distance(start, check)[x][y]

                # [카드 초기화, 짝을 선택하고 난 뒤의 현재 위치, 선택 카드 제거, 총 이동 거리]
                dfs.append([0, other, check - {other}, go])

        else:
            # 현재 위치는 고정. 도착하는 위치만 바뀌는 것이므로 최소 거리를 담은 배열을 계속 구하지 않기 위해 저장.
            m = distance(start, check)

            # 선택한 카드가 없을 경우 남아있는 모든 카드로 가는 경우를 전부 구함.
            for x, y in check:
                go = cnt + m[x][y]

                # [선택한 카드, 이동 후 현재 위치, 선택 카드 제거, 총 이동 거리]
                dfs.append([board[x][y], (x, y), check - {(x, y)}, go])

    # 카드 선택 시 또한 1의 조작 횟수가 추가됨. 그러나 따로 구현하지 않고, 카드의 개수와 같을 수 밖에 없음에 착안.
    return answer + len(card_set)

''' 카드가 사라지면서 계속 바뀌는 경로와, 이동 후에는 기준이 바뀌기에 다시 최소 거리를 구해야 함.
    최단 거리만을 구하면 되는 것이 아니라 이를 이용하여 문제를 해결해야 됐기에 마치 두 문제를 푸는 것 같은 느낌이었다.
    
    이후 어떤 카드를 선택할지에 대해 모든 경우를 고려해야 했고, 또 각각의 경우 마다 달라지는 조건들을 어떻게 구현하는지가 관건이었음.
    
    차집합을 이용하여 계속 새로운 집합을 만들어 주면, 기존의 집합이나 board 자체를 deepcopy 하는 수고를 덜 수 있었고,
    bfs 와 dfs를 적합한 곳에 사용하여 유의미한 시간 단축 또한 이끌어 낼 수 있었음.
    
    Ctrl을 사용한 건너뛰기의 구현을 깔끔하게 다시 구현해볼 것.'''