import flet as ft
from calculator_logic import CalculatorLogic
import json
import os

# 历史记录存储文件
HISTORY_FILE = "history.json"

class CalculatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.logic = CalculatorLogic()
        self.history = self.load_history()
        
        # 主题配置
        self.is_dark = False
        self.current_theme = self.get_light_theme()
        
        # 表达式和结果显示
        self.expression = ""
        self.result = "0"
        
        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        self.page.title = "FletCalc"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_full_screen = True
        self.page.update()
    
    def get_light_theme(self):
        return {
            "bg": "#FFFFFF",
            "display_bg": "#F5F5F5",
            "display_text": "#000000",
            "operator": "#FF9500",
            "operator_text": "#FFFFFF",
            "number": "#F0F0F0",
            "number_text": "#000000",
            "function": "#A0A0A0",
            "function_text": "#000000",
            "equal": "#FF9500",
            "equal_text": "#FFFFFF",
        }
    
    def get_dark_theme(self):
        return {
            "bg": "#1C1C1E",
            "display_bg": "#2C2C2E",
            "display_text": "#FFFFFF",
            "operator": "#FF9500",
            "operator_text": "#FFFFFF",
            "number": "#3A3A3C",
            "number_text": "#FFFFFF",
            "function": "#5A5A5A",
            "function_text": "#FFFFFF",
            "equal": "#FF9500",
            "equal_text": "#FFFFFF",
        }
    
    def toggle_theme(self, e):
        self.is_dark = not self.is_dark
        self.page.theme_mode = ft.ThemeMode.DARK if self.is_dark else ft.ThemeMode.LIGHT
        self.current_theme = self.get_dark_theme() if self.is_dark else self.get_light_theme()
        self.build_ui()
    
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f)
    
    def add_to_history(self, expr, result):
        self.history.insert(0, {"expression": expr, "result": result})
        if len(self.history) > 10:
            self.history = self.history[:10]
        self.save_history()
    
    def on_button_click(self, value):
        if value == "C":
            self.expression = ""
            self.result = "0"
        elif value == "CE":
            self.expression = ""
            self.result = "0"
        elif value == "⌫":
            self.expression = self.expression[:-1]
            if not self.expression:
                self.result = "0"
            else:
                try:
                    self.result = str(self.logic.calculate(self.expression))
                except:
                    pass
        elif value == "=":
            if self.expression:
                try:
                    self.result = str(self.logic.calculate(self.expression))
                    self.add_to_history(self.expression, self.result)
                    self.expression = self.result
                except Exception as e:
                    self.result = "Error"
        elif value == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
        elif value == "%":
            try:
                val = float(self.expression)
                self.result = str(val / 100)
                self.expression = self.result
            except:
                pass
        elif value == "History":
            self.show_history()
        elif value == "Theme":
            self.toggle_theme(None)
        else:
            self.expression += value
            try:
                self.result = str(self.logic.calculate(self.expression))
            except:
                pass
        
        self.update_display()
    
    def update_display(self):
        self.display.value = self.expression if self.expression else "0"
        self.result_display.value = self.result
        self.page.update()
    
    def show_history(self):
        history_text = "\n".join([f"{h['expression']} = {h['result']}" for h in self.history]) if self.history else "暂无记录"
        
        dialog = ft.AlertDialog(
            title=ft.Text("计算历史"),
            content=ft.Text(history_text, selectable=True),
            actions=[ft.TextButton("关闭", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def create_button(self, text, bg_color, text_color, width=80, height=60, on_click=None):
        return ft.Container(
            content=ft.Text(text, size=24, weight=ft.FontWeight.W500, color=text_color),
            width=width,
            height=height,
            bgcolor=bg_color,
            border_radius=50,
            alignment=ft.alignment.center,
            on_click=on_click,
        )
    
    def build_ui(self):
        # 显示区域
        self.display = ft.Text(
            self.expression if self.expression else "0",
            size=32,
            color=self.current_theme["display_text"],
            text_align=ft.TextAlign.RIGHT,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        self.result_display = ft.Text(
            self.result,
            size=48,
            weight=ft.FontWeight.BOLD,
            color=self.current_theme["display_text"],
            text_align=ft.TextAlign.RIGHT,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        display_container = ft.Container(
            content=ft.Column([
                ft.Container(content=self.display, alignment=ft.alignment.center_right, padding=10),
                ft.Container(content=self.result_display, alignment=ft.alignment.center_right, padding=10),
            ]),
            bgcolor=self.current_theme["display_bg"],
            height=180,
            padding=20,
        )
        
        # 按钮布局
        buttons = [
            # 第一行
            [("C", "function"), ("CE", "function"), ("%", "function"), ("⌫", "function")],
            # 第二行
            [("7", "number"), ("8", "number"), ("9", "number"), ("/", "operator")],
            # 第三行
            [("4", "number"), ("5", "number"), ("6", "number"), ("*", "operator")],
            # 第四行
            [("1", "number"), ("2", "number"), ("3", "number"), ("-", "operator")],
            # 第五行
            [("±", "function"), ("0", "number"), (".", "number"), ("+", "operator")],
            # 第六行
            [("History", "function"), ("=", "equal"), ("Theme", "function")],
        ]
        
        button_rows = []
        for row in buttons:
            row_controls = []
            for btn_text, btn_type in row:
                if btn_type == "operator":
                    bg = self.current_theme["operator"]
                    color = self.current_theme["operator_text"]
                elif btn_type == "equal":
                    bg = self.current_theme["equal"]
                    color = self.current_theme["equal_text"]
                elif btn_type == "function":
                    bg = self.current_theme["function"]
                    color = self.current_theme["function_text"]
                else:
                    bg = self.current_theme["number"]
                    color = self.current_theme["number_text"]
                
                row_controls.append(
                    self.create_button(btn_text, bg, color, on_click=lambda e, v=btn_text: self.on_button_click(v))
                )
            button_rows.append(
                ft.Row(row_controls, spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            )
        
        buttons_container = ft.Column(
            button_rows,
            spacing=10,
            expand=True,
        )
        
        # 主界面
        self.page.controls = [
            ft.Container(
                content=ft.Column([
                    display_container,
                    ft.Container(content=buttons_container, padding=10, expand=True),
                ]),
                bgcolor=self.current_theme["bg"],
                expand=True,
            )
        ]
        self.page.update()


def main(page: ft.Page):
    CalculatorApp(page)


if __name__ == "__main__":
    ft.app(target=main)
