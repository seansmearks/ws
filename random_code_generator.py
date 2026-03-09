#!/usr/bin/env python3
"""Generate random codes with configurable length, character set, and output format."""

from __future__ import annotations

import argparse
import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk
from dataclasses import dataclass


CHARSET_OPTIONS = {
    "alphanumeric": string.ascii_letters + string.digits,
    "numeric": string.digits,
    "alphabetic": string.ascii_letters,
}


@dataclass(frozen=True)
class GeneratorConfig:
    length: int
    charset: str
    output_format: str
    group_length: int
    separator: str


def build_charset(charset_name: str) -> str:
    """Return the character set associated with the provided option."""
    return CHARSET_OPTIONS[charset_name]


def generate_raw_code(length: int, charset: str) -> str:
    """Generate a random code using cryptographically secure randomness."""
    return "".join(secrets.choice(charset) for _ in range(length))


def format_code(raw_code: str, output_format: str, group_length: int, separator: str) -> str:
    """Format a raw code according to the selected output format."""
    if output_format == "plain":
        return raw_code

    groups = [raw_code[i : i + group_length] for i in range(0, len(raw_code), group_length)]
    return separator.join(groups)


def generate_code(config: GeneratorConfig) -> str:
    charset = build_charset(config.charset)
    raw_code = generate_raw_code(config.length, charset)
    return format_code(raw_code, config.output_format, config.group_length, config.separator)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Random code generator")
    parser.add_argument("--ui", action="store_true", help="Launch graphical UI instead of CLI output")
    parser.add_argument("--length", type=int, default=12, help="Length of the generated code (default: 12)")
    parser.add_argument(
        "--charset",
        choices=sorted(CHARSET_OPTIONS.keys()),
        default="alphanumeric",
        help="Character set type (default: alphanumeric)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["plain", "grouped"],
        default="plain",
        help="Output format (default: plain)",
    )
    parser.add_argument(
        "--group-length",
        type=int,
        default=4,
        help="Group size when --format grouped is selected (default: 4)",
    )
    parser.add_argument(
        "--separator",
        default="-",
        help="Separator between groups when --format grouped is selected (default: -)",
    )
    parser.add_argument("--count", type=int, default=1, help="How many codes to generate (default: 1)")

    args = parser.parse_args()

    validate_numeric_args(args.length, args.group_length, args.count, parser)

    return args


def validate_numeric_args(length: int, group_length: int, count: int, parser: argparse.ArgumentParser | None = None) -> None:
    """Validate integer inputs for code generation settings."""
    errors = []
    if length <= 0:
        errors.append("Length must be a positive integer.")
    if group_length <= 0:
        errors.append("Group length must be a positive integer.")
    if count <= 0:
        errors.append("Count must be a positive integer.")

    if not errors:
        return

    if parser:
        parser.error(" ".join(errors))
    raise ValueError(" ".join(errors))


def launch_ui() -> None:
    """Launch a modern desktop UI for generating random codes."""
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        raise RuntimeError("UI mode requires a graphical environment with a display server.") from exc

    root.title("Random Code Generator")
    root.geometry("760x560")
    root.minsize(720, 520)

    bg_color = "#0f172a"
    card_color = "#111827"
    text_color = "#e5e7eb"
    muted_text_color = "#94a3b8"
    accent_color = "#6366f1"
    field_color = "#1f2937"

    root.configure(bg=bg_color)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("App.TFrame", background=bg_color)
    style.configure("Card.TFrame", background=card_color)
    style.configure("Header.TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 20, "bold"))
    style.configure("SubHeader.TLabel", background=bg_color, foreground=muted_text_color, font=("Segoe UI", 10))
    style.configure("Field.TLabel", background=card_color, foreground=text_color, font=("Segoe UI", 10, "bold"))
    style.configure(
        "App.TEntry",
        fieldbackground=field_color,
        foreground=text_color,
        insertcolor=text_color,
        bordercolor="#374151",
        lightcolor="#374151",
        darkcolor="#374151",
        padding=6,
    )
    style.configure(
        "App.TCombobox",
        fieldbackground=field_color,
        background=field_color,
        foreground=text_color,
        bordercolor="#374151",
        arrowcolor=text_color,
        lightcolor="#374151",
        darkcolor="#374151",
        padding=4,
    )
    style.map("App.TCombobox", fieldbackground=[("readonly", field_color)], foreground=[("readonly", text_color)])
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        background=accent_color,
        foreground="white",
        borderwidth=0,
    )
    style.map("Accent.TButton", background=[("active", "#4f46e5")])
    style.configure(
        "Ghost.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background="#1f2937",
        foreground=text_color,
        borderwidth=0,
    )
    style.map("Ghost.TButton", background=[("active", "#374151")])

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    length_var = tk.StringVar(value="12")
    charset_var = tk.StringVar(value="alphanumeric")
    format_var = tk.StringVar(value="plain")
    group_length_var = tk.StringVar(value="4")
    separator_var = tk.StringVar(value="-")
    count_var = tk.StringVar(value="1")

    header = ttk.Frame(root, style="App.TFrame", padding=(24, 20, 24, 8))
    header.grid(column=0, row=0, sticky="ew")
    ttk.Label(header, text="Random Code Generator", style="Header.TLabel").grid(column=0, row=0, sticky="w")
    ttk.Label(
        header,
        text="Generate secure numeric, alphabetic, or alphanumeric codes.",
        style="SubHeader.TLabel",
    ).grid(column=0, row=1, sticky="w", pady=(6, 0))

    controls_card = ttk.Frame(root, style="Card.TFrame", padding=18)
    controls_card.grid(column=0, row=1, sticky="ew", padx=24, pady=8)
    for col in range(4):
        controls_card.columnconfigure(col, weight=1)

    ttk.Label(controls_card, text="Length", style="Field.TLabel").grid(column=0, row=0, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Entry(controls_card, textvariable=length_var, width=14, style="App.TEntry").grid(column=0, row=1, sticky="ew", padx=(0, 10), pady=(0, 12))

    ttk.Label(controls_card, text="Character set", style="Field.TLabel").grid(column=1, row=0, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Combobox(
        controls_card,
        textvariable=charset_var,
        values=sorted(CHARSET_OPTIONS.keys()),
        state="readonly",
        style="App.TCombobox",
    ).grid(column=1, row=1, sticky="ew", padx=(0, 10), pady=(0, 12))

    ttk.Label(controls_card, text="Format", style="Field.TLabel").grid(column=2, row=0, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Combobox(
        controls_card,
        textvariable=format_var,
        values=["plain", "grouped"],
        state="readonly",
        style="App.TCombobox",
    ).grid(column=2, row=1, sticky="ew", padx=(0, 10), pady=(0, 12))

    ttk.Label(controls_card, text="Count", style="Field.TLabel").grid(column=3, row=0, sticky="w", pady=(0, 6))
    ttk.Entry(controls_card, textvariable=count_var, width=14, style="App.TEntry").grid(column=3, row=1, sticky="ew", pady=(0, 12))

    ttk.Label(controls_card, text="Group length", style="Field.TLabel").grid(column=0, row=2, sticky="w", padx=(0, 10), pady=(0, 6))
    group_length_input = ttk.Entry(controls_card, textvariable=group_length_var, width=14, style="App.TEntry")
    group_length_input.grid(column=0, row=3, sticky="ew", padx=(0, 10))

    ttk.Label(controls_card, text="Separator", style="Field.TLabel").grid(column=1, row=2, sticky="w", padx=(0, 10), pady=(0, 6))
    separator_input = ttk.Entry(controls_card, textvariable=separator_var, width=14, style="App.TEntry")
    separator_input.grid(column=1, row=3, sticky="ew", padx=(0, 10))

    actions = ttk.Frame(controls_card, style="Card.TFrame")
    actions.grid(column=2, row=3, columnspan=2, sticky="e")

    output_card = ttk.Frame(root, style="Card.TFrame", padding=18)
    output_card.grid(column=0, row=2, sticky="nsew", padx=24, pady=(8, 24))
    output_card.columnconfigure(0, weight=1)
    output_card.rowconfigure(1, weight=1)

    ttk.Label(output_card, text="Generated code(s)", style="Field.TLabel").grid(column=0, row=0, sticky="w", pady=(0, 8))

    output_text = tk.Text(
        output_card,
        wrap="word",
        background="#0b1220",
        foreground="#e2e8f0",
        insertbackground="#e2e8f0",
        relief="flat",
        borderwidth=0,
        highlightthickness=1,
        highlightbackground="#334155",
        padx=12,
        pady=12,
        font=("Consolas", 12),
    )
    output_text.grid(column=0, row=1, sticky="nsew")

    scrollbar = ttk.Scrollbar(output_card, orient="vertical", command=output_text.yview)
    scrollbar.grid(column=1, row=1, sticky="ns")
    output_text.configure(yscrollcommand=scrollbar.set)

    def set_group_controls_state(*_args: object) -> None:
        state = "normal" if format_var.get() == "grouped" else "disabled"
        group_length_input.configure(state=state)
        separator_input.configure(state=state)

    def handle_generate() -> None:
        try:
            length = int(length_var.get().strip())
            group_length = int(group_length_var.get().strip())
            count = int(count_var.get().strip())
            validate_numeric_args(length, group_length, count)

            config = GeneratorConfig(
                length=length,
                charset=charset_var.get(),
                output_format=format_var.get(),
                group_length=group_length,
                separator=separator_var.get(),
            )
            generated = "\n".join(generate_code(config) for _ in range(count))
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, generated)
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))

    def copy_to_clipboard() -> None:
        generated = output_text.get("1.0", tk.END).strip()
        if not generated:
            messagebox.showinfo("Nothing to copy", "Generate at least one code before copying.")
            return
        root.clipboard_clear()
        root.clipboard_append(generated)
        messagebox.showinfo("Copied", "Generated code copied to clipboard.")

    def clear_output() -> None:
        output_text.delete("1.0", tk.END)

    ttk.Button(actions, text="Clear", style="Ghost.TButton", command=clear_output).grid(column=0, row=0, padx=(0, 8))
    ttk.Button(actions, text="Copy", style="Ghost.TButton", command=copy_to_clipboard).grid(column=1, row=0, padx=(0, 8))
    ttk.Button(actions, text="Generate", style="Accent.TButton", command=handle_generate).grid(column=2, row=0)

    format_var.trace_add("write", set_group_controls_state)
    set_group_controls_state()

    root.mainloop()


def main() -> None:
    args = parse_args()

    if args.ui:
        try:
            launch_ui()
            return
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc

    config = GeneratorConfig(
        length=args.length,
        charset=args.charset,
        output_format=args.output_format,
        group_length=args.group_length,
        separator=args.separator,
    )

    for _ in range(args.count):
        print(generate_code(config))


if __name__ == "__main__":
    main()
