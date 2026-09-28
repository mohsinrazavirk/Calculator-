import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Scientific Calculator")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a1a',           # Dark background
            'display_bg': '#000000',   # Pure black display
            'display_fg': '#ffffff',   # White text
            'button_bg': '#2d2d2d',    # Dark gray buttons
            'button_fg': '#ffffff',    # White button text
            'operator_bg': '#ff9500',  # Orange operators
            'operator_fg': '#ffffff',  # White operator text
            'function_bg': '#a6a6a6',  # Light gray functions
            'function_fg': '#000000',  # Black function text
            'scientific_bg': '#4a4a4a', # Darker gray for scientific functions
            'scientific_fg': '#ffffff', # White text for scientific functions
            'hover_bg': '#404040',     # Hover effect
            'border': '#333333'        # Border color
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Variables
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.operator = ""
        self.result = False
        self.operation_display = ""  # For showing full operation
        self.first_number = ""  # Store the first number for display
        self.memory = 0  # Memory storage
        self.angle_mode = "deg"  # Degree or radian mode
        
        # Create display frame with modern styling
        self.display_frame = tk.Frame(
            self.root, 
            bg=self.colors['display_bg'], 
            height=140,
            relief=tk.FLAT,
            bd=0
        )
        self.display_frame.pack(fill=tk.X, padx=15, pady=(20, 15))
        
        # Operation display (smaller text for showing the equation)
        self.operation_display_label = tk.Label(
            self.display_frame,
            text=self.operation_display,
            font=('Segoe UI', 16, 'normal'),
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            anchor='e',
            padx=20,
            pady=10
        )
        self.operation_display_label.pack(fill=tk.X)
        
        # Main display label with modern font
        self.display = tk.Label(
            self.display_frame,
            text=self.current,
            font=('Segoe UI', 32, 'normal'),
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            anchor='e',
            padx=20,
            pady=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Create button frame with modern styling
        self.button_frame = tk.Frame(
            self.root, 
            bg=self.colors['bg'],
            padx=15,
            pady=10
        )
        self.button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for scientific calculator
        for i in range(8):  # More rows for scientific functions
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):  # More columns for scientific functions
            self.button_frame.grid_columnconfigure(i, weight=1)
        
        # Modern button configuration
        self.button_config = {
            'font': ('Segoe UI', 18, 'normal'),
            'relief': tk.FLAT,
            'bd': 0,
            'width': 3,
            'height': 1,
            'cursor': 'hand2'
        }
        
        # Create buttons
        self.create_buttons()
        
    def create_buttons(self):
        # Scientific calculator button layout
        buttons = [
            ['sin', 'cos', 'tan', 'log', 'ln', 'π'],
            ['√', 'x²', 'x³', 'x^y', '1/x', 'n!'],
            ['(', ')', 'MC', 'MR', 'MS', 'M+'],
            ['C', '±', '%', '÷', '⌫', '='],
            ['7', '8', '9', '×', 'e', 'EE'],
            ['4', '5', '6', '-', 'RAD', 'DEG'],
            ['1', '2', '3', '+', 'M-', '='],
            ['0', '.', '=', '', '', '']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # Skip empty strings
                if text == '':
                    continue
                    
                # Determine button colors based on type
                if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    bg_color = self.colors['button_bg']
                    fg_color = self.colors['button_fg']
                elif text in ['+', '-', '×', '÷', '=']:
                    bg_color = self.colors['operator_bg']
                    fg_color = self.colors['operator_fg']
                elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'x³', 'x^y', '1/x', 'n!', 'π', 'e', 'EE']:
                    bg_color = self.colors['scientific_bg']
                    fg_color = self.colors['scientific_fg']
                elif text in ['(', ')', 'MC', 'MR', 'MS', 'M+', 'M-', 'RAD', 'DEG', '⌫']:
                    bg_color = self.colors['function_bg']
                    fg_color = self.colors['function_fg']
                else:
                    bg_color = self.colors['function_bg']
                    fg_color = self.colors['function_fg']
                
                # Special case for '=' button spanning two columns
                if text == '=' and j == 2:
                    btn = tk.Button(
                        self.button_frame,
                        text=text,
                        bg=bg_color,
                        fg=fg_color,
                        activebackground=self.colors['hover_bg'],
                        command=lambda t=text: self.button_click(t),
                        **self.button_config
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky='nsew', padx=3, pady=3)
                else:
                    btn = tk.Button(
                        self.button_frame,
                        text=text,
                        bg=bg_color,
                        fg=fg_color,
                        activebackground=self.colors['hover_bg'],
                        command=lambda t=text: self.button_click(t),
                        **self.button_config
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=3, pady=3)
                
                # Add hover effects
                self.add_hover_effect(btn, bg_color)
    
    def add_hover_effect(self, button, original_color):
        """Add modern hover effects to buttons"""
        def on_enter(event):
            button.configure(bg=self.colors['hover_bg'])
        
        def on_leave(event):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def button_click(self, value):
        if value.isdigit():
            self.number_input(value)
        elif value == '.':
            self.decimal_input()
        elif value in ['+', '-', '×', '÷', '^']:
            self.operator_input(value)
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
        elif value == '⌫':
            self.backspace()
        elif value in ['sin', 'cos', 'tan']:
            self.trig_function(value)
        elif value in ['log', 'ln']:
            self.log_function(value)
        elif value == '√':
            self.square_root()
        elif value == 'x²':
            self.square()
        elif value == 'x³':
            self.cube()
        elif value == 'x^y':
            self.power()
        elif value == '1/x':
            self.reciprocal()
        elif value == 'n!':
            self.factorial()
        elif value == 'π':
            self.pi()
        elif value == 'e':
            self.euler()
        elif value in ['MC', 'MR', 'MS', 'M+', 'M-']:
            self.memory_function(value)
        elif value in ['RAD', 'DEG']:
            self.angle_mode_toggle(value)
    
    def number_input(self, num):
        if self.result:
            self.current = "0"
            self.result = False
            self.operation_display = ""
            self.first_number = ""
            self.update_operation_display()
        
        # If we have an operator and current is "0", start fresh
        if self.operator and self.current == "0":
            self.current = num
        elif self.current == "0":
            self.current = num
        else:
            self.current += num
        
        self.update_display()
    
    def decimal_input(self):
        if self.result:
            self.current = "0"
            self.result = False
        
        if '.' not in self.current:
            self.current += '.'
            self.update_display()
    
    def operator_input(self, op):
        if self.operator and not self.result:
            self.calculate()
        
        self.total = float(self.current)
        self.first_number = self.current  # Store the first number
        self.operator = op
        self.input_value = True
        self.result = False
        
        # Reset current number to start entering second number
        self.current = "0"
        
        # Update operation display
        self.operation_display = f"{self.first_number} {op}"
        self.update_operation_display()
        self.update_display()
    
    def calculate(self):
        if self.operator and not self.result:
            try:
                # Store the second number before calculation
                second_number = self.current
                
                if self.operator == '+':
                    self.total += float(self.current)
                elif self.operator == '-':
                    self.total -= float(self.current)
                elif self.operator == '×':
                    self.total *= float(self.current)
                elif self.operator == '÷':
                    if float(self.current) == 0:
                        self.current = "Error"
                        self.operation_display = ""
                        self.update_display()
                        self.update_operation_display()
                        return
                    self.total /= float(self.current)
                elif self.operator == '^':
                    self.total = self.total ** float(self.current)
                
                # Format result
                if self.total == int(self.total):
                    self.current = str(int(self.total))
                else:
                    self.current = str(self.total)
                
                # Update operation display to show complete equation
                self.operation_display = f"{self.first_number} {self.operator} {second_number} ="
                
                self.operator = ""
                self.input_value = True
                self.result = True
                self.update_display()
                self.update_operation_display()
                
            except Exception as e:
                self.current = "Error"
                self.operation_display = ""
                self.update_display()
                self.update_operation_display()
    
    def clear(self):
        self.current = "0"
        self.total = 0
        self.operator = ""
        self.input_value = True
        self.result = False
        self.operation_display = ""
        self.first_number = ""
        self.update_display()
        self.update_operation_display()
    
    def toggle_sign(self):
        if self.current != "0" and self.current != "Error":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.update_display()
    
    def percentage(self):
        try:
            self.current = str(float(self.current) / 100)
            self.update_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def update_display(self):
        # Limit display length for modern display
        if len(self.current) > 15:
            if '.' in self.current:
                self.current = self.current[:15]
            else:
                self.current = self.current[:15]
        
        # Format large numbers with commas for better readability
        try:
            if self.current != "Error" and '.' not in self.current and len(self.current) > 3:
                formatted = f"{int(self.current):,}"
                self.display.config(text=formatted)
            else:
                self.display.config(text=self.current)
        except:
            self.display.config(text=self.current)
    
    def update_operation_display(self):
        """Update the operation display line"""
        self.operation_display_label.config(text=self.operation_display)
    
    # Scientific Functions
    def backspace(self):
        """Remove last character"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def trig_function(self, func):
        """Trigonometric functions"""
        try:
            num = float(self.current)
            if self.angle_mode == "deg":
                num = math.radians(num)
            
            if func == 'sin':
                result = math.sin(num)
            elif func == 'cos':
                result = math.cos(num)
            elif func == 'tan':
                result = math.tan(num)
            
            self.current = str(result)
            self.operation_display = f"{func}({self.current})"
            self.result = True
            self.update_display()
            self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def log_function(self, func):
        """Logarithmic functions"""
        try:
            num = float(self.current)
            if num <= 0:
                self.current = "Error"
            else:
                if func == 'log':
                    result = math.log10(num)
                elif func == 'ln':
                    result = math.log(num)
                
                self.current = str(result)
                self.operation_display = f"{func}({self.current})"
                self.result = True
                self.update_display()
                self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def square_root(self):
        """Square root function"""
        try:
            num = float(self.current)
            if num < 0:
                self.current = "Error"
            else:
                result = math.sqrt(num)
                self.current = str(result)
                self.operation_display = f"√({self.current})"
                self.result = True
                self.update_display()
                self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def square(self):
        """Square function"""
        try:
            num = float(self.current)
            result = num ** 2
            self.current = str(result)
            self.operation_display = f"({self.current})²"
            self.result = True
            self.update_display()
            self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def cube(self):
        """Cube function"""
        try:
            num = float(self.current)
            result = num ** 3
            self.current = str(result)
            self.operation_display = f"({self.current})³"
            self.result = True
            self.update_display()
            self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def power(self):
        """Power function (x^y)"""
        self.operator_input('^')
    
    def reciprocal(self):
        """Reciprocal function (1/x)"""
        try:
            num = float(self.current)
            if num == 0:
                self.current = "Error"
            else:
                result = 1 / num
                self.current = str(result)
                self.operation_display = f"1/({self.current})"
                self.result = True
                self.update_display()
                self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def factorial(self):
        """Factorial function"""
        try:
            num = int(float(self.current))
            if num < 0 or num > 170:  # Limit to prevent overflow
                self.current = "Error"
            else:
                result = math.factorial(num)
                self.current = str(result)
                self.operation_display = f"{self.current}!"
                self.result = True
                self.update_display()
                self.update_operation_display()
        except:
            self.current = "Error"
            self.update_display()
    
    def pi(self):
        """Pi constant"""
        self.current = str(math.pi)
        self.operation_display = "π"
        self.result = True
        self.update_display()
        self.update_operation_display()
    
    def euler(self):
        """Euler's number"""
        self.current = str(math.e)
        self.operation_display = "e"
        self.result = True
        self.update_display()
        self.update_operation_display()
    
    def memory_function(self, func):
        """Memory functions"""
        try:
            if func == 'MC':  # Memory Clear
                self.memory = 0
            elif func == 'MR':  # Memory Recall
                self.current = str(self.memory)
                self.update_display()
            elif func == 'MS':  # Memory Store
                self.memory = float(self.current)
            elif func == 'M+':  # Memory Add
                self.memory += float(self.current)
            elif func == 'M-':  # Memory Subtract
                self.memory -= float(self.current)
        except:
            self.current = "Error"
            self.update_display()
    
    def angle_mode_toggle(self, mode):
        """Toggle between degrees and radians"""
        if mode == 'DEG':
            self.angle_mode = "deg"
        elif mode == 'RAD':
            self.angle_mode = "rad"

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
