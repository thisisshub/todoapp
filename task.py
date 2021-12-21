import sys, os.path
from datetime import datetime


def help():
    message = """Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics\n"""
    sys.stdout.buffer.write(message.encode('utf8'))


def add(priority: int, message: str):
    """Add a new item with priority in task.txt

    Args:
        priority (int): Integer used for index
        message (str): A string used for text
    """
    message = ' '.join(message)
    if os.path.isfile('task.txt'):
        with open('task.txt', 'r') as original_f:
            data = original_f.read()
        with open('task.txt', 'w') as modified_f:
            modified_f.writelines('{} [{}] \n{}'.format(message, priority, data))
    else:
        with open('task.txt', 'w') as f:
            f.writelines('{} [{}] \n'.format(message, priority))
    sys.stdout.buffer.write('Added task: "{}" with priority {}\n'.format(message, priority).encode('utf8'))


def ls():
    """Show sorted tasks by priority in ascending order
    """
    if os.path.isfile('task.txt'):
        with open('task.txt', 'r') as f:
            data = f.readlines()
        count = sum(1 for line in open('task.txt'))
        st = ""
        with open('task.txt') as f:
            f = set(f.readlines())
            lines = [line.split() for line in f]
            lines.sort(key=lambda s: s[-1])
            for index, line in enumerate(lines, 1):
                st += "{}. {}\n".format(index, ' '.join(line))
        sys.stdout.buffer.write(st.encode('utf8'))
        if count == 0:
            sys.stdout.buffer.write("There are no pending tasks!\n".encode('utf8'))


def delete(index: int):
    """Delete the incomplete item with the given index

    Args:
        index (int): Integer used for index
    """
    if os.path.isfile('task.txt'):
        with open('task.txt', 'r') as f:
            data = f.readlines()
        count = sum(1 for line in open('task.txt'))
        if index > count or index <= 0:
            sys.stdout.buffer.write("Error: task with index #{} does not exist. Nothing deleted.".format(index).encode('utf8'))
        else:
            with open('task.txt', 'w') as f:
                for line in data:
                    if count != index:
                        f.write(line)
                    count -= 1
                sys.stdout.buffer.write("Deleted task #{}".format(index).encode('utf8'))
    else:
        sys.stdout.buffer.write("Error: task with index #{} does not exist. Nothing deleted.".format(index).encode('utf8'))


def done(index: int):
    """Mark the incomplete item with the given index as complete and move item from
    task.txt to completed.txt

    Args:
        index (int): Integer used for index
    """
    if os.path.isfile('task.txt'):
        with open('task.txt', 'r') as todo_file:
            todo_data = todo_file.readlines()
        count = sum(1 for line in open('task.txt'))
        if index > count or index <= 0:
            sys.stdout.buffer.write("Error: no incomplete item with index #{} exists.\n".format(index).encode('utf8'))
        else:
            with open('task.txt', 'r') as todo_file_modified, open('completed.txt', 'a') as done_file_modified:
                lines = todo_file_modified.readlines()
                for line in lines:
                    if lines[index - 1] == line:
                        done_file_modified.writelines('x '
                                        + datetime.today().strftime('%Y-%m-%d') + ' ' + line)
            sys.stdout.buffer.write('Marked item as done.\n'.format(index).encode('utf8'))
            with open('task.txt', 'r+') as f:
                lines = f.readlines()
                f.truncate(0)
                for line in lines:
                    if lines[index - 1] not in line:
                        f.write(line)
    else:
        sys.stdout.buffer.write('Error: no incomplete item with index #{} exists.\n'.format(index).encode('utf8'))


def report():
    """Statistics
    """
    todo_count = 0
    count_done = 0
    if os.path.isfile('task.txt'):
        with open('task.txt', 'r') as f:
            data = f.readlines()
        todo_count = len(data)
    st = ""
    with open('task.txt') as original_f:
        original_f = set(original_f.readlines())
        lines = [line.split() for line in original_f]
        lines.sort(key=lambda s: s[-1])
        for index, line in enumerate(lines, 1):
            st += "{}. {}\n".format(index, ' '.join(line))
    if os.path.isfile('completed.txt'):
        count_done = 0
        with open('completed.txt', 'r') as done_file:
            done_data = done_file.readlines()
            for line in done_data:
                temp = line.split()
                if temp[1] == str(datetime.today().strftime('%Y-%m-%d')):
                    count_done += 1
    done_st = ""
    with open('completed.txt') as done_f:
        done_f = set(done_f.readlines())
        lines = [line.split() for line in done_f]
        lines.sort(key=lambda s: s[-1])
        for index, line in enumerate(lines, 1):
            line = ' '.join(line)
            line = line[13:]
            line = line[:-4]
            done_st += "{}. {}\n".format(index, line)
    message = 'Pending : {}\n{}'.format(todo_count, st)
    message += 'Completed : {}\n{}'.format(count_done, done_st)
    sys.stdout.buffer.write(message.encode('utf8'))


def main():
    if len(sys.argv)==1:
        help()
    elif sys.argv[1]=='help':
        help()
    elif sys.argv[1]=='ls':
        ls()
    elif sys.argv[1]=='add':
        if len(sys.argv)>2:
            add(sys.argv[2], sys.argv[3:])
        else:
            print("Error: Missing tasks string. Nothing added!")
    elif sys.argv[1]=='del':
        if len(sys.argv)>2:
            delete(int(sys.argv[2]))
        else:
            print("Error: Missing NUMBER for deleting tasks.")
    elif sys.argv[1]=='done':
        if len(sys.argv)>2:
            done(int(sys.argv[2]))
        else:
            print("Error: Missing NUMBER for marking tasks as done.")
    elif sys.argv[1] == 'report':
            report()


if __name__ == '__main__':
    main()
