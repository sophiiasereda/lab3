import math
import re

maxsize = float('inf')

def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]


def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]

    return min


def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]

        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]

    return second


def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res

    if level == N:

        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return

    for i in range(N):

        if (adj[curr_path[level - 1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)

            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)

            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def TSP(adj):
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    for i in range(N):
        curr_bound += (firstMin(adj, i) +
                       secondMin(adj, i))

    curr_bound = math.ceil(curr_bound / 2)

    visited[0] = True
    curr_path[0] = 0

    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


file = open("l3-1.txt")
size = int(file.readline())

matrix = []

for line_index, line in enumerate(file):
    matrix.append(re.split('\s', re.sub('\n', '', line)))
    matrix[line_index] = list(map(int, matrix[line_index]))

adj = matrix
N = size

final_path = [None] * (N + 1)

visited = [False] * N

final_res = maxsize

TSP(adj)

print("Мінімальна вартість шляху:", final_res)
print("Покроковий шлях: ", end=' ')
for i in range(N + 1):
    print(final_path[i], end=' ')
print("")
