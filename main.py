import copy
import math
import random
import time

import matplotlib.pyplot as plt


def build_source_table(filename):
    source_massive = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            from_city_to_others = []
            departure = line.split(' ')

            for l in lines:
                destination = l.split(' ')
                from_city_to_others.append(
                    [math.sqrt((float(departure[1]) - float(destination[1])) ** 2
                               + (float(departure[2]) - float(destination[2])) ** 2), 0.5, 0])
            source_massive.append(from_city_to_others)

    return source_massive


def update_coefficient(table):
    for row in table:
        for road in row:
            road[2] = 0
    return table


def update_feromon(table, routes, amountOfFeromonToAdd):
    for row in table:
        for road in row:
            road[1] *= 0.7  # Just 70% of feromon will stay
            if road[1] < 0.1:  # If the way has < 0.1 feromon, add feromon up to 0.1 (MMAS)
                road[1] = 0.1

    for index, route in enumerate(routes):  # Massive of routes

        route_arr = route.strip().split(" ")  # One route -> massive (eg 0 9 3 13 50 23... 0)

        for i in range(len(route_arr)):
            if i > 0:
                table[int(route_arr[i - 1])][int(route_arr[i])][1] += amountOfFeromonToAdd[index]  # Add feromon
                table[int(route_arr[i])][int(route_arr[i - 1])][1] += amountOfFeromonToAdd[index]  # Add feromon

    return table  # Returns the edited table


def solve(table, alpha, betta, c, Q):
    best_route = ""
    best_length = math.inf
    n = len(table[0])

    for iteration in range(250):
        routes = []
        amountOfFeromonToAdd = []

        for index in range(n):

            # table_to_use = copy.deepcopy(table)
            update_coefficient(table)
            probabilities = []
            current_row = index
            route = str(current_row) + " "
            length = 0

            for _ in range(n):
                summ = 0

                # Counting the probabilities of choosing local destination
                for road in table[current_row]:
                    if not (road[0] == 0) and (road[2] == 0):
                        summ += (c / (road[0])) ** betta * road[1] ** alpha

                for road in table[current_row]:
                    if not (road[0] == 0) and (road[2] == 0):
                        w = (c / (road[0])) ** betta
                        r = road[1] ** alpha
                        probabilities.append((w * r) / summ)
                    else:
                        probabilities.append(0)

                counting = 0
                if not (iteration % 10 == 0) or (iteration == 0):  # Simple ants
                    random_number = random.uniform(0, 1)

                    for index_local, probability in enumerate(probabilities):
                        counting += probability

                        if random_number <= counting:
                            counting = index_local
                            probabilities = []
                            length += table[int(route.strip().split(" ")[-1])][counting][0]
                            route += str(counting) + " "
                            break

                else:  # Elite ones
                    best_destination = probabilities[0]
                    for index_local, probability in enumerate(probabilities):
                        if probability >= best_destination:
                            best_destination = probability
                            counting = index_local

                    probabilities = []
                    length += table[int(route.strip().split(" ")[-1])][counting][0]
                    route += str(counting) + " "

                # Cleaning the column with the element we chose as a local destination
                for i, delete_column in enumerate(table):
                    table[i][current_row][2] = 1

                # Cleaning the row with the element we chose as a local destination
                for i, delete_row in enumerate(table[current_row]):
                    table[current_row][i][2] = 1

                current_row = counting

            length += table[int(route.strip().split(" ")[0])][index][0]  # Going back
            route += str(index)

            routes.append(route)

            if best_length > length:
                best_length = length
                best_route = route
                print(best_length)

            if not (iteration % 10 == 0) or (iteration == 0):
                amountOfFeromonToAdd.append(Q / length)
            else:
                amountOfFeromonToAdd.append(Q * 1.7 / length)  # If this ant is "elite", add more feromon

        update_feromon(table, routes, amountOfFeromonToAdd)

    return best_length, best_route


def draw(file_name, route, length):
    points_array = []

    with open(file_name, 'r') as file:
        for line in file:
            parts = line.split()
            x_coordinate = float(parts[1])
            y_coordinate = float(parts[2])

            points_array.append([x_coordinate, y_coordinate])

        city_indices = list(map(int, route.strip().split()))
        route_points = [points_array[index] for index in city_indices]

        x, y = zip(*route_points)

        plt.plot(x, y, color='#557070', linestyle='--')
        plt.scatter(x, y, color='green', marker='o', label='Cities')
        plt.title('Travelling salesman problem: solved!')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend([f'Length: {length}'])
        plt.show()


if __name__ == '__main__':
    start_time = time.time()

    file_name = 'data_tsp.txt'
    table = build_source_table(file_name)

    final_length, route = solve(table, 1.0, 4.0, 500, 320)
    print("\nBest ant-trip-length: ", final_length, " Best ant-trip:\n", route, "\n")

    draw(file_name, route, final_length)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(elapsed_time)
    # To see the result-table:
    # for row in table:
    #     print(row)
