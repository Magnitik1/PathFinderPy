import copy
import math
import random
import matplotlib.pyplot as plt

random.seed(1)


infile = open('berlin11_modified.tsp', 'r')
# infile = open('berlin52.tsp', 'r')
# infile = open('kroA100.tsp', 'r')

Name = infile.readline()  # NAME
FileType = infile.readline()  # TYPE
Comment = infile.readline()  # COMMENT
N = int(infile.readline().strip().split()[1])  # DIMENSION
EdgeWeightType = infile.readline()  # EDGE_WEIGHT_TYPE
infile.readline()
nodelist = []
solutions_array = []
found_cities = []
total_distance = 0

shuffled_array = []
for i in range(0, N):
    n, x, y = infile.readline().strip().split()
    nodelist.append([n, float(x), float(y)])

# Close input file
infile.close()


def add_positions_to_names(arr):
    for i in range(len(nodelist)):
        for j in range(len(arr)):
            if nodelist[i][0] == arr[j]:
                arr[j] = [nodelist[i][0], nodelist[i][1], nodelist[i][2]]
                break
    return arr


def distance_between_two_cities(name1, name2):
    a = False
    b = False
    for i in nodelist:
        if str(i[0]) == str(name1):
            a = i
        if str(i[0]) == str(name2):
            b = i
    if not a or not b:
        print("wrong input, there are no such city!")
        return
    q = math.sqrt(abs((b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2])))
    return q


def distance(name):  # greedy
    global shuffled_array
    global total_distance
    shuffled_array = []
    distance_sum = 0
    for i in nodelist:
        if str(i[0]) == str(name):
            a = i
    new_array = [a]
    total_distance = 0
    shuffled_array = copy.deepcopy(nodelist)
    shuffled_array.remove(a)
    shuffled_array.insert(0, a)
    way = ""
    for i in range(len(shuffled_array)):
        min = float('inf')
        city = []
        city0 = []
        for j in shuffled_array:
            if a == j[0] or new_array.__contains__(j):
                continue
            temp = distance_between_two_cities(a[0], j[0])
            if min > temp:
                min = temp
                city = j
                city0 = a
        if city == []:
            continue
        way += str('\n' + str(city0[0]) + "->" + str(city[0]) + " - " + str(float('{:.2f}'.format(min))))
        distance_sum += min
        new_array.append(city)
        a = city

    tt = distance_between_two_cities(new_array[0][0], new_array[-1][0])
    distance_sum += tt
    new_array.append(new_array[0])
    names = []
    for i in new_array:
        names.append(i[0])
    names.pop()
    return [float('{:.2f}'.format(distance_sum)), names]


def distance_rand(name):  # random
    global total_distance
    global shuffled_array
    a = False

    for i in nodelist:
        if str(i[0]) == str(name):
            a = i
    total_distance = 0
    shuffled_array = copy.deepcopy(nodelist)
    shuffled_array.remove(a)
    random.shuffle(shuffled_array)
    shuffled_array.insert(0, a)
    return distance_between_all_cities_in_chain(shuffled_array)


def distance_between_all_cities_in_chain(arr, num=0):
    global total_distance
    if num == 0:
        total_distance = 0
    if num + 1 < len(nodelist):
        q = math.sqrt(abs((arr[num + 1][1] - arr[num][1]) * (
                arr[num + 1][1] - arr[num][1]) + (
                                  arr[num + 1][2] - arr[num][2]) * (
                                  arr[num + 1][2] - arr[num][2])))

        arr[num].append(float('{:.2f}'.format(q)))
        total_distance += q
        total_distance = float('{:.2f}'.format(total_distance))
        return distance_between_all_cities_in_chain(arr, num + 1)
    else:
        q = math.sqrt(abs((arr[num][1] - arr[0][1]) * (
                arr[num][1] - arr[0][1]) + (
                                  arr[num][2] - arr[0][2]) * (
                                  arr[num][2] - arr[0][2])))
        arr[num].append(float('{:.2f}'.format(q)))
        total_distance += q
        total_distance = float('{:.2f}'.format(total_distance))

        names = []
        for i in arr:
            names.append(i[0])
        # tournament_list.append([total_distance, names])
        return [total_distance, names]


tournament_list = []
parents = []
children = []


def tournament_final(tournament_members):
    global parents
    min = tournament_members[0]
    for i in tournament_members:
        test = random.randrange(0, 50)
        if min[0] > i[0] and test != 5:
            min = i
    if len(parents) >= 2:
        parents = []
    parents.append(min)


def start_tournament():
    for j in range(2):
        tournament_members = []
        temp = []
        for i in range(8):
            p = random.randrange(1, len(tournament_list))
            if p not in temp:
                temp.append(p)
                tournament_members.append(tournament_list[p])
        tournament_final(tournament_members)


def get_all_greedy():
    global tournament_list
    for i in nodelist:
        t = distance(i[0])
        tournament_list.append(t)

def start(amount=N*10, new_gen=[]):#111111111111111111111112
    global tournament_list
    if new_gen == []:
        tournament_list = []
        get_all_greedy()
        for i in range(1, len(nodelist)):
            for j in range(9):
                tournament_list.append(distance_rand(i))
    else:
        tournament_list = new_gen
    for i in range(amount):
        start_tournament()
        create_next_generation()


next_tournament = []


def mutation_swap(arr):
    p1 = random.randrange(0, int(len(arr) / 2))
    p2 = random.randrange(int(len(arr) / 2), len(arr))
    q = arr[p1]
    arr[p1] = arr[p2]
    arr[p2] = q
    k = 0
    return arr


def mutation_reverse(arr):
    p1 = random.randrange(0, int(len(arr) / 2))
    p2 = random.randrange(int(len(arr) / 2), len(arr))
    pos = slice(p1, p2)
    arr1 = arr[pos]
    arr1.reverse()
    arr[pos] = arr1
    return arr


def create_next_generation():
    global next_tournament
    s1 = copy.deepcopy(parents[0][1])
    s2 = copy.deepcopy(parents[1][1])
    if parents[0][0] < parents[1][0]:
        s1, s2 = s2, s1
    p1 = random.randrange(0, int(len(s2) / 2))
    p2 = random.randrange(int(len(s2) / 2), len(s2))
    arr = []

    for i in range(p1, p2):
        arr.append(s2[i])

    temp_i = 0
    temp_j = 0
    insert_position = 0
    while temp_i + temp_j < len(s1):
        if s1[temp_i + temp_j] in arr:
            temp_j += 1
            continue
        insert_position += 1
        if insert_position > p1:
            insert_position = p2
        if insert_position >= len(s2):
            break
        arr.insert(insert_position, s1[temp_i + temp_j])

        temp_i += 1

    global total_distance
    # total_distance = 0
    # o = add_posotions_to_names(copy.copy(parents[0][1]))
    # kk = distance_between_all_cities_in_chain(o)
    # print("p1", kk)
    # total_distance = 0
    # o = add_posotions_to_names(copy.copy(parents[1][1]))
    # kk = distance_between_all_cities_in_chain(o)
    # print("p2", kk)
    total_distance = 0

    r = random.randrange(1, 21)
    if r == 20:
        arr = mutation_swap(arr)
    if r == 1:
        arr = mutation_reverse(arr)

    kk = distance_between_all_cities_in_chain(add_positions_to_names(arr))
    # print("ch", kk)
    # print()
    next_tournament.append(kk)
    global min_dis
    global count
    if kk[0] < min_dis:
        min_dis = kk[0]
    count += 1
    # print(count)


min_dis = float('inf')
count = 0
start()

answers = []
stop = 0
ij = 0
ij2 = 0
my_algorithm_plot = []
my_algorithm_plot_len = []
my_random_plot_len = []

for i in range(99999999999):
    ij2 = i
    start(N*10, next_tournament)#111111111111111111111112
    answers.append(min_dis)
    if i != 0 and answers[i] == answers[i - 1]:
        stop += 1
    else:
        my_algorithm_plot_len.append(ij)
        ij+=1
        print(i, '->', min_dis)
        stop = 0
        my_algorithm_plot.append(min_dis)
    if stop >= N*8:
        break

# print(ij, 'generations ->', min_dis, '!')


my_random_plot = []
my_min = float('inf')
for i in range(ij):
    a = distance_rand(i%N+1)
    my_random_plot.append(a[0])
    my_min = min(my_min, a[0])



my_min2 = float('inf')
for i in range(N):
    my_min2 = min(my_min, distance(i%N+1)[0])
print()
print(ij2, 'random ->', my_min, '!')
ff15 = str(ij)
for i in ff15:
    print(' ', end='')
print(' greedy ->', my_min2, '!')
print(ij2, 'generations ->', min_dis, '!')
my_algorithm_plot[0]=my_min2


my_greedy_plot = []
my_greedy_plot_len = []
for i in range(len(my_random_plot)):
    my_greedy_plot.append(my_min2)
    my_random_plot_len.append(i)
    my_greedy_plot_len.append(i)

plt.figure(facecolor='#C9A66B')
ax = plt.axes()
plt.plot(my_random_plot_len, my_random_plot, label="random")
plt.plot(my_algorithm_plot_len, my_algorithm_plot, label="my algorithm")
plt.plot(my_greedy_plot_len, my_greedy_plot, label="greedy")
plt.xlabel("Generations")
plt.ylabel("Best distance")
plt.title(Name)
plt.legend(loc="center right")
ax.set_facecolor("#EBDCB2")
plt.show()


