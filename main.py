import copy
import math
import random
import matplotlib.pyplot as plt


def build_source_table(filename):
    sourcemassive = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            from_city_to_others = []
            elements1 = line.split(' ')

            for l in lines:
                elements2 = l.split(' ')
                from_city_to_others.append(
                    [math.sqrt((float(elements1[1]) - float(elements2[1])) ** 2
                               + (float(elements1[2]) - float(elements2[2])) ** 2), 0.5])
            sourcemassive.append(from_city_to_others)

    return sourcemassive


def availible(table):
    for row in table:
        for P in row:
            if P[0] > 0:
                return True
    return False


def updateferomon(table, routes, amountOfFeromonToAdd):
    for row in table:
        for element in row:
            element[1] *= 0.8
            if element[1] < 0.5:
                element[1] = 0.5

    for index, route in enumerate(routes):
        route_arr = route.strip().split(" ")
        for i in range(len(route_arr)):
            if i > 0:
                table[int(route_arr[i - 1])][int(route_arr[i])][1] += amountOfFeromonToAdd[index]
                table[int(route_arr[i])][int(route_arr[i - 1])][1] += amountOfFeromonToAdd[index]

    return table


def method1(table, alpha, betta, n, Q):
    best_route = ""
    best_length = math.inf

    for iteration in range(200):
        routes = []
        amountOfFeromonToAdd = []

        for index, nextCity in enumerate(table):

            table_to_use = copy.deepcopy(table)
            cities = []
            current_row = index
            route = str(current_row) + " "
            length = 0
            Qplus = Q

            while True:
                summ = 0
                for dista_freo in table_to_use[current_row]:
                    if not (dista_freo[0] == 0):
                        summ += (n / (dista_freo[0])) ** alpha * dista_freo[1] ** betta

                for dista_freo in table_to_use[current_row]:
                    if not (dista_freo[0] == 0):
                        w = (n / (dista_freo[0])) ** alpha
                        r = dista_freo[1] ** betta
                        cities.append((w * r) / summ)
                    else:
                        cities.append(0)

                counting = 0
                if not (iteration % 4 == 0) or (iteration == 0):  # Simple ants
                    random_number = random.uniform(0, 1)

                    for index_local, city in enumerate(cities):
                        counting += city
                        if random_number <= counting:
                            counting = index_local

                            for iii, delete_column in enumerate(table_to_use):  # Cleaning the column with this element
                                table_to_use[iii][current_row][0] = 0

                            for iii, delete_row in enumerate(table_to_use[current_row]):  # Cleaning the column with
                                # this element
                                table_to_use[current_row][iii][0] = 0

                            cities = []
                            length += table[int(route.strip().split(" ")[-1])][counting][0]
                            route += str(counting) + " "
                            break

                else:  # Elite ones
                    best_destination = cities[0]
                    for index_local, city in enumerate(cities):
                        if city >= best_destination:
                            best_destination = city
                            counting = index_local

                    for iii, delete_column in enumerate(table_to_use):  # Cleaning the column with this element
                        table_to_use[iii][current_row][0] = 0

                    for iii, delete_row in enumerate(
                            table_to_use[current_row]):  # Cleaning the column with this element!!!!!
                        table_to_use[current_row][iii][0] = 0

                    cities = []
                    length += table[int(route.strip().split(" ")[-1])][counting][0]
                    route += str(counting) + " "

                if availible(table_to_use):
                    current_row = counting
                else:
                    length += table[int(route.strip().split(" ")[0])][index][0]
                    route += str(index)

                    routes.append(route)

                    if best_length > length:
                        best_length = length
                        best_route = route
                        print(best_length)
                        # if length <= 7235:
                        #     Qplus *= 2
                    if not (iteration % 4 == 0) or (iteration == 0):
                        amountOfFeromonToAdd.append(Qplus / length)
                    else:
                        amountOfFeromonToAdd.append(Qplus * 1.4 / length)

                    break

        updateferomon(table, routes, amountOfFeromonToAdd)

    return best_length, best_route


if __name__ == '__main__':

    table = build_source_table('data_tsp.txt')
    final_length, route = method1(table, 4, 1.0, 200, 240)
    print("\n!For de-bag only!\nBest ant-trip-length: ", final_length, " Best ant-trip:\n", route, "\n")

    points_array = []

    with open('data_tsp.txt', 'r') as file:
        for line in file:
            parts = line.split()
            point_id = int(parts[0])
            x_coordinate = float(parts[1])
            y_coordinate = float(parts[2])

            points_array.append([x_coordinate, y_coordinate])

        x, y = zip(*points_array)

        plt.scatter(x, y, color='blue', label='Cities')
        plt.title('Cities')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()

        for row in table:
            print(row)

    city_indices = list(map(int, route.strip().split()))
    route_points = [points_array[index] for index in city_indices]

    x, y = zip(*route_points)

    plt.plot(x, y, color='#557070', linestyle='--')
    plt.scatter(x, y, color='green', marker='o', label='Cities')
    plt.title('Travelling salesman problem: solved!')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend([f'Length: {final_length}'])
    plt.show()
