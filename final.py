# final 
# xandy duhe


import argparse
import pickle
import os
from datetime import datetime
from datetime import timedelta



class Task:
    """
    Representation of a task

    Attributes:
    - created: date and time  
    - completed: date and time    
    - name: str if description of task  
    - id: nique id for task          
    - id_counter: variable to keep track of the total number of tasks
    - priority: 1 is default, 3 is highest
    - due_date: optional 

    """

    id_counter = 0  #  to assign unique id

    def __init__(self, name, priority=1, due_date=None):
        """
        creates a new task with a name, priority, and optional due date
        """
        # count and assign ID
        Task.id_counter += 1
        self.id = Task.id_counter

        # task attributes
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.created = datetime.now()  
        self.completed = None  # initialize as not completed

    def mark_done(self):
        """
        marks the task as completed by setting the completion date to the current date and time
        """
        self.completed = datetime.now()

    def is_completed(self):
        """
        vhecks if task is completed.
        """
        return self.completed is not None

    def age(self):
        """
        calculates age task in days (since it was created)
        """
        return (datetime.now() - self.created).days


class Tasks:
    """
    manages Task class
    """

    def __init__(self):

        """loads tasks from a pickle file"""

        self.tasks = []  # empty list to hold Task objects
        self.load_tasks()  # load tasks from pickle file

    def pickle_tasks(self):

        """adds tasks to .todo.pickle"""

        with open('.todo.pickle', 'wb') as file:
            pickle.dump(self.tasks, file)  # save tasks to file

    def list(self):

        """lists incomplete tasks (sorted by due date and priority)"""

        # filter unfinished tasks using list comprehention 
        tasks_to_list = [task for task in self.tasks if not task.is_completed()]  

        # sort tasks by due date and by priority using lambda
        tasks_to_list.sort(key=lambda x: (x.due_date or datetime.max, -x.priority))

        # header
        print("ID   Age  Due Date   Priority   Task")
        print("--   ---  --------   --------   ----")

        # task details
        for task in tasks_to_list:

            due_date_str = task.due_date.strftime('%m/%d/%Y') if task.due_date else "-"

            print(f"{task.id:<4} {task.age():<3} {due_date_str:<10} {task.priority:<8} {task.name}")

    def report(self):

        """creates report of all tasks (completed and incomplete)"""

        # header 
        print("ID   Age  Due Date   Priority   Task                Created                       Completed")
        print("--   ---  --------   --------   ----                ---------------------------   -------------------------")
        
        # task details
        for task in self.tasks:
        
            due_date_str = task.due_date.strftime('%m/%d/%Y') if task.due_date else "-"
            completed_str = task.completed.strftime('%a %b %d %H:%M:%S %Z %Y') if task.completed else "-"
            created_str = task.created.strftime('%a %b %d %H:%M:%S %Z %Y')

            print(f"{task.id:<4} {task.age():<3} {due_date_str:<10} {task.priority:<8} {task.name:<20} {created_str:<30} {completed_str:<25}")

    def done(self, task_id):
        """mark task as complete """

        for task in self.tasks:

            if task.id == task_id:
                # task completed
                task.mark_done() 
                
                # save updated list to pickle file
                self.pickle_tasks()  

                print(f"Completed task {task_id}")

                return
            
        # task not found error 
        print(f"Task {task_id} not found")  

    def query(self, terms):
        """search for tasks using search terms """

        print("ID   Age  Due Date   Priority   Task")
        print("--   ---  --------   --------   ----")

        for task in self.tasks:

            if not task.is_completed() and any(term.lower() in task.name.lower() for term in terms):

                due_date_str = task.due_date.strftime('%m/%d/%Y') if task.due_date else "-"

                print(f"{task.id:<4} {task.age():<3} {due_date_str:<10} {task.priority:<8} {task.name}")



    def add(self, name, priority=1, due_date=None):

        """Add new task list"""

        try:
            # crate new task 
            new_task = Task(name, priority, due_date)  
            # add task 
            self.tasks.append(new_task)  
            # save to pickle
            self.pickle_tasks() 
            print(f"Created task {new_task.id}")

        except Exception as e:
            print("Could not create your task. Run 'todo.py -h' for instructions.")
            print(e)  # error message

    def delete(self, task_id):

        """delet task from list using id"""

        # gilter out the task to be deleted
        self.tasks = [task for task in self.tasks if task.id != task_id] 
        # save list to npickle
        self.pickle_tasks() 

        print(f"Deleted task {task_id}")

    def load_tasks(self):

        """loads tasks from pickle file"""

        if os.path.exists('.todo.pickle'):
            with open('.todo.pickle', 'rb') as file:
                # load 
                self.tasks = pickle.load(file)  
                #count task 
                Task.id_counter = max(task.id for task in self.tasks)  
        else:
            # empty list if pickle file has not bee created yet 
            self.tasks = []  


def main():
    """
    main: task management using argparse

    """
    parser = argparse.ArgumentParser(description="Command Line Task Manager. \nUpdate your ToDo List.")

    # add new task 
    parser.add_argument('--add', type=str, required=False, help="a task string to add to your list")
    # set due date
    parser.add_argument('--due', type=str, required=False, help="due date in mm/dd/yyyy format")
    # set priority of task
    parser.add_argument('--priority', type=int, required=False, choices=[1, 2, 3], default=1, help="priority for the task; default is 1. options: 1, 2, or 3")
    # list all tasks (not been completed)
    parser.add_argument('--list', required=False, action='store_true', help="list all tasks that have not been completed")
    # print all tasks
    parser.add_argument('--report', required=False, action='store_true', help="full report of tasks")
    # mark task as completed by its id
    parser.add_argument('--done', type=int, required=False, help="mark a task as completed")
    # delete a task by id
    parser.add_argument('--delete', type=int, required=False, help="delete a task by ID")
    # search tasks byterms
    parser.add_argument('--query', type=str, required=False, nargs='+', help="search tasks by terms")
    
    # rarse
    args = parser.parse_args()
    
    # make instance of Tasks
    tasks = Tasks()

    if args.add:
        # due date if given, or None
        due_date = datetime.strptime(args.due, "%m/%d/%Y") if args.due else None

        # add task 
        tasks.add(args.add, args.priority, due_date)
    
    # --list: list incomplete tasks
    elif args.list:
        tasks.list()
    
    # --report : report of all tasks
    elif args.report:
        tasks.report()
    
    # --done: mark task as finished
    elif args.done:
        tasks.done(args.done)
    
    # --delete: delete task by its id
    elif args.delete:
        tasks.delete(args.delete)
    
    # --query: search tasks based on terms
    elif args.query:
        tasks.query(args.query)
    
    # no arguments: print help message
    else:
        parser.print_help()


if __name__ == "__main__":
    main()




