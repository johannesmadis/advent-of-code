with open("6-1.input.txt") as f:

    content = f.read()
    answers = content.split("\n\n")

    lengths = 0

    for group_answers in answers:
        individiual_answers = group_answers.split("\n")
        answer_obj = {}
        answer_counter = 0

        len_indi = len(individiual_answers)

        for individual_answer in individiual_answers:
            for answer in individual_answer:
                answer_obj.setdefault(answer, 0)
                answer_obj[answer] += 1
                if (answer_obj[answer] == len_indi):
                    answer_counter += 1

        lengths += answer_counter

    print(lengths)
