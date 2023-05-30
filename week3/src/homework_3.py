#! /usr/bin/python3

def read_number(line: str, index: int):
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


def read_plus(line: str, index: int):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line: str, index: int):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line: str, index: int):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line: str, index: int):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_lparen(line: str, index: int):
    token = {'type': 'LPAREN'}
    return token, index + 1


def read_rparen(line: str, index: int):
    token = {'type': 'RPAREN'}
    return token, index + 1


def tokenize(line: str):
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
        elif line[index] == '(':
            (token, index) = read_lparen(line, index)
        elif line[index] == ')':
            (token, index) = read_rparen(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    tokens = evaluate_parentheses(tokens)
    tokens = evaluate_multiply_divide(tokens)
    answer = evaluate_add_subtract(tokens)
    return answer


def evaluate_parentheses(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'LPAREN':
            end_index = find_matching_rparen(tokens, index)
            sub_tokens = tokens[index + 1:end_index]
            result = evaluate(sub_tokens)
            tokens = tokens[:index] + [{'type': 'NUMBER', 'number': result}] + tokens[end_index + 1:]
        index += 1
    return tokens


def find_matching_rparen(tokens, start_index):
    count = 1
    index = start_index + 1
    while index < len(tokens):
        if tokens[index]['type'] == 'LPAREN':
            count += 1
        elif tokens[index]['type'] == 'RPAREN':
            count -= 1
            if count == 0:
                return index
        index += 1
    raise ValueError('Matching RPAREN not found')


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


def evaluate_add_subtract(tokens):
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


def test(line: str) -> None:
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
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
    test("(1+2)")
    test("(1+2)/3")
    test("(1+(2+3))")
    test("1+2*(1+(2+3))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)