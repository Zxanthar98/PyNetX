print('I print out the shortest bit string that contains all combinations of bit strings of length n!')

def allBits(n):
    s = '0' * n
    print(s)
    while len(s) < 2**n + n - 1:
        if s.count(s[- (n - 1):] + '1') == 0:
            s = s + '1'
        else:
            s = s + '0'
        print(s[-n:])
    return s
print(allBits(5))