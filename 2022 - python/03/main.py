priority_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
priorities = {}
for char,i in enumerate(priority_list):
    priorities[i] = char


# part1
with open("C:/Users/kasutaja7yh/Desktop/aoc-2022/03/input.txt") as inputs:

    input_lines = [x.strip() for x in inputs.readlines()]

    sums = []
    for input_line in input_lines:
        priority_table_0 = [0]*52
        priority_table_1 = [0]*52
        half_length = int(len(input_line) / 2) 
        [sack0, sack1] = (input_line[:half_length],input_line[half_length:])

        for char in sack0:
            priority_table_0[priorities[char]] = 1
        for char in sack1:
            priority_table_1[priorities[char]] = 1

        priority_table_2 = [0]*52
        for i in range(52):
            priority_table_2[i] = priority_table_0[i] * priority_table_1[i] * (i + 1)

        
        sums.append(sum(priority_table_2))

    print(sum(sums))


#part2
with open("C:/Users/kasutaja7yh/Desktop/aoc-2022/03/input.txt") as inputs:

    input_lines = [x.strip() for x in inputs.readlines()]

    sums = []
    for group_index in range(0,len(input_lines),3):
        line0 = input_lines[group_index]
        line1 = input_lines[group_index+1]
        line2 = input_lines[group_index+2]

        tables = ([0]*52,[0]*52,[0]*52)
        lines = (line0, line1, line2)
        for i, line in enumerate(lines):
            for c, char in enumerate(line):
                tables[i][priorities[char]] = 1

        summed_table = [1]*52
        for table in tables:
            for n, item in enumerate(table):
                summed_table[n] *= item

        for a, item in enumerate(summed_table):
            summed_table[a] *= a +1
        
        sums.append(sum(summed_table))
    print(sum(sums))
            

    

