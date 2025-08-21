FILEPATH = "todos.txt"


def get_todos(path=FILEPATH):
    """
    Read a text file and return the list of
    to-do items.
    """
    with open(path, "r", encoding="utf8") as fr:
        todos = fr.readlines()
    return todos


def write_todos(todos: list[str], path=FILEPATH):
    """Write the to-do items list in the text file."""
    with open(path, "w", encoding="utf8") as fw:
        fw.writelines(todos)
