import re

def extract_function_definition(s):
    """
    Extracts the function/method definition part of the string that precedes the first '/* TODO */' comment.

    Parameters:
    - s (str): The original string containing the function/method definition and other content.

    Returns:
    - str: The extracted function definition part of the string.
    """
    # Define the pattern to search for. This pattern looks for the least greedy match up to an opening brace '{'
    # followed by any characters until the '/* TODO */' comment.
    pattern = r"^(.*?\{).*?/\* TODO \*/"

    # Use re.search() to find the match. The DOTALL flag allows '.' to match newline characters as well.
    match = re.search(pattern, s, flags=re.DOTALL)

    if match:
        # Extract and return the matched part, which is the function definition up to the opening brace
        return match.group(1)
    else:
        # If there is no match (which should not happen given your input but is good practice to check), return an empty string or appropriate message
        return ""

def prompt_fillbody(text):
    '''
    Applies a prompt format to text read from a _fillbody benchmark task file.
    For weaker models, prompt format can influence a model's performance on the benchmark. Hence we hold this constant across baseline evaluations in our original study. We invite community members to play with prompt format here!
    '''
    # NOTE: you are welcome to do fancier things to modify what the models sees of the task from the benchmark.
    # For the default approach used to initially compute the baselines reported in this benchmark, we prompt in the following way

    return f"""In Dafny, fill in the bodies of the functions, lemmas, or methods labeled with /* TODO */. This is the code to
complete:\n```dafny\n{text}\n```\nNow it is your turn:\n
```dafny\n{extract_function_definition(text)}""".rstrip() + "\n\t"

def prompt_fillanno(text):
    '''
    Applies a prompt format to text read from a _fillbody benchmark task file.
    '''
    pass
