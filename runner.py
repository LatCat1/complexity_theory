import sys
from collections import defaultdict


def parse_state_map(s: str, verbose=False):
    m = {}
    
    lines = [
        l.split("//")[0] for l in s.split('\n')
    ]
    lines = [l for l in lines if not l.isspace() and l != ""]
    name = lines[0].split(':')[1][1:]
    init = lines[1].split(':')[1][1:]
    accept = lines[2].split(':')[1][1:]

    if verbose:
        print(f"--- {name} ---")

    i = 3
    while i < len(lines): 
        # whitespace ignore
        if lines[i].isspace():
            i += 1
            continue
        # so its not just whitespace. so we have data
        a = lines[i].split(',')
        b = lines[i+1].split(',')
        if a[0] not in m:
            m[a[0]] = {}
        m[a[0]][a[1][0]] = (b[0],b[1],b[2])
        i = i + 2
    return ((init, accept), m)

def parse_tape_init(s: str):
    tape = defaultdict(lambda *args, **kwargs: '_')
    for i in range(len(s)):
        tape[i] = s[i]
    return tape

def transition(loc: int, state, tape, state_map):
    (new_state,new_symbol,move) = state_map[state][tape[loc]]
    tape[loc] = new_symbol
    if move == ">":
        loc += 1
    elif move == "<":
        loc -= 1
    return (loc, new_state)
    

MAXSTEPS = 10000

def print_tape(tape):
    s = min(i for i in tape if tape[i] != "_")
    e = max(i for i in tape if tape[i] != "_")
    s = min(s, loc)
    e = max(e, loc)
    for i in range(s,e+1):
        print(tape[i], end="")
    print()
    print(" "*(loc-s)+"^")

# Gives a string reprentation of the 
# output of "tape", excluding leading
# and trailing blanks
def tape_to_string(tape):
    s = min(i for i in tape if tape[i] != "_")
    e = max(i for i in tape if tape[i] != "_")
    s = ''.join(tape[i] for i in range(s, e+1))
    return s


def run_turing(code: str, init: str, verbose=False): 
    ((state, accept), state_map) = parse_state_map(code,verbose)
    tape = parse_tape_init(init)
    loc = 0

    for i in range(MAXSTEPS):
        if verbose:
            print(f"Step {i}: {state}")
            print_tape(tape)
            print()
        if state == accept:
            if verbose:
                print(f"Accepted in {i} steps. Final tape state:")
                print_tape(tape)
            return (True, tape)

        try:
            (loc, state) = transition(loc, state, tape, state_map)
        except Exception as e:
            if verbose:
                print(f"Rejected in {i} steps")
            return (False, tape)
    raise Exception("Failure to terminate within {MAXSTEPS}")

if __name__ == "__main__":
    f_name = sys.argv[1]
    init = sys.argv[2]
    verbose = False
    if len(sys.argv) >= 4:
        verbose = sys.argv[3] == "verbose=true"

    with open(f_name) as f:
        code = f.read()
    
    run_turing(code, init, verbose=verbose)
