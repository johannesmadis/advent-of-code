lines = []
with open("./input.txt") as input_file:
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]


def differences(arr_numbers):
    result = []

    for index, num in enumerate(arr_numbers[1:]):
        result.append(num - arr_numbers[index])

    difference = 0
    if sum(result) != 0:
        result, difference = differences(result)

    return result, arr_numbers[-1] + difference


results = []
for line in lines:
    numbers = list(reversed([int(num) for num in line.split(" ")]))
    r0, result = differences(numbers)
    results.append(result)

print(sum(results))
