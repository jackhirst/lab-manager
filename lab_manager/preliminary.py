"""
stuff that needs making:
- manager class(?)
    - contains list of experiments
    -

- experiment class
    - made up of tasks (these are things you can reasonably complete in a single sitting)
    - has a list of prerequisites and a bool to say if they've been completed
    - has sample count
    - with sample count, will list estimate of time
    - has ability to tick off prerequisites, activate tasks

-task class
    - has timer to clock up how long spent on task
    - has sample count

- task memory
    - stores list of lists of tasks, sample counts, and time spent on them previously
"""

import datetime as dt
import tkinter as tk


def function_to_test(an_integer: int) -> int:
    return an_integer + 1

# region

# class Task:
#     def __init__(self, name):
#         self.name = name

#     runs = []
#     fit = None

#     def fit_time(self):
#         xs = [x[0] for x in self.runs]
#         ys = [x[1] for x in self.runs]
#         coef = np.polyfit(xs, ys, 1)
#         self.fit = np.poly1d(coef)


# transfection_task = Task("transfection")
# transfection_task.runs = [[6, 90], [2, 30], [4, 45]]
# transfection_task.fit_time()

# mediachange_task = Task("media_change")
# mediachange_task.runs = [[6, 25], [2, 20], [4, 25]]
# mediachange_task.fit_time()

# task_dict = {"transfection": transfection_task, "media_change": mediachange_task}


# class Experiment:
#     def __init__(self, name, start_date, schedule, sample_count):
#         self.name = name
#         self.start_date = start_date
#         self.schedule = schedule
#         self.sample_count = sample_count

#     def initialise_schedule(self):
#         final_schedule = []
#         for i in range(len(self.schedule) + 1):
#             if i == 0:
#                 first_task = self.schedule[0][0]
#                 final_schedule.append(first_task.name, self.start_date, first_task.fit(self.sample_count))
#             else:
#                 task_date = "test"
#         pass

#     # def estimate_time(self):
#     #     constituent_tasks = [x for x in task_list if x.name in self.constituent_task_names]
#     #     estimated_task_lengths = [x.fit(self.sample_count) for x in constituent_tasks]
#     #     self.estimated_time = sum(estimated_task_lengths)

# endregion

def initialise_schedule(input_schedule: list, start_date: dt.date) -> list:
    final_schedule = []
    for i in range(len(input_schedule)):
        if i == 0:  # treat first task separately
            first_task = input_schedule[0][0]
            final_schedule.append([first_task, start_date, "soft"])
        else:
            previous_date = final_schedule[i - 1][1]
            new_date = previous_date + dt.timedelta(hours=input_schedule[i][-1])
            final_schedule.append([input_schedule[i][0], new_date, input_schedule[i][1]])
    return final_schedule

def alter_existing_schedule(existing_schedule: list, index: int, new_date: dt.date) -> list:
    # change the schedule at index and update downstream requirements
    # remembering each item in the schedule goes ["name", "date", "hard/soft flag"]
    first_part = existing_schedule[0:index]
    # get gaps and flags for next parts. basically going to treat this like its own separate schedule
    second_part = existing_schedule[index:]
    dates = [x[1] for x in second_part]
    diff_list = [dates[i + 1] - dates[i] for i in range(len(dates) - 1)]
    new_schedule = []
    for i in range(len(second_part)):
        if i == 0:
            new_schedule.append([second_part[i][0], new_date, second_part[i][2]])
        else:
            previous_date = new_schedule[i - 1][1]
            updated_date = previous_date + diff_list[i - 1]
            new_schedule.append([second_part[i][0], updated_date, second_part[i][2]])
    new_schedule = first_part + new_schedule
    return new_schedule

class LabelledEntry(tk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        name: str,
        suggestion: str,
        index: int,
        button_text1: str = "Add",
        button_text2: str = "Update",
        button_text3: str = "Remove",
        command1=None,
        command2=None,
        command3=None,
    ) -> None:
        super().__init__(parent)
        self.index = index
        self.label = tk.Label(self, text=name)
        self.label.grid(column=1)
        self.entry = tk.Entry(self, fg="black")
        self.entry.grid(column=1)
        self.suggestion = suggestion
        self.entry.insert(0, suggestion)
        self.button1 = tk.Button(self, text=button_text1, command=command1)
        self.button2 = tk.Button(self, text=button_text2, command=lambda: command2(self))
        self.button3 = tk.Button(self, text=button_text3, command=command3)
        self.button1.grid(row=2, column=0)
        self.button2.grid(row=2, column=1)
        self.button3.grid(row=2, column=2)

    def get_entry(self):
        return self.index, self.entry.get()

def update_schedule(widget: LabelledEntry):
    index, new_date = widget.get_entry()
    print(index)
    print(new_date)
    return None
    # widget.winfo_toplevel().destroy()

def gui_modify_schedule(input_schedule: list) -> list:
    schedule = tk.Toplevel()
    schedule.title("schedule")
    counter = 0
    for s in input_schedule:
        if s[-1] == "soft":
            widget = LabelledEntry(
                schedule,
                name=s[0],
                suggestion=str(s[1].date()),
                button_text1="Add",
                command2=update_schedule,
                button_text2="Update",
                button_text3="Remove",
                index=counter,
            )
        if s[-1] == "hard":
            label = tk.Label(schedule, text=f"{s[0]}\n{str(s[1].date())}")
            label.pack()
        counter += 1
        widget.pack()
    exit = tk.Button(schedule, text = "Finish", command=None)
    exit.pack()
    return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main")

    test_schedule = [
        ["transfection"],
        ["media_change", "hard", 24],
        ["d3_harvest", "soft", 48],
        ["EP1", "soft", 0],
        ["EP1_harvest", "hard", 72],
        ["EP2", "soft", 0],
        ["EP2 harvest", "hard", 72],
    ]

    test_schedule = initialise_schedule(test_schedule, dt.datetime.fromisoformat("2026-01-01"))
    
    updated_test_schedule = gui_modify_schedule(test_schedule)

    label_test = tk.Label(root, text="main window")
    label_test.pack()

    root.mainloop()

    print("yay")
