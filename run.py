import importlib
Node = importlib.import_module("llm-verified-with-monte-carlo-tree-search.montecarlo.node")
MonteCarlo = importlib.import_module("llm-verified-with-monte-carlo-tree-search.montecarlo.montecarlo")

from evaluate import can_be_solution
from evaluate import score_func_whole as uncached_score_func #NOTE: score_func_whole is generalized score_func

create_cached_func = importlib.import_module("llm-verified-with-monte-carlo-tree-search.common_cache").create_cached_func
score_func, cache_stats, reset_cache = create_cached_func(uncached_score_func)

from prompts import expansion_count
limit_depth = importlib.import_module("llm-verified-with-monte-carlo-tree-search.common").limit_depth
max_completion_depth = importlib.import_module("llm-verified-with-monte-carlo-tree-search.common").max_completion_depth
stats = importlib.import_module("llm-verified-with-monte-carlo-tree-search.common_stats").stats

llm = importlib.import_module("llm-verified-with-monte-carlo-tree-search.llm")

import tiktoken

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def generate_complete(text, montecarlo, current_completion_depth=1, formal_spec=[]):
    if current_completion_depth >= max_completion_depth:
        return None
    prev = text
    texts = llm.generate(text, 1)
    text = texts[0]
    score = score_func(text)
    if score is not None:
        if score < 0:
            return None
        else:
            is_sol, sol = can_be_solution(text, formal_spec)
            if is_sol:
                montecarlo.solution = sol
            return text
    else:
        return generate_complete(text, montecarlo, current_completion_depth + 1, formal_spec)


def child_finder(node, montecarlo, formal_spec=[]):
    if limit_depth(node):
        return

    text = generate_complete(node.state, montecarlo, formal_spec)
    if text is None:
        node.update_win_value(-1)
    else:
        child = Node(text)
        node.add_child(child)
        child.update_win_value(1)
        child.update_policy_value(1)

        child = Node(node.state)
        node.add_child(child)
        child.update_policy_value(0.2)

def main(mins_timeout = None, prompt = prompt, formal_spec = []):
    montecarlo = MonteCarlo(Node(prompt), mins_timeout)
    montecarlo.child_finder = child_finder(formal_spec=formal_spec) #NOTE: can I curry like this?

    montecarlo.simulate(expansion_count)

    print("CHOSEN SOLUTION")
    print(montecarlo.solution)

    stats(montecarlo)
    print('cache stats', cache_stats)
    #with open("graph.dot", "w") as f:
    #    montecarlo.print_tree(f)

    return cache_stats

if __name__ == "__main__":
    main()

