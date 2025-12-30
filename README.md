# tree-sitter-builder

A CLI tool to clone, build, and manage tree-sitter language parsers.

## Features

- Clone tree-sitter grammar repositories from GitHub or any Git URL
- Build parser shared libraries automatically
- Manage multiple grammars with simple commands
- XDG-compliant directory structure

## Requirements

- Python 3.11+

## Installation

Using [pipx](https://pypa.github.io/pipx/) (recommended):

```bash
pipx install tree-sitter-builder
```

Using pip:

```bash
pip install tree-sitter-builder
```

## Usage

### Build a parser

Clone a repository and build the tree-sitter language parser:

```bash
tree-sitter-builder build conao3/tree-sitter-sql
```

You can also specify a full Git URL:

```bash
tree-sitter-builder build https://github.com/tree-sitter/tree-sitter-python
```

Repositories are cloned to `$XDG_DATA_HOME/tree-sitter-builder/repos/`.

To rebuild all existing parsers:

```bash
tree-sitter-builder build
```

### Get parser path

Retrieve the path to the built shared library:

```bash
tree-sitter-builder dist conao3/tree-sitter-sql
# Output: /home/user/.local/share/tree-sitter-builder/build/conao3__tree-sitter-sql.so
```

### Update repositories

Pull the latest changes for all cloned repositories:

```bash
tree-sitter-builder update
```

### List repositories

Show all managed repositories:

```bash
tree-sitter-builder list
```

### Remove a repository

Delete a specific repository and its build artifacts:

```bash
tree-sitter-builder remove conao3/tree-sitter-sql
```

### Clean build files

Remove all built shared libraries:

```bash
tree-sitter-builder clean
```

## License

Apache-2.0
