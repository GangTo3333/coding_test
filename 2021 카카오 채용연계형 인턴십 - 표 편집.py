# 2021 카카오 채용연계형 인턴십 - 표 편집

def solution(n, k, cmd):
    # key 값으로 빠르게 접근하기 위한 dict 생성. value 값에는 [이전, 본인, 다음]의  데이터 삽입.
    table = {i : [i-1, i, i+1] for i in range(n)}

    # 가장 최근 삭제된 값인 "Z" 를 쉽게 알기 위한 삭제 리스트.
    delete = []
    start, end = k, n-1

    for order in cmd:
        # "C(삭제)" cmd 실행과 unpacking
        if order == "C":
            delete.append(table[start])
            up, x, down = table[start]

            # 현재 위치가 마지막 리스트일 경우 한 칸 위로 위치. (예외사항)
            if x == end:
                end, start  = up, up

            # 현재 위치가 0일 경우 table에 -1로 접근하여 발생하는 오류 차단.
            elif x == 0:
                start = down

            # 위의 경우가 아닐 시 한 칸 뒤, 한 칸 앞의 리스트를 연결. table 에서 현재의 값을 임의로 삭제.
            else:
                table[up][2], table[down][0] = down, up
                start = down

        # "Z(복구)" cmd 실행과 unpacking
        elif order == "Z":
            up, x, down = delete.pop()

            # 삭제한 end 값 복구 시 end 값 초기화.
            if x > end:
                end = x

            # 복구 데이터가 0일 경우 table에 -1로 접근하여 발생하는 오류 차단.
            elif x == 0:
                table[down][0] = x

            # 좌, 우 값에 다시 연결하여 데이터 복구.
            else:
                table[up][2], table[down][0] = x, x

        else:
            c, cnt = order.split(' ')

            # 포인터가 위로 가는 경우.
            if c == "U":
                # 연결한 리스트를 정해진 횟수만큼 타고 올라감.
                for i in range(int(cnt)):
                    start = table[start][0]

            # 포인터가 아래로 가는 경우.
            else:
                for i in range(int(cnt)):
                    start = table[start][2]

    answer = ['O'] * n
    for i in delete:
        answer[i[1]] = 'X'

    return "".join(answer)

    ''' remove 와 insert 를 사용하면 쉽게 해결할 수 있는 문제.
        그러나 두 함수는 리스트를 순회하며 삭제할 값이나, 삽입할 위치를 찾고, 이후 뒤의 모든 원소를 한 칸씩 당기거나 미루기에 
        시간복잡도가 O(N) 으로 매우 길다.
        
        따라서 삭제한 원소를 건너뛰며 원소들을 연결하고, 이 연결선을 따라 위와 아래로 가는 방식을 사용함.
        
        원소가 직접적으로 사라지는 것은 아니기에, 굳이 dict를 만들지 않고,
        본인의 값을 list의 index로 사용하면, 저장해야 하는 정보가 줄어들어 괜찮았을 것 같다는 생각.
        (table에는 앞, 뒤 연결 데이터만을 가지고, delete list에 본인의 index값을 추가로 저장하여 복구하는 방식.)
        
        class 함수를 사용하여 조금 더 입체적인 구현을 할 수 있었으면 조금 더 깔끔한 풀이가 되었을 것 같다는 생각.
        이후에 class 함수를 공부하고 난 뒤, class 함수를 활용해 볼 것.'''