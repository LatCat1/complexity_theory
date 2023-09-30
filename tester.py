from runner import run_turing, tape_to_string
from random import randint


# for a large(ish?) number of inputs
# sampled from input_generator, checks
# that the turing code matches f
def test_machine(input_generator, turing_code, f, iters=1000,verbose=False):
    for i in range(iters):
        inp = input_generator()
        (accept, tape) = run_turing(turing_code, inp)
        x = f(inp)
        # if x is a tuple, we check tape state
        if type(x) is tuple:
            assert(len(x)) == 2, "f has wrong return type"
            assert accept == x[0], f"Acceptance mismatch on {inp}"
            assert tape_to_string(tape) == x[1], f"Tape mismatch on {inp}"
        else:
            assert accept == x, f"Acceptance mismatch on {inp}"
        if verbose:
            print(f"Test {i} correct: {inp} => {x[1]}")

# generates a random n-string from a set of symbols
def nstring_generator(n: int, syms):
   return "".join(syms[randint(0, len(syms)-1)] for _ in range(n))


def splice_generator(s_max=15, j_max=13):
    s = nstring_generator(randint(1, s_max), ["0","1"])
    i = "0" * randint(1, len(s))
    j = "0" * randint(1, j_max)
    return "2".join([s,i,j])


def splice_correct(inp):
    try:
        [s, i_u, j_u] = inp.split("2")
        i = len(i_u)
        j = len(j_u)
        return (True, s[:i] + "2"*j + s[i:])
    except Exception as e:
        return (False, None)

if __name__ == "__main__":
    print("Testing 2_splicer")
    with open("hw1/2_splicer.txt") as f:
        splicer_code = f.read()
    test_machine(splice_generator, splicer_code, splice_correct, verbose=True)
    print("All correct") 
