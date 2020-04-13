import hfst
import re

acceptor_dict_lst = []
finality_dict_lst = []
name_lst = []
sym_pair_set = set()

error_count = 100       # so many errors can still be reported

def acceptor_dict(rule_fst):
    brule = hfst.HfstBasicTransducer(rule_fst)
    rule_dict = {}
    final_states = set()
    for state in brule.states():
        if brule.is_final_state(state):
            final_states.add(state)
        trans_dict = {}
        for transition in brule.transitions(state):
            insym = transition.get_input_symbol()
            outsym = transition.get_output_symbol()
            sym_pair_set.add((insym, outsym))
            target = transition.get_target_state()
            trans_dict[(insym,outsym)] = target
        rule_dict[state] = trans_dict
    return rule_dict, final_states

def init(rule_file_name):
    istream = hfst.HfstInputStream(rule_file_name)
    while not (istream.is_eof()):
        fst = istream.read()
        rule_d, final_states = acceptor_dict(fst)
        acceptor_dict_lst.append(rule_d)
        finality_dict_lst.append(final_states)
        name = fst.get_name()
        name_lst.append(name)
    istream.close()
    return

def complain(pre_lst, post_lst, name):
    global verbosity
    pre_lst = [(insym if insym == outsym
                else insym + ":" + outsym) for insym, outsym in pre_lst]
    pre_str = " ".join(pre_lst)
    post_lst = [(insym if insym == outsym
                else insym + ":" + outsym) for insym, outsym in post_lst]
    post_str = " ".join(post_lst)
    print(pre_str, ">>>", post_str)
    print(" "*8, name)

def accept(state_lst, accepted_lst,
           remaining_lst,
           fail_set):
    global verbosity
    if verbosity >= 10:
        print("state_lst:", state_lst)
        print("accepted_lst:", accepted_lst)
        print("remaining_lst:", remaining_lst)
        print("fail_set:", fail_set)
    if not remaining_lst:
        for state, finality, name in zip(state_lst,
                                         finality_dict_lst,
                                         name_lst):
            if state in fail_set:
                continue
            if state not in finality and name not in fail_set:
                complain(accepted_lst, [], name)
        return
    sym_pair = remaining_lst[0]
    
    new_state_lst = []
    for state, rule_d, name in zip(state_lst, acceptor_dict_lst, name_lst):
        if name in fail_set:
            new_state_lst.append('*')
        elif sym_pair in rule_d[state]:
            new_state_lst.append(rule_d[state][sym_pair])
        else:
            new_state_lst.append('*')
            complain(accepted_lst, remaining_lst, name)
            fail_set.add(name)
    accepted_lst.append(sym_pair)
    accept(new_state_lst, accepted_lst, remaining_lst[1:], fail_set)
    return

def test(pair_sym_str):
    global verbosity
    psym_lst = pair_sym_str.strip().split()
    spair_lst = []
    for psym in psym_lst:
        insym, colon, outsym = psym.partition(":")
        if not colon:
            outsym = insym
        if (insym, outsym) not in sym_pair_set:
            print("\n*** " + pair_sym_str + "\n")
            print("***", psym, "not known by the rules")
            return
        spair_lst.append((insym, outsym))
    if verbosity >= 10:
        print("spair_lst:", spair_lst)
    start_state_lst = [0 for r in acceptor_dict_lst]
    accept(start_state_lst, [], spair_lst, set())
    return

if __name__ == "__main__":
    global verbosity
    import sys
    import argparse
    argparser = argparse.ArgumentParser("python3 pairtest.py",
    description="""
    Tests a set of pair string examples against compiled two-level rules

    The examples are read from STDIN and possible discrepancies are
    printed.  The testing checks one example at a time and reports all
    rules which do not accept the example. """)
    argparser.add_argument(
        "-r", "--rules",
        help="""An FST file containing the compiled two-level rules.
        The file contains one FST for each rule, the default is
        "ofi-rules-in.fst".""",
        default="ofi-rules-in.fst")
    argparser.add_argument(
        "-m", "--max-errors", default="100", type=int,
        help="""Maximum number of error messages printed in total.
        Default is 100""")
    argparser.add_argument(
        "-v", "--verbosity",
    default=0, type=int,
    help="Level of diagnostic output, default is 0.")

    args = argparser.parse_args()
    verbosity = args.verbosity

    init(args.rules)
    for line_nl in sys.stdin:
        line = line_nl.strip()
        test(line)
    print("-------------------------")
    print("all tests now completeded")
    print("-------------------------")
