import ast as _ast
import operator as _operator
import tkinter as tk


class Calculator(tk.Tk):
    """A simple calculator GUI built with tkinter."""

    # Maps operator display symbols to Python operator symbols
    _OP_SYMBOLS = {"+": "+", "-": "−", "*": "×", "/": "÷"}
    # Maps display symbols back to Python operators for evaluation
    _OP_MAP = {"−": "-", "×": "*", "÷": "/"}
    # Safe binary operators for expression evaluation
    _SAFE_OPS = {
        _ast.Add: _operator.add,
        _ast.Sub: _operator.sub,
        _ast.Mult: _operator.mul,
        _ast.Div: _operator.truediv,
        _ast.USub: _operator.neg,
        _ast.UAdd: _operator.pos,
    }

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg="#1c1c1e")

        # State
        self._expression = ""
        self._result_shown = False

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    def _bind_keys(self):
        """Bind keyboard shortcuts to calculator actions."""
        for digit in "0123456789":
            self.bind(digit, lambda e, d=digit: self._digit(d))
        self.bind(".", lambda e: self._decimal())
        self.bind("<Return>", lambda e: self._equals())
        self.bind("<KP_Enter>", lambda e: self._equals())
        self.bind("+", lambda e: self._operator("+"))
        self.bind("-", lambda e: self._operator("-"))
        self.bind("*", lambda e: self._operator("*"))
        self.bind("/", lambda e: self._operator("/"))
        self.bind("%", lambda e: self._percent())
        self.bind("<Escape>", lambda e: self._clear())
        self.bind("c", lambda e: self._clear())

    # ------------------------------------------------------------------ #
    #  Display                                                             #
    # ------------------------------------------------------------------ #

    def _build_display(self):
        display_frame = tk.Frame(self, bg="#1c1c1e", padx=4, pady=8)
        display_frame.pack(fill="x")

        # Secondary row – shows the running expression
        self._expr_var = tk.StringVar(value="")
        self._expr_label = tk.Label(
            display_frame,
            textvariable=self._expr_var,
            font=("Helvetica", 14),
            anchor="e",
            bg="#1c1c1e",
            fg="#8e8e93",
            padx=10,
        )
        self._expr_label.pack(fill="x")

        # Primary row – shows current input or result
        self._display_var = tk.StringVar(value="0")
        self._display = tk.Label(
            display_frame,
            textvariable=self._display_var,
            font=("Helvetica", 40, "bold"),
            anchor="e",
            bg="#1c1c1e",
            fg="white",
            padx=10,
            pady=4,
        )
        self._display.pack(fill="x")

    # ------------------------------------------------------------------ #
    #  Buttons                                                             #
    # ------------------------------------------------------------------ #

    def _build_buttons(self):
        btn_frame = tk.Frame(self, bg="#1c1c1e")
        btn_frame.pack(fill="both", expand=True)

        # Colour palette (inspired by iOS Calculator)
        DARK   = "#2c2c2e"
        LIGHT  = "#636366"
        ORANGE = "#ff9f0a"

        button_layout = [
            # (label,  col, row, colspan, bg,     fg,      command)
            ("AC",  0, 0, 1, LIGHT,  "black",  self._clear),
            ("+/-", 1, 0, 1, LIGHT,  "black",  self._toggle_sign),
            ("%",   2, 0, 1, LIGHT,  "black",  self._percent),
            ("÷",   3, 0, 1, ORANGE, "white",  lambda: self._operator("/")),
            ("7",   0, 1, 1, DARK,   "white",  lambda: self._digit("7")),
            ("8",   1, 1, 1, DARK,   "white",  lambda: self._digit("8")),
            ("9",   2, 1, 1, DARK,   "white",  lambda: self._digit("9")),
            ("×",   3, 1, 1, ORANGE, "white",  lambda: self._operator("*")),
            ("4",   0, 2, 1, DARK,   "white",  lambda: self._digit("4")),
            ("5",   1, 2, 1, DARK,   "white",  lambda: self._digit("5")),
            ("6",   2, 2, 1, DARK,   "white",  lambda: self._digit("6")),
            ("−",   3, 2, 1, ORANGE, "white",  lambda: self._operator("-")),
            ("1",   0, 3, 1, DARK,   "white",  lambda: self._digit("1")),
            ("2",   1, 3, 1, DARK,   "white",  lambda: self._digit("2")),
            ("3",   2, 3, 1, DARK,   "white",  lambda: self._digit("3")),
            ("+",   3, 3, 1, ORANGE, "white",  lambda: self._operator("+")),
            ("0",   0, 4, 2, DARK,   "white",  lambda: self._digit("0")),
            (".",   2, 4, 1, DARK,   "white",  self._decimal),
            ("=",   3, 4, 1, ORANGE, "white",  self._equals),
        ]

        for col in range(4):
            btn_frame.columnconfigure(col, weight=1, minsize=80)
        for row in range(5):
            btn_frame.rowconfigure(row, weight=1, minsize=80)

        for label, col, row, colspan, bg, fg, cmd in button_layout:
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Helvetica", 22, "bold"),
                bg=bg,
                fg=fg,
                activebackground=self._lighten(bg),
                activeforeground=fg,
                relief="flat",
                bd=0,
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

    @staticmethod
    def _lighten(hex_color: str) -> str:
        """Return a slightly lighter version of a hex colour for hover effect."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ------------------------------------------------------------------ #
    #  Display helpers                                                     #
    # ------------------------------------------------------------------ #

    @classmethod
    def _eval_expr(cls, expr: str) -> float:
        """Safely evaluate a simple arithmetic expression (no eval/exec)."""
        for display_sym, py_op in cls._OP_MAP.items():
            expr = expr.replace(display_sym, py_op)
        try:
            tree = _ast.parse(expr, mode="eval")
        except SyntaxError:
            raise ValueError(f"Invalid expression: {expr}")
        return cls._eval_node(tree.body)

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, _ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, _ast.BinOp) and type(node.op) in cls._SAFE_OPS:
            return cls._SAFE_OPS[type(node.op)](
                cls._eval_node(node.left), cls._eval_node(node.right)
            )
        if isinstance(node, _ast.UnaryOp) and type(node.op) in cls._SAFE_OPS:
            return cls._SAFE_OPS[type(node.op)](cls._eval_node(node.operand))
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    def _set_display(self, value: str):
        self._display_var.set(value)

    def _get_display(self) -> str:
        return self._display_var.get()

    def _format_number(self, value) -> str:
        """Format a number, removing unnecessary trailing decimals."""
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        # Remove excessive trailing zeros after decimal
        text = f"{value:.10g}"
        return text

    # ------------------------------------------------------------------ #
    #  Button handlers                                                     #
    # ------------------------------------------------------------------ #

    def _digit(self, digit: str):
        current = self._get_display()
        if self._result_shown:
            # Start a fresh number after a result
            self._expression = ""
            self._expr_var.set("")
            current = "0"
            self._result_shown = False

        if current == "0":
            self._set_display(digit)
        else:
            self._set_display(current + digit)

    def _decimal(self):
        current = self._get_display()
        if self._result_shown:
            self._expression = ""
            self._expr_var.set("")
            current = "0"
            self._result_shown = False

        if "." not in current:
            self._set_display(current + ".")

    def _operator(self, op: str):
        self._result_shown = False
        current = self._get_display()

        sym = self._OP_SYMBOLS.get(op, op)

        # Append current number and operator to expression
        self._expression += current + " " + sym + " "
        self._expr_var.set(self._expression)

        # Reset display for the next operand
        self._set_display("0")

    def _equals(self):
        current = self._get_display()
        full_expr = self._expression + current

        # Build the full expression string shown above
        self._expr_var.set(full_expr + " =")

        try:
            result = self._eval_expr(full_expr)
            display = self._format_number(result)
            self._set_display(display)
        except ZeroDivisionError:
            self._set_display("Error")
        except Exception:
            self._set_display("Error")

        self._expression = ""
        self._result_shown = True

    def _clear(self):
        self._expression = ""
        self._expr_var.set("")
        self._set_display("0")
        self._result_shown = False

    def _toggle_sign(self):
        current = self._get_display()
        if current not in ("0", "Error"):
            if current.startswith("-"):
                self._set_display(current[1:])
            else:
                self._set_display("-" + current)

    def _percent(self):
        current = self._get_display()
        if current == "Error":
            return
        try:
            value = float(current) / 100
            self._set_display(self._format_number(value))
        except ValueError:
            self._set_display("Error")


def main():
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
