# 2020 KAKAO BLIND RECRUITMENT - 기둥과 보 설치

# 기둥과 보를 조건에 맞게 배치할 수 있는지 확인.
def can(work):
    for x, y, a in work:
        if a == 0:
            # 기둥의 위 or 보의 좌, 우 끝에 기둥을 세웠는지 확인.
            if y == 0 or (x-1, y, 1) in work or (x, y, 1) in work or (x, y-1, a) in work:
                continue
            else:
                return False

        else:
            # 보의 좌, 우 끝의 아래에 기둥이 있는지 확인.
            if (x, y-1, 0) in work or (x+1, y-1, 0) in work:
                continue
            # 기둥이 없을 시 보와 보 사이에 이어져 있는지 확인.
            elif (x-1, y, a) in work and (x+1, y, a) in work:
                continue
            else:
                return False

    return True

def solution(n, build_frame):

    # 명령어 시행 후 in을 사용하며 확인하기에 list가 아닌 set를 사용. 시간복잡도를 줄임.
    work = set()

    for build in build_frame:
        x, y, a, b = build

        # 구조물을 설치하는 경우.
        if b == 1:
            # 일단 미리 설치하고, 이후에 가능한지 확인.
            work.add((x, y, a))

            # 조건에 부합하지 않으면 back
            if not can(work):
                work.remove((x, y, a))

        # 구조물을 제거하는 경우 또한 같다.
        else:
            work.remove((x, y, a))
            if not can(work):
                work.add((x, y, a))

    return sorted(list(work))

''' set를 활용하였고, 조건에 부합하지 않을 시 바로 return 하는 방법으로 시간을 단축했으나,
 달라지는 조건마다 모든 for 문을 도는 것은 불필요하다는 생각.
 
 그러나 조건을 먼저 확인하고 시행하기에는 구조물 제거 시 가정해야 하는 경우의 수가 상당하였으며,
 설치와 제거를 따로 구분하여 함수를 만들어야 하기에 많은 시간이 소요됨.
 
 건물을 설치하는 벽면의 크기 n을 활용하는 dp 풀이 또한 구상할 것.'''