import math

class Calculator:
    _id_counter = 1

    def __init__(self):
        self.id = Calculator._id_counter
        Calculator._id_counter += 1
        self.stack = []
    
    #계산기 객체가 생성될 때마다 새로운 ID 부여 계산을 위해 스택을 초기화

    def __del__(self):
        pass

    def push(self, value):
        self.stack.append(value)

    #스택에 값을 추가하는 역할

    def pop(self):
        if not self.stack:
            raise Exception("스택이 비어있습니다")
        return self.stack.pop()
    
    #스택에서 값을 제거하고 추가하는 역할

    def peek(self):
        if not self.stack:
            raise Exception("스택이 비어있습니다")
        return self.stack[-1]
    
    #스택에서 값을 제거하지 않고 조회하는 역할

    def perform_operation(self, operator):
        if len(self.stack) < 2:
            raise Exception("스택이 충분하지 않습니다")
        b = self.pop()
        a = self.pop()
        if operator == '+':
            self.push(a + b)
        elif operator == '-':
            self.push(a - b)
        elif operator == '*':
            self.push(a * b)
        elif operator == '/':
            if b == 0:
                raise Exception("0으로 나눌 수 없습니다")
            self.push(a / b)
        else:
            raise Exception("지원하지 않는 연산입니다")

    #스택에서 숫자를 팝하여 주어진 연산자를 수행하고 다시 스택에 결과를 푸시

    def evaluate(self, expression):
        if expression.count('(') != expression.count(')'):
            raise Exception("괄호의 쌍이 맞지 않습니다")

        tokens = expression.split()
        for token in tokens:
            if token in '+-*/':
                self.perform_operation(token)
            elif token == '(':
                self.push(token)
            elif token == ')':
                while self.peek() != '(':
                    self.perform_operation(self.pop())
                self.pop()
            else:
                self.push(float(token))

        if len(self.stack) != 1:
            raise Exception("수식이 유효하지 않습니다")
        return self.pop()

    #수식의 괄호와 연산자가 올바르게 입력되었는지를 판단

class EngineerCalculator(Calculator):
    def __init__(self):
        super().__init__()
    
    def tokenize(self, expression):
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i] in '()+-*/':
                tokens.append(expression[i])
                i += 1
            elif expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
            elif i + 3 <= len(expression) and expression[i:i+3] in ['sin', 'cos', 'tan']:
                tokens.append(expression[i:i+3])
                i += 3
            else:
                raise Exception(f"Invalid character found: {expression[i]}")
                i += 1
        return tokens
    
    #수식을 토큰으로 분리하여 반환하는 역할 수행

    def perform_operation(self, operator):
        if operator in ['sin', 'cos', 'tan']:
            if not self.stack:
                raise Exception("스택이 비어 있습니다.")
            angle = self.pop()
            if operator == 'sin':
                self.push(math.sin(math.radians(angle)))
            elif operator == 'cos':
                self.push(math.cos(math.radians(angle)))
            elif operator == 'tan':
                self.push(math.tan(math.radians(angle)))
        else:
            super().perform_operation(operator)
    
    #공학용 계산기에서 삼각함수를 처리하고, 그외의 연산은 기본 계산기에서 처리

    def evaluate(self, expression):
        if expression.count('(') != expression.count(')'):
            raise Exception("괄호의 쌍이 맞지 않습니다.")

        tokens = self.tokenize(expression)

        for token in tokens:
            if token in '+-*/':
                self.perform_operation(token)
            elif token in ['sin', 'cos', 'tan']:
                if len(self.stack) < 1:
                    raise Exception("스택이 충분하지 않습니다")
                self.perform_operation(token)
            elif token == '(':
                self.push(token)
            elif token == ')':
                top = self.peek()
                while top != '(':
                    self.perform_operation(self.pop())
                    top = self.peek()
                self.pop()
            else:
                self.push(float(token))

        if len(self.stack) != 1:
            raise Exception("수식이 유효하지 않습니다.")
        return self.pop()

    def factorial(self, n):
        if n < 0:
            raise ValueError("음수에 대한 팩토리얼은 정의되지 않습니다.")
        if n == 0 or n == 1:
            return 1
        else:
            return n * self.factorial(n - 1)

    #팩토리얼을 재귀적으로 계산하는 역할

def get_expression_from_user():
    return input("계산할 수식을 입력하세요: ")

def calculate_user_input():
    try:
        user_expression = get_expression_from_user()
        calculator = EngineerCalculator()
        result = calculator.evaluate(user_expression)
        print(f"계산된 결과: {result}")
        calculator.last_result = result
    except Exception as e:
        print(f"오류: {e}")

calculate_user_input()