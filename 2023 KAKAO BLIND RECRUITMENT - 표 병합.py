# 2023 KAKAO BLIND RECRUITMENT - 표 병합

from collections import defaultdict

# 표의 크기는 50 x 50 으로 고정. [value, merge]의 형태로 각 좌표별 셀을 만듦.
dp = [[["EMPTY", set()] for i in range(51)] for j in range(51)]

# 좌표가 아닌 값을 통한 접근을 빠르게 하기 위한 {value : [좌표]} 형식의 dict.
dic = defaultdict(set)

# 셀에 값을 추가할 때.
def UPDATE(li):

    # 좌표를 통한 접근일 경우.
    if len(li) == 3:
        x, y, value = int(li[0]), int(li[1]), li[2]

        # dict | merge 를 용이하게 사용하기 위해 merge에 본인 값 삽입.
        dp[x][y][1].add((x, y))

        # 셀에 값이 없을 경우: 값 추가 이후 dict에 좌표 추가.
        if dp[x][y][0] == "EMPTY":

            # merge 한 list의 주소가 모두 같기 때문에 모든 병합된 셀의 값이 한 번에 바뀜.
            dp[x][y][0] = value

            # 연결된 모든 셀의 좌표를 dict에 삽입.
            dic[value] |= dp[x][y][1]

        # 셀에 값이 존재할 경우.
        else:
            # 연결된 모든 셀의 값이 변경. 차집합을 이용한 이전 값 제거.
            dic[dp[x][y][0]] -= dp[x][y][1]
            dp[x][y][0] = value

            # 바뀐 값에 연결된 모든 셀 삽입.
            dic[value] |= dp[x][y][1]

    # value를 통한 접근일 경우.
    else:
        value1, value2 = li

        # value를 가지는 모든 셀의 값 변경.
        for x, y in dic[value1]:
            dp[x][y][0] = value2

        # 변경된 셀의 좌표 옮김.
        dic[value2] |= dic[value1]

        # 같은 값으로 변경한 것이 아니면, 모든 값이 변경 되었으므로 이전 값 삭제.
        if value1 != value2:
            del dic[value1]

# 셀을 병합할 때.
def MERGE(li):
    x, y, r, c = map(int, li)
    value = "EMPTY"
    out = "EMPTY"

    # 같은 위치일 경우 무시.
    if x == r and y == c:
        return

    # merge를 하는 위치에 값이 존재할 경우: 모든 값을 해당 셀로 통일.
    if dp[x][y][0] != "EMPTY":
        value = dp[x][y][0]

        # 합쳐지는 위치에 다른 값이 존재하면, dict를 갱신하기 위한 값 추출.
        out = dp[r][c][0]

    # merge를 하는 위치에 값이 없으면 다른 위치의 값으로 통일. 둘 다 없으면 "EMPTY".
    else:
        value = dp[r][c][0]

    # 우선 두 셀을 병합.
    dp[x][y][1].update(((x, y), (r, c)))

    # 두 셀과 병합된 셀 또한 연결.
    merge = dp[x][y][1] | dp[r][c][1]

    # 덮어쓴 값 제거.
    if out != "EMPTY":
        dic[out] -= merge

    # 새로운 값 추가.
    if value != "EMPTY":
        dic[value] |= merge

    # 최종 값과 병합셀의 list.
    dp[x][y] = [value, merge]

    # 같은 list를 주소 그대로 삽입하여 update시 병합된 셀 또한 전부 바뀜.
    for r1, c1 in merge:
        dp[r1][c1] = dp[x][y]

# 셀의 병합을 해제할 때.
def UNMERGE(li):
    x, y = int(li[0]), int(li[1])
    value = dp[x][y][0]

    # 해제 후 병합 해제 된 셀들은 초기 상태로 전환. 해당 value의 dict 값을 전부 지우고 선택한 셀만 유지.
    if value != "EMPTY":
        dic[value] -= dp[x][y][1]
        dic[value].add((x, y))

    # 초기 상태로 전환하는 셀들은 다시 개별의 list를 줌.
    for r, c in dp[x][y][1]:
        dp[r][c] = ["EMPTY", set()]

    # 현재 위치의 선택된 셀의 값은 유지. merge 전부 해제.
    dp[x][y] = [value, set()]
    dp[x][y][1].add((x, y))

def solution(commands):
    answer = []

    for command in commands:
        command = command.split(' ')
        order = command[0]

        if order == "UPDATE":
            UPDATE(command[1:])

        elif order == "MERGE":
            MERGE(command[1:])

        elif order == "UNMERGE":
            UNMERGE(command[1:])

        elif order == "PRINT":
            x, y = int(command[1]), int(command[2])
            answer.append(dp[x][y][0])

    return answer

''' 단순 구현 문제였으나 수많은 조건과 고려해야하는 예외 사항들이 많아 곤란했던 문제.
    UPDATE value1 value2 에서 value1 = value2 의 경우를 차마 생각하지 못 해 많은 시간 소요.
    
    예외 사항이 제시되지 않으면 모든 경우의 수를 고려할 것.'''