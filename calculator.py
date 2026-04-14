# ast = Abstract Syntax Tree (Best practice for safe evaluation of user input)
import ast
import operator
import tkinter as tk


class Calculator(tk.Tk):

    # Maps UI button symbols to Python operator symbols for ease of use
    OP_SYMBOLS = {"+": "+", "-": "−", "*": "×", "/": "÷"}
    
    # Translates symbols back to Python operators to prevent errors
    OP_MAP = {"−": "-", "×": "*", "÷": "/"}
    
    # Define the operations Python is allowed to perform; using ast to prevent malicious code injection.
    SAFE_OPS = {
        ast.Add:  operator.add,
        ast.Sub:  operator.sub,
        ast.Mult: operator.mul,
        ast.Div:  operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Initialize a resizable application window and set up the UI
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(True, True)
        self.configure(bg="#3d023d")

        # Tracks the ongoing equation and whether a result is currently being displayed
        self.expression = ""
        self.result_shown = False

        # Initialize UI elements defined below
        self.build_display()
        self.build_buttons()
        self.bind_keys()


    # Maps keyboard keys to their corresponding calculator functions for convenience
    def bind_keys(self):
        for digit in "0123456789":
            self.bind(digit, lambda e, d=digit: self.digit(d))
        self.bind(".", lambda e: self.decimal())
        self.bind("<Return>", lambda e: self.equals())
        self.bind("<KP_Enter>", lambda e: self.equals())
        self.bind("+", lambda e: self.operator("+"))
        self.bind("-", lambda e: self.operator("-"))
        self.bind("*", lambda e: self.operator("*"))
        self.bind("/", lambda e: self.operator("/"))
        self.bind("%", lambda e: self.percent())
        self.bind("<Escape>", lambda e: self.clear())
        self.bind("c", lambda e: self.clear())

    # ------------------------------------------------------------------ #
    #  Display                                                           #
    # ------------------------------------------------------------------ #
   
    # Build output frame with two rows: top for stored equation, bottom for real-time input/results.
    def build_display(self):
        display_frame = tk.Frame(self, bg="#2e2e2e", padx=4, pady=8)
        display_frame.pack(fill="x")

        # Top display row - shows the stored equation
        self.expr_var = tk.StringVar(value="")
        self.expr_label = tk.Label(
            display_frame,
            textvariable=self.expr_var,
            font=("Segoe UI", 16, "bold"),
            anchor="e",
            bg="#000000",
            fg="#ADADAD",
            padx=10,
        )
        self.expr_label.pack(fill="x")

        # Bottom display row - shows real-time user input, as well as results on calculation
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Segoe UI", 40, "bold"),
            anchor="e",
            bg="#000000",
            fg="#ADADAD",
            padx=10,
            pady=4,
        )
        self.display.pack(fill="x")

    # ------------------------------------------------------------------ #
    #  Buttons                                                           #
    # ------------------------------------------------------------------ #

    # Build button grid with 5 rows and 4 columns. Color scheme inspired by Frosted Wild-Berry Pop-Tarts.
    def build_buttons(self):
        btn_frame = tk.Frame(self, bg="#000000")
        btn_frame.pack(fill="both", expand=True)

        # Color pallet for UI
        GRAY    = "#2c2c2e"
        MAGENTA = "#690b67"
        TEAL    = "#056465"

        button_layout = [
            # Format: "Label" column, row, column width, BACKGROUND COLOR, "foreground color", command
            ("AC",  0, 0, 1, TEAL,  "black",  self.clear),
            ("+/-", 1, 0, 1, TEAL,  "black",  self.toggle_sign),
            ("%",   2, 0, 1, TEAL,  "black",  self.percent),
            ("÷",   3, 0, 1, MAGENTA, "black",  lambda: self.operator("/")),
            ("7",   0, 1, 1, GRAY,   "white",  lambda: self.digit("7")),
            ("8",   1, 1, 1, GRAY,   "white",  lambda: self.digit("8")),
            ("9",   2, 1, 1, GRAY,   "white",  lambda: self.digit("9")),
            ("×",   3, 1, 1, MAGENTA, "black",  lambda: self.operator("*")),
            ("4",   0, 2, 1, GRAY,   "white",  lambda: self.digit("4")),
            ("5",   1, 2, 1, GRAY,   "white",  lambda: self.digit("5")),
            ("6",   2, 2, 1, GRAY,   "white",  lambda: self.digit("6")),
            ("−",   3, 2, 1, MAGENTA, "black",  lambda: self.operator("-")),
            ("1",   0, 3, 1, GRAY,   "white",  lambda: self.digit("1")),
            ("2",   1, 3, 1, GRAY,   "white",  lambda: self.digit("2")),
            ("3",   2, 3, 1, GRAY,   "white",  lambda: self.digit("3")),
            ("+",   3, 3, 1, MAGENTA, "black",  lambda: self.operator("+")),
            ("0",   0, 4, 2, GRAY,   "white",  lambda: self.digit("0")),
            (".",   2, 4, 1, GRAY,   "white",  self.decimal),
            ("=",   3, 4, 1, MAGENTA, "black",  self.equals),
        ]

        # Ensure even spacing on window resize
        for col in range(4):
            btn_frame.columnconfigure(col, weight=1, minsize=80)
        for row in range(5):
            btn_frame.rowconfigure(row, weight=1, minsize=80)

        # Create some snazzy-ass buttons
        for label, col, row, colspan, bg, fg, cmd in button_layout:
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Segoe UI", 18),
                bg=bg,
                fg=fg,
                activebackground=self.lighten(bg),
                activeforeground=fg,
                relief="raised",
                bd=2,
                cursor="hand2",
                command=cmd,
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                sticky="nsew",
                padx=2,
                pady=2,
            )

    # Fade color on button press
    @staticmethod
    def lighten(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ------------------------------------------------------------------ #
    #  Display helpers                                                   #
    # ------------------------------------------------------------------ #

    # Convert display symbols and evaluate the expression safely.
    @classmethod
    def evalexpr(cls, expr: str) -> float:
        for display_sym, py_op in cls.OP_MAP.items():
            expr = expr.replace(display_sym, py_op)
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError:
            raise ValueError(f"Invalid expression: {expr}")
        return cls.eval_node(tree.body)

    # Recursively ensure AST protocol compliance.
    @classmethod
    def eval_node(cls, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in cls.SAFE_OPS:
            try:
                return cls.SAFE_OPS[type(node.op)](
                    cls.eval_node(node.left), cls.eval_node(node.right)
                )
            except ArithmeticError as exc:
                raise ValueError("Invalid arithmetic operation in expression") from exc
        if isinstance(node, ast.UnaryOp) and type(node.op) in cls.SAFE_OPS:
            return cls.SAFE_OPS[type(node.op)](cls.eval_node(node.operand))
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    # Update the main display.
    def set_display(self, value: str):
        self.display_var.set(value)

    # Fetch the current main display readout.
    def get_display(self) -> str:
        return self.display_var.get()

    # Remove excess zeros after decimal point
    def format_number(self, value) -> str:
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        text = f"{value:.10g}"
        return text

    # ------------------------------------------------------------------ #
    #  Button handlers                                                   #
    # ------------------------------------------------------------------ #

    # Check number in display - if result is currently shown, reset expression and start new one with this digit
    def digit(self, digit: str):
        current = self.get_display()
        if self.result_shown:
            self.expression = ""
            self.expr_var.set("")
            current = "0"
            self.result_shown = False

        # Replace the initial 0, otherwise append to keep building the number.
        if current == "0":
            self.set_display(digit)
        else:
            self.set_display(current + digit)

    # Add a decimal point once per number, and start fresh after a result.
    def decimal(self):
        current = self.get_display()
        if self.result_shown:
            self.expression = ""
            self.expr_var.set("")
            current = "0"
            self.result_shown = False

        if "." not in current:
            self.set_display(current + ".")

    # Store the current number with an operator, then wait for the next number.
    def operator(self, op: str):
        self.result_shown = False
        current = self.get_display()

        sym = self.OP_SYMBOLS.get(op, op)

        # Append current number and operator to expression
        self.expression += current + " " + sym + " "
        self.expr_var.set(self.expression)

        # Reset display for the next operand
        self.set_display("0")

    # Evaluate the full expression and show either the result or an error.
    def equals(self):
        current = self.get_display()
        fullexpr = self.expression + current

        # Build the full expression string shown above
        self.expr_var.set(fullexpr + " =")

        try:
            result = self.evalexpr(fullexpr)
            display = self.format_number(result)
            self.set_display(display)
        except ZeroDivisionError:
            self.set_display("Error")
        except Exception:
            self.set_display("Error")

        self.expression = ""
        self.result_shown = True

    # UI Reset - Clear the current expression and reset the display to 0.
    def clear(self):
        self.expression = ""
        self.expr_var.set("")
        self.set_display("0")
        self.result_shown = False

    # +/- Logic - Flip the sign of the current value (positive <-> negative).
    def toggle_sign(self):
        current = self.get_display()
        if current not in ("0", "Error"):
            if current.startswith("-"):
                self.set_display(current[1:])
            else:
                self.set_display("-" + current)

    # % Logic - Convert the current value to a percentage by dividing by 100.
    def percent(self):
        current = self.get_display()
        if current == "Error":
            return
        try:
            value = float(current) / 100
            self.set_display(self.format_number(value))
        except ValueError:
            self.set_display("Error")

# Create and run the calculator window.
def main():
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
