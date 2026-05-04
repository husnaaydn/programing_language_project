import json


def load_grammar(filename):
    grammar = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            lhs, rhs = line.split("::=")
            lhs = lhs.strip()
            rhs = rhs.strip()

            alternatives = rhs.split("|")
            rule_list = []

            for alt in alternatives:
                tokens = alt.strip().split()
                rule_list.append(tokens)

            grammar[lhs] = rule_list

    return grammar


def is_nonterminal(symbol, grammar):
    return symbol in grammar


def current_token(tokens, pos):
    if pos < len(tokens):
        return tokens[pos]
    return None


def update_best_error(best_error, pos, expected):
    if pos > best_error["pos"]:
        best_error["pos"] = pos
        best_error["expected"] = {expected}
    elif pos == best_error["pos"]:
        best_error["expected"].add(expected)


def parse_symbol(symbol, grammar, tokens, pos, best_error):
    if not is_nonterminal(symbol, grammar):
        token = current_token(tokens, pos)

        if token == symbol:
            tree = {
                "type": "terminal",
                "symbol": symbol
            }
            return True, tree, pos + 1

        update_best_error(best_error, pos, symbol)
        return False, None, pos

    alternatives = sorted(grammar[symbol], key=len, reverse=True)

    for alt in alternatives:
        temp_pos = pos
        children = []

        if alt == ["ε"]:
            tree = {
                "type": "nonterminal",
                "symbol": symbol,
                "children": [
                    {
                        "type": "epsilon",
                        "symbol": "ε"
                    }
                ]
            }
            return True, tree, temp_pos

        success = True

        for part in alt:
            result, child_tree, temp_pos = parse_symbol(
                part, grammar, tokens, temp_pos, best_error
            )

            if not result:
                success = False
                break

            children.append(child_tree)

        if success:
            tree = {
                "type": "nonterminal",
                "symbol": symbol,
                "children": children
            }
            return True, tree, temp_pos

    return False, None, pos


def print_tree(tree, indent=0):
    space = "  " * indent
    print(space + tree["symbol"])

    if tree["type"] == "nonterminal":
        for child in tree["children"]:
            print_tree(child, indent + 1)


def compress_recursive_chain(tree):
    if tree["type"] != "nonterminal":
        return None

    children = tree["children"]

    if len(children) == 2:
        first, second = children

        if (
            first["type"] == "terminal"
            and second["type"] == "nonterminal"
            and second["symbol"] == tree["symbol"]
        ):
            rest = compress_recursive_chain(second)
            if rest is not None:
                return first["symbol"] + rest

    if len(children) == 1 and children[0]["type"] == "epsilon":
        return ""

    return None


def tree_to_json(tree):
    if tree["type"] == "terminal":
        return tree["symbol"]

    if tree["type"] == "epsilon":
        return "ε"

    compressed = compress_recursive_chain(tree)
    if compressed is not None:
        return compressed if compressed != "" else "ε"

    if len(tree["children"]) == 1 and tree["children"][0]["type"] == "terminal":
        return tree["children"][0]["symbol"]

    if len(tree["children"]) == 1 and tree["children"][0]["type"] == "epsilon":
        return "ε"

    result = {}

    for child in tree["children"]:
        key = child["symbol"].replace("<", "").replace(">", "")
        value = tree_to_json(child)

        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value

    return result


def tokenize_sentence(sentence, grammar):
    if sentence == "" or sentence == "ε":
        return []

    if " " in sentence:
        return sentence.split()

    terminals = set()

    for rules in grammar.values():
        for alt in rules:
            for symbol in alt:
                if not is_nonterminal(symbol, grammar) and symbol != "ε":
                    terminals.add(symbol)

    if terminals and all(len(t) == 1 for t in terminals):
        return list(sentence)

    return sentence.split()


def get_start_symbol(grammar):
    return next(iter(grammar))


def process_sentence(sentence, grammar, start_symbol):
    tokens = tokenize_sentence(sentence, grammar)
    best_error = {"pos": -1, "expected": set()}

    result, tree, final_pos = parse_symbol(start_symbol, grammar, tokens, 0, best_error)

    print("=" * 50)
    print("Input:", sentence if sentence != "" else "ε")

    if result and final_pos == len(tokens):
        print("Valid")
        print("Parse Tree:")
        print_tree(tree)

        print("\nJSON:")
        json_output = {
            tree["symbol"].replace("<", "").replace(">", ""): tree_to_json(tree)
        }
        print(json.dumps(json_output, indent=2, ensure_ascii=False))
        return

    print("Invalid")
    print("Error:")

    error_pos = best_error["pos"]
    found_token = current_token(tokens, error_pos)

    if found_token is None:
        found_token = "END"

    expected = ", ".join(sorted(best_error["expected"])) if best_error["expected"] else "unknown"

    print(f'- Where the error occurs: token {error_pos + 1} ("{found_token}")')
    print(f"- What was expected: {expected}")

    if error_pos == 0:
        print("- Why the sentence is invalid: sentence does not match the required starting structure")
    else:
        print(f"- Why the sentence is invalid: There should have been '{expected}' instead")


def main():
    grammar_file = "grammar1.txt"
    sentences_file = "sentences1.txt"

    grammar = load_grammar(grammar_file)
    start_symbol = get_start_symbol(grammar)

    with open(sentences_file, "r", encoding="utf-8") as file:
        for line in file:
            sentence = line.strip()
            process_sentence(sentence, grammar, start_symbol)


if __name__ == "__main__":
    main()