import copy
import math
import random
import matplotlib.pyplot as plt


def build_source_table(filename):
    source_massive = []

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
            source_massive.append(from_city_to_others)

    return source_massive


def updateferomon(table, routes, amountOfFeromonToAdd):
    for row in table:
        for element in row:
            element[1] *= 0.7  # Just 80% of feromon will stay
            if element[1] < 0.1:  # If the way has < 0.1 feromon, add feromon up to 0.1 (MMAS)
                element[1] = 0.1

    for index, route in enumerate(routes):  # Massive of routes

        route_arr = route.strip().split(" ")  # One route -> massive (eg 0 9 3 13 50 23... 0)

        for i in range(len(route_arr)):
            if i > 0:
                table[int(route_arr[i - 1])][int(route_arr[i])][1] += amountOfFeromonToAdd[index]  # Add feromon
                table[int(route_arr[i])][int(route_arr[i - 1])][1] += amountOfFeromonToAdd[index]  # Add feromon

    return table  # Returns the edited table


def solve(table, alpha, betta, n, Q):
    best_route = ""
    best_length = math.inf

    for iteration in range(250):
        routes = []
        amountOfFeromonToAdd = []

        for index, nextCity in enumerate(table):

            table_to_use = copy.deepcopy(table)
            probabilities = []
            current_row = index
            route = str(current_row) + " "
            length = 0

            for ant in range(len(nextCity)):
                summ = 0

                # Counting the probabilities of choosing local destination
                for dista_freo in table_to_use[current_row]:
                    if not (dista_freo[0] == 0):
                        summ += (n / (dista_freo[0])) ** betta * dista_freo[1] ** alpha

                for dista_freo in table_to_use[current_row]:
                    if not (dista_freo[0] == 0):
                        w = (n / (dista_freo[0])) ** betta
                        r = dista_freo[1] ** alpha
                        probabilities.append((w * r) / summ)
                    else:
                        probabilities.append(0)

                counting = 0
                if not (iteration % 4 == 0) or (iteration == 0):  # Simple ants
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
                for iii, delete_column in enumerate(table_to_use):
                    table_to_use[iii][current_row][0] = 0

                # Cleaning the row with the element we chose as a local destination
                for iii, delete_row in enumerate(table_to_use[current_row]):
                    table_to_use[current_row][iii][0] = 0

                current_row = counting

            length += table[int(route.strip().split(" ")[0])][index][0]  # Going back
            route += str(index)

            routes.append(route)

            if best_length > length:
                best_length = length
                best_route = route
                print(best_length)

            if not (iteration % 4 == 0) or (iteration == 0):
                amountOfFeromonToAdd.append(Q / length)
            else:
                amountOfFeromonToAdd.append(Q * 1.7 / length)  # If this ant is "elite", add more feromon

        updateferomon(table, routes, amountOfFeromonToAdd)

    return best_length, best_route


if __name__ == '__main__':

    table = build_source_table('data_tsp.txt')
    final_length, route = solve(table, 1.0, 4.0, 100, 320)
    print("\nBest ant-trip-length: ", final_length, " Best ant-trip:\n", route, "\n")

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

        # To see the result-table:
        # for row in table:
        #     print(row)

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
