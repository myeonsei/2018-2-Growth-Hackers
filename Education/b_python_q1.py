# 1안
def solution(n, money):
    money.sort(reverse=True)
    answer = 0
    for i, m in enumerate(money):
        if n > m:
            answer += solution(n-m, money[i:])
        elif n == m: answer += 1
    return answer
    
# 2안
def solution(n, money):
    money.sort()
    if n < money[0]: return 0
    answer = 0
    for i, m in enumerate(money):
        if n > m: 
            answer += solution(n-m, money[i:])
        elif n == m:
            answer +=1
            break
    return answer
    
# 효율성 문제 해결이 안됨. ^_^;;
