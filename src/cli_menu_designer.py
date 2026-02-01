import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import argparse
import sys
from io import StringIO
import os

class CLIMenuDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("CLI Help Menu Designer v0.4 by Leon Prieat")
        self.args = [{"name": "verbose", "flags": "-v, --verbose", "help": "Enable verbose output", "type": "flag"}]
        self.setup_ui()

    def setup_ui(self):
        # Program Details
        tk.Label(self.root, text="Program Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.prog_name = tk.Entry(self.root, width=40)
        self.prog_name.insert(0, "mycli")
        self.prog_name.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Program Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prog_desc = tk.Text(self.root, height=3, width=40)
        self.prog_desc.insert("1.0", "A sample CLI tool")
        self.prog_desc.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Column Width Slider
        tk.Label(self.root, text="Terminal Width:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.width_var = tk.IntVar(value=80)
        tk.Scale(self.root, from_=40, to=120, orient="horizontal", variable=self.width_var, command=self.update_preview).grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Arguments Frame
        self.args_frame = ttk.LabelFrame(self.root, text="Arguments", padding=10)
        self.args_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.args_entries = []

        # Buttons
        tk.Button(self.root, text="Add Argument", command=self.add_argument).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Export Code", command=self.export_code).grid(row=4, column=1, padx=5, pady=5)

        # Preview
        tk.Label(self.root, text="Help Menu Preview:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.preview = scrolledtext.ScrolledText(self.root, height=15, width=60, wrap="word")
        self.preview.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Initialize arguments UI after all widgets are created
        self.update_args_ui()

    def update_args_ui(self):
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.args_entries = []
        for i, arg in enumerate(self.args):
            frame = ttk.Frame(self.args_frame)
            frame.grid(row=i, column=0, sticky="w", pady=2)
            tk.Label(frame, text=f"Arg {i+1}:").grid(row=0, column=0, padx=2)
            name_entry = tk.Entry(frame, width=15)
            name_entry.insert(0, arg["name"])
            name_entry.grid(row=0, column=1, padx=2)
            flags_entry = tk.Entry(frame, width=15)
            flags_entry.insert(0, arg["flags"])
            flags_entry.grid(row=0, column=2, padx=2)
            help_entry = tk.Entry(frame, width=30)
            help_entry.insert(0, arg["help"])
            help_entry.grid(row=0, column=3, padx=2)
            type_combo = ttk.Combobox(frame, values=["flag", "option"], width=10)
            type_combo.set(arg["type"])
            type_combo.grid(row=0, column=4, padx=2)
            tk.Button(frame, text="Remove", command=lambda idx=i: self.remove_argument(idx)).grid(row=0, column=5, padx=2)
            self.args_entries.append((name_entry, flags_entry, help_entry, type_combo))
        self.update_preview()

    def add_argument(self):
        self.args.append({"name": "", "flags": "", "help": "", "type": "flag"})
        self.update_args_ui()

    def remove_argument(self, index):
        if len(self.args) > 1:
            self.args.pop(index)
            self.update_args_ui()

    def update_preview(self, *args):
        for i, (name_entry, flags_entry, help_entry, type_combo) in enumerate(self.args_entries):
            self.args[i] = {
                "name": name_entry.get(),
                "flags": flags_entry.get(),
                "help": help_entry.get(),
                "type": type_combo.get()
            }
        parser = argparse.ArgumentParser(
            prog=self.prog_name.get(),
            description=self.prog_desc.get("1.0", "end-1c"),
            formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=self.width_var.get())
        )
        for arg in self.args:
            if arg["flags"]:
                if arg["type"] == "flag":
                    parser.add_argument(arg["flags"], action="store_true", help=arg["help"])
                else:
                    parser.add_argument(arg["flags"], help=arg["help"])
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        parser.print_help()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", output)

    def export_code(self):
        code = f"""import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="{self.prog_name.get()}",
        description="{self.prog_desc.get('1.0', 'end-1c')}",
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, width={self.width_var.get()})
    )
"""
        for arg in self.args:
            if arg["flags"]:
                if arg["type"] == "flag":
                    code += f'    parser.add_argument("{arg["flags"]}", action="store_true", help="{arg["help"]}")\n'
                else:
                    code += f'    parser.add_argument("{arg["flags"]}", help="{arg["help"]}")\n'
        code += """    args = parser.parse_args()
    # Your code here
    print(args)

if __name__ == "__main__":
    main()
"""
        with open("cli.py", "w") as f:
            f.write(code)
        messagebox.showinfo("Export", "Code exported to cli.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = CLIMenuDesigner(root)
    root.mainloop()