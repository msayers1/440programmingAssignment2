"""
Module:
For file manager functions.
"""

def create_file(filename):
    """
    Args:
    filename: name of file
    
    Results:
    Creates file
    """
    with open(filename, 'w', encoding="utf-8"):
        pass
# def write_to_file(filename):
#     """
#     Args:
#     filename: name of file
#     Results:
#     Opens a file and writes to it.
#     """

def add_to_file(filename, string):
    """
    Args:
    filename: name of file
    
    Results:
    Opens a file to write and passes back a handler
    """
    with open(filename, 'a', encoding="utf-8") as file:
        file.write(string + '\n')

def count_lines(file_name):
    """
    Args:
    filename: name of file which you want to count lines.

    Returns:
    Number of lines. 
    """
    with open(file_name, 'r', encoding="utf-8") as file:
        return sum(1 for line in file)

def read_file(filename, separator, dictionary_maker):
    """
    Args:
    filename: name of file which you want to count lines.

    Returns:
    A list of the lines separated by separator. 
    """
    result_dictionary = []
    with open(filename, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
        line_array = None
        for line in all_lines:
            line_array = line.split(separator)
            line_of_dictionary = dictionary_maker(line_array)
            result_dictionary.append(line_of_dictionary)
    return result_dictionary
