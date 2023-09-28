# Cli

Cli is a Python library to help create command-line interfaces with ease.

# Installation

```bash
pip install git+https://github.com/HashLDash/cli
```

# Usage

```python
from cli import cli

@cli("hello")
def hello():
  ''' This is a test command '''
  print("Hello, World!")

@cli("add <int:a> <int:b>")
def add(a, b):
  print(f'Adding {a} + {b} = {a+b}')
```

This would add two commands (and automagically a help command) that can be called like:

```bash
$ python command.py hello
Hello, World!
$ python command.py add 5 4
Adding 5 + 4 = 9
$ python command.py help
command.py help

    hello - This is a test command
```

You can also add shebangs, ommit the extension and link to your path to create a command for using like:

```bash
$ command hello
Hello, World!
$ command add 5 4
Adding 5 + 4 = 9
```

# TODO

This is still in development. The following is planned:
- Handling of keyword arguments
- Increase supported types

Feel free to open issues for bugs and feature requests.

PRs are welcome too!

Enjoy :)
