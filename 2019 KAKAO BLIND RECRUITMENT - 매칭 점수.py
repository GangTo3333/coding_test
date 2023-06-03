# 2019 KAKAO BLIND RECRUITMENT - 매칭 점수

from collections import defaultdict

def solution(word, pages):
    # {url : index, 개인 score, [link]} 형식의 dict.
    dic = defaultdict(list)

    # index를 return 하기 위한 {index : score} 형식의 dict.
    score = defaultdict(int)

    # 대소문자에 관계 없이 단어의 사용 횟수를 알아내기 위해 소문자로 통일.
    word = word.lower()

    # pages 내의 page를 필요한 부분만 추출 후 dict에 정리.
    for i in range(len(pages)):

        # 주어진 형식에 의거, 순수한 url 추출.
        url = pages[i].split('<meta property="og:url" content="')[1]
        url = url[:url.index('"/>')]

        # 주어진 형식에 의거, url 내의 link 추출.
        link_list = pages[i].split('<a href="')[1:]

        # link의 개수가 하나 이상일 수 있고, 중복될 수 있어 list 형식으로 정리.
        stack = []
        for link in link_list:
            stack.append(link[:link.index('">')])

        # HTML 내의 word 등장 횟수를 찾기 위해 전체 page를 소문자 변환.
        page = pages[i].lower()
        cnt = 0
        empty = ''

        # 한 단어를 기준으로 비교해야하므로 단어 별로 일치하는지 확인.
        for s in page:
            if s.isalpha():
                empty += s
            else:
                if empty == word:
                    cnt += 1
                empty = ''

        # dict에 정보 담기.
        dic[url].extend([i, cnt, stack])

    # 기본 점수와 연결된 링크 수를 이용하여 점수 계산.
    for url in dic:
        idx, cnt, link_list = dic[url]
        score[idx] += cnt
        average = len(link_list)

        for link in link_list:
            if link in dic:
                score[dic[link][0]] += cnt / average

    # 최대 score를 가진 index를 찾기 위해 [index, score] 형식으로 변환.
    score = list(score.items())

    # score가 가장 큰 index를 return. 만약 동점일 경우 가장 작은 index를 return.
    score.sort(key = lambda x: (x[1], -x[0]), reverse = True)

    return score[0][0]

''' 지문이 길고, HTML 지식이 적어 마치 암호를 해독하는 느낌이었으나,
    필요한 정보를 문제에서 주어지는 대로 구현 후 추출하면 전혀 어렵지 않은 문제.
    
    "정규 표현식" 공부 이후, 깔끔하게 다시 풀어볼 것.'''