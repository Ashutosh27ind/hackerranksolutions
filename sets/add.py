# set.add
if __name__ == '__main__':
    n = int(input())
    stamps = set()
    for i in range(n):
        stamp = input()
        stamps.add(stamp)
        # Find the length of the set
    print(len(stamps))
