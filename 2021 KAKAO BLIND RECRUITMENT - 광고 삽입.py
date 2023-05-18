# 2021 KAKAO BLIND RECRUITMENT - 광고 삽입

# "hh:mm:ss" 형식의 문자열을 초 단위의 int로 변환.
def convert(x):
    x = x.split(':')
    time = int(x[0])*3600 + int(x[1])*60 + int(x[2])
    return time

def solution(play_time, adv_time, logs):
    adv_time = convert(adv_time)
    play_time = convert(play_time)

    # "00:00:00" 부터 play_time 까지의 초 단위를 담은 배열.
    dp = [0 for i in range(play_time+1)]

    # 시청 기록을 빠르게 unpacking 하기 위해 누적합을 사용함.
    for log in logs:
        start, end = log.split('-')
        start = convert(start)
        end = convert(end)

        # 상영 시간을 계산하기 위함이므로 시청 시작 후 1초가 지난 시점부터 사람의 수 count.
        dp[start+1] += 1

        # 영상이 끝나기 전 시청 종료 시, 종료 이후 시간에 시청자 수 -1
        if play_time > end:
            dp[end+1] -= 1

    # 각 초별 시청자 수를 위한 반복문을 돌면서, 동시에 누적 광고 상영 시간을 running_time 에 저장.
    running_time = 0
    for i in range(1, adv_time+1):
        dp[i] = dp[i] + dp[i-1]
        running_time += dp[i]

    # 광고가 "00:00:00" 부터 시작했을 시 누적 광고 상영시간(running_time) 과 광고가 끝나는 시간 answer.
    answer = adv_time

    # 누적 광고 상영시간을 비교하기 위한 comparison.
    comparison = running_time

    # 1초씩 광고를 뒤로 미루면서 최댓값을 찾기 위함.
    idx = 1

    # 광고가 끝난 이후부터 영상이 종료하는 시점까지 1초씩 미루면서 비교. 누적합 또한 진행.
    for i in range(adv_time+1, play_time+1):
        dp[i] = dp[i] + dp[i-1]
        comparison += dp[i] - dp[idx]

        # 누적 광고 상영시간이 큰 쪽으로 광고 시간을 바꿈. 이후 running_time 또한 갱신.
        if comparison > running_time:
            running_time = comparison
            answer = i
        idx += 1

    # 누적합을 이용하였기에 광고가 끝나는 시간을 기준으로 답이 도출됨. 광고 시간을 빼 시작시간을 찾음.
    answer = answer - adv_time

    # 초 단위로 계산 된 답을 몫과 나머지 연산을 통해 "hh:mm:ss" 의 형식으로 바꿈.
    i, sec = divmod(answer, 60)
    hour, minute = divmod(i, 60)
    return ":".join(list(map(lambda x: str(x).rjust(2, '0'), [hour, minute, sec])))

''' dp를 이용하며 문제를 해결하였으나, 최대 359,999개의 초를 기록하는 배열을 굳이 만들었어야 하는가 하는 거부감이 듦.
    수많은 데이터를 받고 정보를 깔끔하게 정리할 수 있어 메모리의 낭비라 생각하지는 않으나, 누적합을 통한 계산은 정적인 정보였기에 가능했다는 생각.
    
    문제의 조건 상 정답은 logs 배열 내의 시청 기록 중 '시청 시작 시간' 혹은 '시청 종료 시간' 중 하나일 것이라 사료됨.
    누적합을 사용하지 않고, '영상 누적 시청 시간'에 관한 주제에 맞게 실시간으로 추가되는 정보 또한 빠르게 처리할 수 있는 방법을 생각해 볼 것.'''