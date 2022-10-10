from typing import List


def tokenize(text: str):
    text = '(' + text + ')'
    token: List[str] = []
    for char in text:
        if char in "0123456789":
            token.append(char)
        elif char in " +-*/()":
            if token:
                yield int("".join(token))
                token: List[str] = []
            if char != " ":
                yield char
        else:
            raise ValueError
    if token:
        yield int("".join(token))


async def evaluate(tokens: str):
    stack = []
    for token in tokens:
        if token == ")":
            lb, lhs, op, rhs = stack[-4:]
            del stack[-4:]
            if lb != "(":
                raise ValueError
            if op == '-':
                token = lhs - rhs
            elif op == '+':
                token = lhs + rhs
            elif op == '*':
                token = lhs * rhs
            elif op == '/':
                token = lhs / rhs
        stack.append(token)
    return stack[-1]
