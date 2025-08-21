import time
import utils


INVALID_COMMAND_MESSAGE = "😕 Invalid command, please try again."
INDEX_ERROR_MESSAGE = "😕 There is no item with that number."


def main():
    now = time.strftime("%b %d, %Y %H:%M:%S")
    print("It is", now)
    while True:
        user_action = input("Type add, show, edit, complete or exit: ")
        user_action = user_action.strip()

        if user_action.startswith("add"):
            todo = user_action[4:]

            todos = utils.get_todos()

            todos.append(todo + "\n")

            utils.write_todos(todos)

        elif user_action.startswith("show"):
            todos = utils.get_todos()

            for index, item in enumerate(todos):
                trimmed_item = item.strip("\n")
                row = f"{index + 1}.{trimmed_item}"
                print(row)

        elif user_action.startswith("edit"):
            try:
                number = int(user_action[5:])
                number = number - 1

                todos = utils.get_todos()

                new_todo = input("Enter new todo: ")
                todos[number] = new_todo + "\n"

                utils.write_todos(todos)

            except ValueError:
                print(INVALID_COMMAND_MESSAGE)
                continue

        elif user_action.startswith("complete"):
            try:
                number = int(user_action[9:])

                todos = utils.get_todos()

                index = number - 1
                todo_to_remove = todos[index].strip("\n")

                todos.pop(index)

                utils.write_todos(todos)

                message = f"Todo {todo_to_remove} has been removed."
                print(message)

            except IndexError:
                print(INDEX_ERROR_MESSAGE)
                continue

        elif user_action == "exit":
            print("Closing the program...")
            break
        else:
            print(INVALID_COMMAND_MESSAGE)


main()
