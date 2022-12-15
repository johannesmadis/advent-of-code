

with open("5-1.input.txt") as f:
    lines = f.readlines()

    seat_ids = []

    for line in lines:
        row = line[0:7].strip()
        column = line[7:10].strip()

        row = row.replace("F", "0")
        row = row.replace("B", "1")

        column = column.replace("L", "0")
        column = column.replace("R", "1")

        row_int = int(row, 2)
        col_int = int(column, 2)

        seat_id = row_int * 8 + col_int
        seat_ids.append(seat_id)

    num_seats = max(seat_ids)

    for seat in range(num_seats):
        if (seat not in seat_ids):
            print(seat)
