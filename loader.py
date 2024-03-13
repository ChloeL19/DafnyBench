import os
import re
from prompts import prompt_fillbody

def get_formal_spec(input_string):
    # Remove substrings with brackets surrounding a /*TODO*/ statement
    output_string = ""
    i = 0
    while i < len(input_string):
        if input_string[i] == "{" and "/*TODO*/" in input_string[i:]:
            j = input_string.find("}", i)
            if j != -1:
                i = j + 1
        else:
            output_string += input_string[i]
            i += 1

    # Remove single-line comments
    lines = output_string.split("\n")
    output_lines = [line for line in lines if not line.strip().startswith("//")]
    output_string = "\n".join(output_lines)

    # Remove block comments
    while "/*" in output_string:
        start_index = output_string.find("/*")
        end_index = output_string.find("*/", start_index)
        if end_index != -1:
            output_string = output_string[:start_index] + output_string[end_index + 2:]
        else:
            break

    # Remove any curly braces at the end that have whitespace between them
    output_string = re.sub(r'\{\s+\}$', '{\n', output_string)
    
    # Split the output string into chunks based on empty lines
    chunks = re.split(r'\n\s*\n', output_string)
    
    # Trim whitespace from each chunk and remove empty chunks
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    return chunks

def example_iterator(base_path="tasks/", task_name="fill_body"):
    assert task_name in ["fill_body", "fill_annotations"]
    base_path = os.path.join(base_path, task_name)
    ext_name = '_fillbody.dfy' if task_name == "fill_body" else '_fillanno.dfy'
    # Walk through all subdirectories of the given base path
    for root, dirs, files in os.walk(base_path):
        # Filter and process only files that end with the proper extension
        for file in files:
            if file.endswith(ext_name):
                method_name = file.split(ext_name)[0]
                file_path = os.path.join(root, file)
                # Open and read the content of the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    formal_spec = get_formal_spec(content)
                    # apply the prompt format to the content of the file
                    content = prompt_fillbody(content)
                    # Yield the content of the file
                    yield method_name, content, formal_spec

if __name__ == "__main__":
    sample = next(example_iterator())
    print("METHOD NAME:")
    print(sample[0])
    print("PROMPT:")
    print(sample[1])
    print("FORMAL SPEC")
    print(sample[2])
