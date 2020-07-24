from collections import Counter


def countMedian(l):
    l.sort()

    if len(l) % 2 == 1:
        m = l[len(l) // 2]
    else:
        m = (l[int(len(l) / 2)] + l[int(len(l) / 2 - 1)]) / 2

    return m


def countMode(l):
    counter = Counter(l)
    return counter.most_common(1)[0][0]


def main(arr):
    if arr:
        print('mode', countMode(arr))
        print('median', countMedian(arr))
        print('average:', sum(arr) / len(arr))


arr = [114, 116, 130, 142, 133, 118, 120, 126, 126, 122, 142, 124, 112, 140, 124, 123, 125, 132, 123, 120, 150, 114, 124, 118, 131, 120, 137, 121, 124, 124, 124]
main(arr)