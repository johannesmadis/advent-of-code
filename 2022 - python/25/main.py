def decimal_to_base5(n):
    if n == 0:
        return "0"

    result = ""

    while n > 0:
        remainder = n % 5
        result = str(remainder) + result
        n = n // 5

    return result


def combine_snafu(r0, r1):
    r0_rev = r0[::-1]
    r1_rev = r1[::-1]

    result = ""

    for index, char in enumerate(r0_rev):
        result += r0_rev[index] if r1_rev[index] == "0" else r1_rev[index]

    return result[::-1]


def decimal_to_snafu(n: int):
    if n == 0:
        return "0"

    result0 = ""
    result1 = ""

    while n > 0:
        remainder = n % 5
        if remainder > 2:
            result0 = "0" + result0
            result1 = "-" + result1 if remainder == 4 else "=" + result1
            n = (n + remainder) // 5
        else:
            result0 = str(remainder) + result0
            result1 = "0" + result1
            n = n // 5

    return combine_snafu(result0, result1)


def decimal_from_snafu(snafu: str):
    # extract two numbers from input such that = becomes 2, - becomes 1 and subtract second from first in base 5
    # return base10 number
    result0 = ""
    result1 = ""
    for char in snafu:
        if char == "-":
            result0 += "0"
            result1 += "1"
        elif char == "=":
            result0 += "0"
            result1 += "2"
        else:
            result0 += char
            result1 += "0"

    return int(result0, 5) - int(result1, 5)


input_dec = 1747
snafu_decimal = decimal_to_snafu(input_dec)

snafu_num = decimal_from_snafu(snafu_decimal)


def main():
    with open("input.txt") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        total = 0
        for line in lines:
            total += decimal_from_snafu(line)

        print(decimal_to_snafu(total))


main()
