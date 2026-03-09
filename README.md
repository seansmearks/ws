# Random Code Generator

A small CLI tool that generates random codes with options for:

- **Length** (`--length`)
- **Character set** (`--charset`) with `alphanumeric`, `numeric`, or `alphabetic`
- **Format** (`--format`) with `plain` or grouped output

It also includes a modern desktop UI mode with a dark theme, cleaner controls, and copy/clear actions.

## Usage

```bash
python3 random_code_generator.py --length 16 --charset alphanumeric --format grouped --group-length 4 --separator -
```

### Examples

Generate one numeric code with 6 digits:

```bash
python3 random_code_generator.py --length 6 --charset numeric
```

Generate 5 alphabetic codes grouped every 3 characters:

```bash
python3 random_code_generator.py --length 12 --charset alphabetic --format grouped --group-length 3 --separator : --count 5
```

Launch the desktop UI:

```bash
python3 random_code_generator.py --ui
```
