import sys
import atexit
import os
import builtins
import traceback

__version__ = '0.0.4'

route = [r for r in sys.argv[1:] if not r.startswith('-')]
flags = [flag for flag in sys.argv[1:] if flag.startswith('-')]

if len(route) == 0:
    route = ['help']

def cli_help():
    print(f'{sys.argv[0]} help')
    print()
    for route in routes:
        if 'doc' in routes[route]:
            print(f'    {route} - {routes[route]["doc"].strip()}')
                
routes = {
    'help':{'func':cli_help},
    '-h':{'func':cli_help},
    '--help':{'func':cli_help},
}

def cli(route, methods=None):
    def decorator(f):
        def wrapped(*args, **kwargs):
            try:
                resp = f(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc().replace('"', '\"').replace("'", "\'")
                print(tb, file=sys.stderr)
                return
        routes[route] = {'func':wrapped}
        if f.__doc__:
            routes[route]['doc'] = f.__doc__
        return wrapped
    return decorator

def cast(part, varType):
    varType = varType.replace('string', 'str')
    if varType in builtins.__dict__:
        return getattr(builtins, varType)(part)
    raise TypeError

def isCompatible(pattern, part):
    if pattern.startswith('<') and pattern.endswith('>'):
        if ':' in pattern:
            *varType, var = pattern[1:-1].split(':')
            if varType[0] == 'path':
                return True, var, part
            try:
                return True, var, cast(part, varType[0])
            except TypeError:
                return None
        else:
            return True
    elif pattern == part:
        return True
    return None

def checkArgsLen(command, pattern, variables):
    if len(command) == len(pattern):
        return True
    return False

def parseRoute(pattern, command):
    pattern = pattern.split(' ')
    path = ''
    offset = 0
    variables = {}
    for n, part in enumerate(pattern):
        if '"' in part:
            offset = len(command)-len(pattern)
            if offset >= 0:
                *varType, var = part[1:-1].split(':')
                variables[var] = ' '.join(command[n:n+offset+1])
            else:
                # Route is not compatible
                return None, None
        else:
            result = isCompatible(part, command[n+offset])
            if result is None:
                # Route is not compatible
                return None, None
            else:
                if result is not True and len(result) > 1:
                    variables[result[1]] = result[2]
            # yep, proceed
            continue
    if checkArgsLen(command, pattern, variables):
        # Route {pattern} is compatible with {command}
        return variables, ' '.join(pattern)
    return None, None

def run():
    global route
    variables = {}
    kwargs = {}
    for arg in route.copy():
        if '=' in arg:
            name, val = arg.split('=')
            kwargs[name.strip()] = val.strip()
            route.remove(arg) 
    if not ' '.join(route) in routes:
        for r in routes:
            variables, rule = parseRoute(r, route)
            if rule is not None:
                route = rule
                break
        else:
            print('Invalid command.')
            return
    else:
        route = ' '.join(route)
    try:
        if kwargs:
            routes[route]['func'](**variables, **kwargs)
        else:
            routes[route]['func'](**variables)
    except SystemExit as e:
        atexit.set_exit_code = e

atexit.register(run)
