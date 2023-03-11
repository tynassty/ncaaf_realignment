import matplotlib.pyplot as plt

def divide_list_into_groups(lst, k):
    n = len(lst)
    group_size = n // k  # integer division
    remainder = n % k

    groups = []
    start = 0
    for i in range(k):
        if i < remainder:
            end = start + group_size + 1
        else:
            end = start + group_size
        groups.append(lst[start:end])
        start = end

    return groups


if __name__ == "__main__":
    # x = [i for i in range(100)]
    # y = [item+item for item in x]
    # plt.figure(figsize=(7, 7))
    # plt.plot(x, y, label="hello")
    # plt.title("a graph")
    # plt.legend()
    # plt.show()
    x = 134 // 10
    print(x)
