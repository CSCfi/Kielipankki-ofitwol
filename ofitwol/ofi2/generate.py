import hfst
import re

pairs_with_insym = {}

rule_dict_lst = []
finality_dict_lst = []

def dict_rule(rule_fst):
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
            target = transition.get_target_state()
            trans_dict[(insym,outsym)] = target
            if insym not in pairs_with_insym:
                pairs_with_insym[insym] = set()
            pairs_with_insym[insym].add((insym, outsym))
        rule_dict[state] = trans_dict
    return rule_dict, final_states

def init(rule_file_name):
    istream = hfst.HfstInputStream(rule_file_name)
    while not (istream.is_eof()):
        fst = istream.read()
        rule_d, final_states = dict_rule(fst)
        rule_dict_lst.append(rule_d)
        finality_dict_lst.append(final_states)
    istream.close()
    return

result_set = set()

def search(state_lst, insym_lst, outsym_lst):
    global result_set
    if not insym_lst:
        for state, finality in zip(state_lst, finality_dict_lst):
            if state not in finality:
                return
        # print("outsym_lst:", outsym_lst) ###
        res = "".join(outsym_lst)
        # print("res:", res) ###
        res = res.replace("Ø", "")
        # print("res:", res) ###
        result_set.add(res)
        return
    insym = insym_lst[0]
    pair_set = pairs_with_insym[insym]
    for insym, outsym in pair_set:
        new_state_lst = []
        for state, rule_d in zip(state_lst, rule_dict_lst):
            if (insym, outsym) in rule_d[state]:
                new_state_lst.append(rule_d[state][(insym, outsym)])
            else:
                break
        else:
            new_outsym_lst = outsym_lst.copy()
            new_outsym_lst.append(outsym)
            search(new_state_lst, insym_lst[1:], new_outsym_lst)
        continue
    
    return
        

def generate(word):
    global result_set, rule_dict_lst
    result_set = set()
    insym_lst = re.findall(r"{[^{}]+}|[^{}+]|[+][A-Z1-9]+", word)
    print(insym_lst) ###
    start_state_lst = [0 for r in rule_dict_lst]
    search(start_state_lst, insym_lst, [])
    return result_set

if __name__ == "__main__":
    import sys, re
    init("ofi-rules-in.fst")
    for line_nl in sys.stdin:
        line = line_nl.strip()
        res = generate(line)
        print("  -> ", res)
        print()
    
