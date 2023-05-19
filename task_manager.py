# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# read the tasks.txt file.
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()
    
    # here, I have modified the code so that it checks if a username is already used or not.
    def reg_user():
        '''Add a new user to the user.txt file'''
        
        # - Request input of a new username
        while True:
            new_username = input("New Username: ")
            try:
                with open("user.txt") as f:
                    if new_username in f.read():
                        print("You have entered a username that is already taken, please enter a new one")
                        continue
                    else:
                        break
            except ValueError:
                print("Invalid Username")    
                break      
            
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")


    def add_task():
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


    def view_all():
        '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            
    # For this part I got stuck on how to add the option to edit the task, I therefore requested help
    # from my mentor, who helped me to work through the task and fix the issues I was encountering.
    def view_mine():
        '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
        '''
        num = 0
        for index, t in enumerate(task_list):
            if t['username'] == curr_user: 
                disp_str = f"Task ID: \t\t {index}\n"
                disp_str += f"Task Name: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

        select_task = int(input("Please enter the number of the task you wish to select or -1 to go back to the menu: "))
        if select_task == -1:
            return 
        
    # here the user slects whether or not they want to make any changes to the task that was selected.
        choice = input("Do you wish to edit the task or mark it as completed? Y/N: ")
         
        # if they choose no, then the task is not selected for editing.
        # if they choose yes, then there is a choice between editing or marking as complete.
        if choice in ["N", "No", "n", "no"]:
            print("Task not selected for editing.")
        elif choice in ["Y", "Yes", "y", "yes"]:     
            for index, task in enumerate(task_list):
                if index == select_task: 
                    if task['completed'] == "Yes":
                        print("Task is already completed, unable to edit.")
                        return
                    
                    # if the user selects 1 then the task will be marked as complete, if 2:
                    # the task will be edited: only the user and task due date can be edited.
                    action = int(input("What do you wish to do? 1: Mark as complete, 2: Edit Task: "))
                    if action == 1:
                        task['completed'] = "Yes"
                        print("Task marked as completed.")
                    elif action == 2:
                        edit_choice = int(input("What do you wish to do? 1: Username, 2: due date: "))
                        if edit_choice == 1:
                            task['username'] = input("Enter new username: ")
                        elif edit_choice == 2:
                            while True:
                                try:
                                    task_due_date = input("Enter new due date (YYYY-MM-DD): ")
                                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                                    task['due_date'] = due_date_time
                                    break
                                except ValueError:
                                    print("Invalid format, please use YYYY-MM-DD.")
                    else:
                        print("Invalid Choice. Going back to the menu.")
                        return
            
            # tasks.txt is opened and written to.            
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task successfully edited.")
    
    # the generate reports option is split into two functions, generate_task_overview and generate_user_overview
    # these functions are called in the main menu when gr is entered. the first report contains the following:
    # total tasks
    # completed tasks
    # uncompleted tasks
    # overdue tasks
    # percentage of incomplete tasks
    # percentage of overdue tasks
    
            
    def generate_task_overview(task_list):
        total_tasks = len(task_list)
        completed_tasks = sum(1 for task in task_list if task['completed'] == "Yes")
        uncompleted_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for task in task_list if task['completed'] == "No" and task['due_date'] < datetime.now())
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100

        with open("task_overview.txt", "w") as task_overview:
            task_overview.write(f"Total tasks: {total_tasks}\n")
            task_overview.write(f"Completed tasks: {completed_tasks}\n")
            task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
            task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
            task_overview.write(f"Incomplete tasks percentage: {incomplete_percentage:.2f}%\n")
            task_overview.write(f"Overdue tasks percentage: {overdue_percentage:.2f}%\n") 
    
    #The second report contains the following:
    # total tasks
    # Percentage of total tasks
    # Percentage of completed tasks
    # Percentage of incomplete tasks
    # Percentage of overdue tasks
    def generate_user_overview(task_list, user_data):
        total_users = len(user_data)
        total_tasks = len(task_list)

        user_statistics = {}
        for task in task_list:
            username = task['username']
            if username not in user_statistics:
                user_statistics[username] = {'total': 0, 'completed': 0, 'overdue': 0}
            user_statistics[username]['total'] += 1
            if task['completed'] == "Yes":
                user_statistics[username]['completed'] += 1
            elif task['due_date'] < datetime.now():
                user_statistics[username]['overdue'] += 1

        with open("user_overview.txt", "w") as user_overview:
            user_overview.write(f"Total users: {total_users}\n")
            user_overview.write(f"Total tasks: {total_tasks}\n\n")
            for username, stats in user_statistics.items():
                user_overview.write(f"User: {username}\n")
                user_overview.write(f"Total tasks assigned: {stats['total']}\n")
                user_overview.write(f"Percentage of total tasks: {(stats['total'] / total_tasks) * 100:.2f}%\n")
                user_overview.write(f"Percentage of completed tasks: {(stats['completed'] / stats['total']) * 100:.2f}%\n")
                user_overview.write(f"Percentage of incomplete tasks: {((stats['total'] - stats['completed']) / stats['total']) * 100:.2f}%\n")
                user_overview.write(f"Percentage of overdue tasks: {(stats['overdue'] / stats['total']) * 100:.2f}%\n\n")
    
    # here display statistics is modified to check whether or not the file exists, and creates the file if it doesn't                    
    def display_statistics(): 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            generate_task_overview(task_list)
            generate_user_overview(task_list, user_data)

            with open("task_overview.txt", "r") as task_overview:
                print("Task Overview:\n")
                print(task_overview.read())

            with open("user_overview.txt", "r") as user_overview:
                print("Task Overview:\n")
                print(user_overview.read())    
        
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    
        
        

    def exit_menu():
        print('Goodbye!!!')
        exit()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_task_overview(task_list)
        generate_user_overview(task_list, user_data)
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
        
    elif menu == 'e':
        exit_menu()
    else:
        print("You have made a wrong choice, Please Try again")