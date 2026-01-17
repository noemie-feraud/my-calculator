"""
domain/engine.py

Goal:
- Evaluate a text expression WITHOUT eval() and WITHOUT math.

Method (classic + easy to explain):
1) tokenize: turns "2+3*4" -> [2.0, '+', 3.0, '*', 4.0]
   - supports: sqrt( abs( inv( !
   - supports: unary minus (token "u-")
2) to_rpn: shunting-yard -> Reverse Polish Notation (RPN)
3) eval_rpn: computes the stack

Supported operations:
- + - * / % ^
- parentheses
- u- (unary minus)
- sqrt, abs, inv
- ! (postfix factorial)
"""

from typing import List, Tuple, Union, Optional
from domain.scientific import pow_int, sqrt_newton, factorial_int, abs_value, inv_value, mod_int

Token = Union[str, float]


def evaluate_expression(expr: str) -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Returns (success, value, error_code).
    """
    tokens = tokenize(expr)
    if tokens is None:
        return False, None, "TOKEN_ERROR"

    rpn = to_rpn(tokens)
    if rpn is None:
        return False, None, "PARSE_ERROR"

    ok, value, err = eval_rpn(rpn)
    if not ok:
        return False, None, err

    return True, value, None


def tokenize(expr: str) -> Optional[List[Token]]:
    """
    Read the expression character by character.
    Recognizes:
    - numbers (float)
    - operators
    - parentheses
    - sqrt( abs( inv(
    - postfix !
    - unary minus "u-"
    """
    tokens: List[Token] = []
    i = 0
    n = len(expr)

    def last_is_operator_or_open_paren() -> bool:
        if not tokens:
            return True
        last = tokens[-1]
        return isinstance(last, str) and last in {"+", "-", "*", "/", "%", "^", "u-", "("}

    while i < n:
        c = expr[i]

        if c.isspace():
            i += 1
            continue

        # functions
        if expr.startswith("sqrt(", i):
            tokens.append("sqrt")
            tokens.append("(")
            i += len("sqrt(")
            continue

        if expr.startswith("abs(", i):
            tokens.append("abs")
            tokens.append("(")
            i += len("abs(")
            continue

        if expr.startswith("inv(", i):
            tokens.append("inv")
            tokens.append("(")
            i += len("inv(")
            continue

        # Number (with a decimal point)
        if c.isdigit() or c == ".":
            j = i
            dot_count = 0
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        return None
                j += 1

            part = expr[i:j]
            if part == ".":
                return None

            try:
                tokens.append(float(part))
            except ValueError:
                return None

            i = j
            continue

        # parentheses
        if c in {"(", ")"}:
            tokens.append(c)
            i += 1
            continue

        # factorial
        if c == "!":
            tokens.append("!")
            i += 1
            continue

        # opérators
        if c in {"+", "-", "*", "/", "%", "^"}:
            if c == "-" and last_is_operator_or_open_paren():
                tokens.append("u-")
            else:
                tokens.append(c)
            i += 1
            continue

        # unknown
        return None

    return tokens


def precedence(op: str) -> int:
    """Priorities"""
    if op == "!":
        return 5
    if op in {"u-", "sqrt", "abs", "inv"}:
        return 4
    if op == "^":
        return 3
    if op in {"*", "/", "%"}:
        return 2
    if op in {"+", "-"}:
        return 1
    return 0


def is_right_associative(op: str) -> bool:
    """Right associativity for ^ and u-"""
    return op in {"^", "u-"}


def is_operator(tok: Token) -> bool:
    return isinstance(tok, str) and tok in {"+", "-", "*", "/", "%", "^", "u-", "!"}


def is_function(tok: Token) -> bool:
    return isinstance(tok, str) and tok in {"sqrt", "abs", "inv"}


def to_rpn(tokens: List[Token]) -> Optional[List[Token]]:
    """
    Shunting-yard : tokens -> RPN
    """
    output: List[Token] = []
    stack: List[str] = []

    for tok in tokens:
        if isinstance(tok, float):
            output.append(tok)
            continue

        if isinstance(tok, str) and is_function(tok):
            stack.append(tok)
            continue

        if isinstance(tok, str) and is_operator(tok):
            while stack:
                top = stack[-1]
                if top == "(":
                    break

                if is_function(top) or is_operator(top):
                    if precedence(top) > precedence(tok):
                        output.append(stack.pop())
                        continue

                    if precedence(top) == precedence(tok) and not is_right_associative(tok):
                        output.append(stack.pop())
                        continue

                break

            stack.append(tok)
            continue

        if tok == "(":
            stack.append("(")
            continue

        if tok == ")":
            found_open = False
            while stack:
                top = stack.pop()
                if top == "(":
                    found_open = True
                    break
                output.append(top)

            if not found_open:
                return None

            # If a function is right before it, we put it into the output.
            if stack and is_function(stack[-1]):
                output.append(stack.pop())

            continue

        return None

    # Clear the stack
    while stack:
        top = stack.pop()
        if top in {"(", ")"}:
            return None
        output.append(top)

    return output


def eval_rpn(rpn: List[Token]) -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Evaluate an RPN expression using a stack.
    """
    stack: List[float] = []

    for tok in rpn:
        if isinstance(tok, float):
            stack.append(tok)
            continue

        # unary minus
        if tok == "u-":
            if len(stack) < 1:
                return False, None, "BAD_UNARY_MINUS"
            a = stack.pop()
            stack.append(-a)
            continue

        # Binary operators
        if tok in {"+", "-", "*", "/", "%", "^"}:
            if len(stack) < 2:
                return False, None, "BAD_BINARY_OP"
            b = stack.pop()
            a = stack.pop()

            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            elif tok == "/":
                if b == 0:
                    return False, None, "DIV_ZERO"
                stack.append(a / b)
            elif tok == "%":
                res = mod_int(a, b)
                if res is None:
                    return False, None, "MOD_ERROR"
                stack.append(res)
            elif tok == "^":
                res = pow_int(a, b)
                if res is None:
                    if a == 0 and b < 0:
                        return False, None, "POW_ZERO_NEG"
                    return False, None, "POW_EXP_NOT_INT"
                stack.append(res)
            continue

        # factorial
        if tok == "!":
            if len(stack) < 1:
                return False, None, "FACTORIAL_NO_ARG"
            a = stack.pop()
            res = factorial_int(a)
            if res is None:
                return False, None, "FACTORIAL_NOT_INT"
            stack.append(res)
            continue

        # functions
        if tok == "sqrt":
            if len(stack) < 1:
                return False, None, "SQRT_NO_ARG"
            a = stack.pop()
            res = sqrt_newton(a)
            if res is None:
                return False, None, "SQRT_NEGATIVE"
            stack.append(res)
            continue

        if tok == "abs":
            if len(stack) < 1:
                return False, None, "ABS_NO_ARG"
            a = stack.pop()
            stack.append(abs_value(a))
            continue

        if tok == "inv":
            if len(stack) < 1:
                return False, None, "INV_NO_ARG"
            a = stack.pop()
            res = inv_value(a)
            if res is None:
                return False, None, "INV_ZERO"
            stack.append(res)
            continue

        return False, None, "EVAL_ERROR"

    if len(stack) != 1:
        return False, None, "EVAL_ERROR"

    return True, stack[0], None
