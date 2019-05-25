# if being run from the shell
if __name__ == '__main__':
    # number of element
    n = int(input())
    s = set(map(int, input().split()))
    # number of commands
    n_commnd = int(input())
    for k in range(n_commnd):
        cmd = input().split()
        if cmd[0] == 'pop':
            s.pop()
        elif cmd[0] == 'remove':
            s.remove(int(cmd[1]))
        elif cmd[0] == 'discard':
            s.discard(int(cmd[1]))

    print(sum(s))