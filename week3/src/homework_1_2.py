#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_multiply_divide(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLY':
            tokens[index - 1]['number'] *= tokens[index + 1]['number']
            del tokens[index:index+2]
        elif tokens[index]['type'] == 'DIVIDE':
            if tokens[index + 1]['number'] == 0:
                print("Error: Not divisible by 0")
                exit(1)
            tokens[index - 1]['number'] /= tokens[index + 1]['number']
            del tokens[index:index+2]
        else:
            index += 1
    return tokens


def evaluate_plus_minus(tokens):
    answer = tokens[0]['number']
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'PLUS':
            answer += tokens[index + 1]['number']
            index += 2
        elif tokens[index]['type'] == 'MINUS':
            answer -= tokens[index + 1]['number']
            index += 2
        else:
            print('Invalid syntax')
            exit(1)
    return answer


def test(line):
    tokens = tokenize(line)
    new_tokens = evaluate_multiply_divide(tokens)
    actual_answer = evaluate_plus_minus(new_tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("2*3")
    test("2/3")
    test("2*3/2")
    test("1+2/3")
    test("2/3+1")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    print(tokens)
    new_tokens = evaluate_multiply_divide(tokens)
    print(new_tokens)
    answer = evaluate_plus_minus(new_tokens)
    print("answer = %f\n" % answer)