with open("1-1.input.txt") as f:
    lines = f.readlines()

    for line1 in lines:
        int_line1 = int(line1)
        for line2 in lines:
            int_line2 = int(line2)
            for line3 in lines:
                int_line3 = int(line3)
                summed = int_line1 + int_line2 + int_line3
                if (summed == 2020):
                    print(summed, int_line1, int_line2, int_line3)
                    print(int_line1 * int_line2 * int_line3)
