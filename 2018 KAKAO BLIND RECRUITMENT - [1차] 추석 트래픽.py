# 2018 KAKAO BLIND RECRUITMENT - [1차] 추석 트래픽

def solution(lines):
    answer = 0
    stack = []

    # lines 배열 unpacking.
    for i in range(len(lines)):
        line = lines[i].split()

        # 계산에 필요한 문자열을 숫자만 남김.
        S = line[1].split(':')
        T = line[2][:-1]

        # 정수는 int를 실수는 float 사용. 소수부분을 나타내는 것에 비트가 사용되므로 따로 구분.
        h, m, s = int(S[0]), int(S[1]), float(S[2])

        # 처리시간 또한 밀리초 단위로 주어지므로 float 사용.
        T = float(T) - 0.001

        # 비교가 용이하게 초 단위로 통일.
        time = h * 3600 + m * 60 + s

        # 시작 시간과 끝나는 시간을 배열에 담음.
        stack.extend([(time, i, 'out'), (time - T, i, 'in')])

    # 시작과 끝을 시간의 역순으로 담은 배열.
    stack.sort(reverse=True)

    # 초당 처리량을 담을 집합.
    one_sec = set()

    # 모든 시작 시간 혹은 끝나는 시간 부터 1초를 알기 위한 배열.
    start = stack.copy()

    while start:
        time, idx, in_out = start.pop()

        # 1초 뒤.
        end = time + 1

        # 1초 뒤의 시간 보다 짧으면 집합에 넣음. (중복 방지를 위한 set 사용.)
        while stack and stack[-1][0] < end:
            one_sec.add(stack.pop()[1])

        # 초당 최대 처리량이 바뀌면 갱신.
        answer = max(answer, len(one_sec))

        # 응답이 완료된 시간이었을 경우 제거.
        if in_out == 'out':
            one_sec -= {idx}

    return answer

''' 풀이 구상 이후, 차근차근 만들며 생각하니 어렵지 않았던 문제.
    "초당 최대 처리량" 만을 구하면 되는 문제였기에, 응답 시작 시간과 응답 완료 시간 부터 1초만을 고려하면 됨.
    
    lines 배열의 두 배인 stack 을 copy 하여 해결하는 것 보다, 시작시간과 완료시간을 다른 배열에 담아 확인하는 방법과
    
    set() 를 사용하면서 계속 len(set()) 함수를 불러내는 것이 아닌, in일 경우 +1 out일 경우 -1을 하면서
    이전 값을 기억하는 형태를 생각하는 것이 더 빨랐을 것이라는 아쉬움이 있음.'''