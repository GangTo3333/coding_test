# 2023 KAKAO BLIND RECRUITMENT - 표현 가능한 이진트리

def solution(numbers):
    answer = []

    # 제한 사항의 각 원소 크기가 10의 15승 이하이므로, 트리의 깊이가 5 이상이 되는 경우는 없음.
    full = [1, 3, 7, 15, 31, 63]

    for number in numbers:

        # 각 원소를 이진수로 전환.
        tree = bin(number)[2:]

        # 포화 이진 트리에 적합한지 원소의 개수를 셈.
        len_tree = len(tree)

        # 포화 이진 트리가 아닐 경우, 최소 개수의 '0'을(더미 노드) 채워 넣어 포화 이진 트리로 만듦.
        for f in full:
            if len_tree <= f:
                tree = tree.rjust(f, '0')
                len_tree = len(tree)
                break

        # 모든 노드의 자식, 부모 관계 확인.
        while len_tree != 0:
            can = 1

            # 자식 노드가 있으나, 부모 노드가 없을 경우 불가능.
            for i in range(1, len_tree, 2):
                if tree[i] == '0':
                    if tree[i-1] == '1' or tree[i+1] == '1':
                        can = 0
                        break

            # 더미 노드가 아닌 모든 자식 노드에 부모 노드가 있을 경우.
            if can == 1:

                # root 노드만 남은 경우.
                if tree == '1':
                    answer.append(1)
                    break

                # 맨 밑 층을 없애고 다시 확인.
                else:
                    tree = tree[1::2]
                    len_tree = len(tree)

            # 불가능할 경우 탐색 종료. 백트래킹.
            else:
                answer.append(0)
                break

    return answer