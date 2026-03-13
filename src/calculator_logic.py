"""
计算器核心逻辑模块
支持基本四则运算、括号、负数
"""

class CalculatorLogic:
    def __init__(self):
        self.operators = ['+', '-', '*', '/']
    
    def calculate(self, expression: str) -> float:
        """
        计算表达式字符串
        """
        # 清理表达式
        expr = expression.replace(' ', '')
        
        if not expr:
            return 0
        
        try:
            # 使用 Python 安全评估
            result = self.safe_eval(expr)
            return result
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except Exception:
            # 如果无法计算，返回原表达式（用于实时预览）
            try:
                return float(expr)
            except:
                raise ValueError("Invalid expression")
    
    def safe_eval(self, expr: str) -> float:
        """
        安全地评估数学表达式
        只允许数字和基本运算符
        """
        # 验证表达式只包含允许的字符
        allowed = set('0123456789.+-*/()')
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters in expression")
        
        # 简单的表达式求值
        # 注意：生产环境应使用专门的数学表达式库
        result = eval(expr)
        return float(result)


# 简单的测试
if __name__ == "__main__":
    calc = CalculatorLogic()
    test_cases = [
        ("1+1", 2),
        ("2*3", 6),
        ("10/2", 5),
        ("(1+2)*3", 9),
    ]
    
    for expr, expected in test_cases:
        result = calc.calculate(expr)
        print(f"{expr} = {result} (expected: {expected})")
