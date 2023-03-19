from GA import GA


f = open('output.txt', 'w')
f.writelines("Best Solutions are: \n")
with open('input.txt', 'r') as file:
    lines = file.readlines()
    Input = []
    for i in lines:
        Input.append(i)

test_cases = int(Input[0])
input_index = 1

for T in range(test_cases):
    datapoints, degree = map(int, Input[input_index].split())
    input_index += 1

    x_array = []
    y_array = []

    for points in range(datapoints):
        x, y = map(float, Input[input_index].split())
        x_array.append(x)
        y_array.append(y)
        input_index += 1

    print("\n",test_cases)
    print(datapoints)
    print(degree)
    print(x_array)
    print(y_array)
    # Population size
    ga = GA(16)
    # nOfGenerations, degree, numdatapts, xarray, yarray
    ga.run(2, degree, datapoints, x_array, y_array)
    f.writelines("Case: " + str(T + 1) +"\n")
    f.writelines(str(ga.findBest()))
    f.writelines("\n\n")



