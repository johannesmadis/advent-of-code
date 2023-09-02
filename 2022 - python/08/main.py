input_str = """30373
25512
65332
33549
35390"""


with open("C:\\Users\\kasutaja7yh\\Desktop\\aoc-2022\\08\\input.txt") as input:
    input_str = input.read().strip()

# cast 4 rays from each side
# hit threshold 0
# 
matrix = [[int(char) for char in row] for row in input_str.split("\n")]
#for line in matrix:
#   print(line)

row_count = len(matrix)
col_count = len(matrix[0])

hidden = [1]*row_count*col_count

#ray from top


for col in range(col_count):
    
    top_threshold = -1
    bottom_threshold = -1
    # ray from top, ray from bottom
    for row in range(row_count):
        test_item_top = matrix[row][col]
        test_item_bottom = matrix[-(1+row)][col]

        hidden[row*col_count + col] *= top_threshold >= test_item_top

        hidden[len(hidden) - ((1+row)*col_count) + col] *= bottom_threshold >= test_item_bottom

        if test_item_top > top_threshold:
            top_threshold = test_item_top

        if test_item_bottom > bottom_threshold:
            bottom_threshold = test_item_bottom
"""


print("")

for r in range(row_count):
    print(hidden[r*col_count:(r+1)*col_count])
"""


for row in range(row_count):

    left_threshold = -1
    right_threshold = -1

    for col in range(col_count):
        test_item_left = matrix[row][col]
        test_item_right = matrix[row][-(1+col)]

        hidden[row*col_count + col] *= left_threshold >= test_item_left
        hidden[row*col_count + (col_count - col - 1)] *= right_threshold >= test_item_right

        if test_item_left > left_threshold:
            left_threshold = test_item_left

        if test_item_right > right_threshold:
            right_threshold = test_item_right 

"""
print("")

for r in range(row_count):
    print(hidden[r*col_count:(r+1)*col_count])
"""


#print(len(hidden) - sum(hidden))


#part 2

scores = [0]*row_count*col_count
for row in range(1,row_count-1):
    for col in range(1,col_count-1):
        #up
        #down
        #left
        #right

        self_value = matrix[row][col]
        up_score = 0
        for target_row_index in range(row):
            target_item = matrix[row - target_row_index - 1][col]
            up_score += 1
            if target_item >= self_value:
                break

        down_score = 0
        for target_row_index in range(row + 1, row_count):
            target_item = matrix[target_row_index][col]
            down_score += 1
            if target_item >= self_value:
                break

        left_score = 0

        for target_col_index in range(col):
            target_item = matrix[row][col - target_col_index - 1]
            left_score +=1
            
            if (target_item >= self_value):
                break


        right_score = 0

        for target_col_index in range(col+1, col_count):
            target_item = matrix[row][target_col_index]
            right_score +=1
            
            if (target_item >= self_value):
                break
        
        index = row*col_count + col
        #print(index, up_score, left_score, right_score, down_score)


        scores[row*col_count + col] = up_score * down_score * right_score * left_score

"""
print("")

for r in range(row_count):
    print(scores[r*col_count:(r+1)*col_count])
"""
print(max(scores))


