from __init__ import cli

@cli('lol')
def show(**kwargs):
    print(kwargs)
