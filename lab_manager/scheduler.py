import datetime as dt
import tkinter as tk
import typing

def initialise_schedule(input_schedule: list[dict], start_date: dt.date) -> list[dict]:
    """
    Generate a dated schedule from a template schedule and a start date.

    The first task is assigned `start_date`. Each subsequent task date is
    calculated by adding the task's ``wait_time`` (in hours) to the previous
    task's date. The first task is always marked as ``"soft"``; all other
    tasks retain their original ``category``.

    Args:
        input_schedule (list[dict]): Template schedule where each item contains:
            - "task_name" (str): Name of the task.
            - "wait_time" (int | float): Hours to wait after the previous task.
            - "category" (str): Task category (e.g., "soft", "hard").
        start_date (datetime.date): Date assigned to the first task.

    Returns:
        list[dict]: A new schedule where each item contains:
            - "task_name" (str): Name of the task.
            - "task_date" (datetime.date | datetime.datetime): Calculated date.
            - "category" (str): Task category.

    Raises:
        KeyError: If required keys are missing from input_schedule items.
        TypeError: If wait_time is not numeric or start_date is invalid.
    """
    final_schedule: list[dict] = []
    for i in range(len(input_schedule)):
        if i == 0:  # treat first task separately
            final_schedule.append({"task_name": input_schedule[i]["task_name"], 
                                   "task_date": start_date, 
                                   "category": "soft"})
        else:
            previous_date = final_schedule[i-1]["task_date"]
            new_date = previous_date + dt.timedelta(hours=input_schedule[i]["wait_time"])
            final_schedule.append({"task_name": input_schedule[i]["task_name"],
                                   "task_date": new_date,
                                   "category": input_schedule[i]["category"]})
    return final_schedule

def alter_existing_schedule(existing_schedule: list[dict], index: int, new_date: str) -> list[dict]:
    """
    Update a task's date in an existing schedule and recalculate all downstream dates.

    The task at the specified index is assigned a new date. All subsequent
    tasks are shifted while preserving their original time intervals
    relative to one another. Tasks before the specified index remain unchanged.

    Args:
        existing_schedule (list[dict]): Current schedule where each item contains:
            - "task_name" (str): Name of the task.
            - "task_date" (datetime.datetime): Scheduled date and time.
            - "category" (str): Task category.
        index (int): Position of the task to modify.
        new_date (str): New date in ISO 8601 format
            (e.g., "2026-03-03").

    Returns:
        list[dict]: Updated schedule with recalculated downstream task dates.

    Raises:
        IndexError: If index is out of range.
        ValueError: If new_date is not a valid ISO 8601 datetime string.
        KeyError: If expected keys are missing from schedule items.
    """
    first_part: list[dict] = existing_schedule[0:index]
    # get gaps and flags for next parts. basically going to treat this like its own separate schedule
    second_part: list[dict] = existing_schedule[index:]
    dates = [x["task_date"] for x in second_part]
    wait_times = [dates[i + 1] - dates[i] for i in range(len(dates) - 1)] #convert dates back into wait times
    new_schedule = []
    for i in range(len(second_part)):
        if i == 0: #this is the task that's specifically being altered
            new_schedule.append({"task_name": second_part[i]["task_name"],
                                 "task_date": dt.datetime.fromisoformat(new_date),
                                 "category": second_part[i]["category"]})
        else:
            previous_date = new_schedule[i - 1]["task_date"]
            updated_date = previous_date + wait_times[i - 1]
            new_schedule.append({"task_name": second_part[i]["task_name"],
                                 "task_date": updated_date,
                                 "category": second_part[i]["category"]})
    new_schedule = first_part + new_schedule
    return new_schedule

def display_schedule(existing_schedule: list[dict]) -> None:
    """
    Display a schedule in a Tkinter window with an option to update it.

    Creates a new top-level window showing all tasks in chronological order.
    Each task is displayed as a formatted date and task name. An "Update"
    button opens a secondary interface that allows modification of the
    schedule. After modifications, the view is refreshed to reflect changes.

    Args:
        existing_schedule (list[dict]): Schedule to display. Each item must contain:
            - "task_name" (str): Name of the task.
            - "task_date" (datetime.datetime): Scheduled date/time.
            - "category" (str): Task category.

    Returns:
        None
    """
    view_schedule = tk.Toplevel()
    view_schedule.title("Schedule")
    def refresh_view_schedule():
        # Clear all widgets in the window
        for widget in view_schedule.winfo_children():
            widget.destroy()
        # Display tasks
        for task in existing_schedule:
            label = tk.Label(view_schedule, text=f"{task['task_date'].strftime('%d %b')}: {task['task_name']}")
            label.pack()
        # Update button
        update_button = tk.Button(
            view_schedule,
            text="Update",
            command=lambda: gui_alter_existing_schedule(existing_schedule, refresh_view_schedule) #refresh being passed as an argument to the subfunction, not called directly
        )
        update_button.pack()
    refresh_view_schedule()

class LabelledEntry(tk.Frame):
    """
    A composite Tkinter widget representing a single schedulable task.

    Displays a label, an editable entry field (pre-populated with a suggested
    value), and up to three action buttons. Intended for use in schedule
    editing interfaces where each row corresponds to a task.

    Args:
        parent (tk.Misc): Parent Tkinter container.
        name (str): Text displayed as the task label.
        suggestion (str): Default value inserted into the entry field.
        index (int): Index of the task in the schedule.
        button_text1 (str, optional): Text for the first button. Defaults to "Add".
        button_text2 (str, optional): Text for the second button. Defaults to "Update".
        button_text3 (str, optional): Text for the third button. Defaults to "Remove".
        command1 (Callable | None, optional): Callback bound to the first button.
        command2 (Callable | None, optional): Callback bound to the second button.
        command3 (Callable | None, optional): Callback bound to the third button.

    Attributes:
        index (int): Schedule index associated with this widget.
        label (tk.Label): Label displaying the task name.
        entry (tk.Entry): Entry widget for editing the task value.
        button1 (tk.Button): First action button.
        button2 (tk.Button): Second action button.
        button3 (tk.Button): Third action button.
    """
    def __init__(
        self,
        parent: tk.Misc,
        name: str,
        suggestion: str,
        index: int,
        button_text1: str = "Add",
        button_text2: str = "Update",
        button_text3: str = "Remove",
        command1: typing.Any = None,
        command2: typing.Any = None,
        command3: typing.Any = None,
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
        self.button2 = tk.Button(self, text=button_text2, command=command2)
        self.button3 = tk.Button(self, text=button_text3, command=command3)
        self.button1.grid(row=2, column=0)
        self.button2.grid(row=2, column=1)
        self.button3.grid(row=2, column=2)

    def get_entry(self) -> tuple[int, str]:
        return self.index, self.entry.get()

def gui_alter_existing_schedule(existing_schedule: list[dict], callback) -> None: #) -> None:
    """
    Open a Tkinter window to modify the dates of soft tasks in a schedule.

    Creates a top-level window displaying all tasks. "Soft" tasks are shown
    as editable entries with Add, Update, and Remove buttons. Updating a
    task recalculates downstream dates and refreshes the view. "Hard" tasks
    are displayed as static labels. A "Finish" button closes the window and
    triggers a callback to refresh any parent views.

    Args:
        existing_schedule (list[dict]): List of tasks to display and modify.
            Each task must include:
                - "task_name" (str): Name of the task.
                - "task_date" (datetime.datetime): Scheduled date/time.
                - "category" (str): Task category, e.g., "soft" or "hard".
        callback (Callable): Function called when the "Finish" button is pressed,
            typically used to refresh the parent schedule view.

    Returns:
        None
    """
    schedule_alterer = tk.Toplevel()
    schedule_alterer.title("schedule alterer")
    def refresh_alterer() -> None:
        counter = 0
        #clear the window
        for widget in schedule_alterer.winfo_children():
            widget.destroy()
        #recreate the window
        for s in existing_schedule:
            if s["category"] == "soft":
                widget = LabelledEntry(
                    schedule_alterer,
                    name=s["task_name"],
                    suggestion=str(s["task_date"].date()),
                    button_text1="Add",
                    button_text2="Update",
                    button_text3="Remove",
                    index=counter,
                )
            widget.button2.config(command=lambda w=widget: (trigger_schedule_alteration(w, existing_schedule), refresh_alterer())) #update schedule with new date
            widget.pack()
            if s["category"] == "hard":
                label = tk.Label(schedule_alterer, text=f"{s['task_name']}\n{str(s['task_date'].date())}")
                label.pack()
            counter += 1
        exit = tk.Button(schedule_alterer, text="Finish", command = lambda: (callback(), schedule_alterer.destroy()))
        exit.pack()
        schedule_alterer.grab_set()
    refresh_alterer()
    return None

def trigger_schedule_alteration(widget: LabelledEntry, input_schedule: list) -> None:
    """
    Update a schedule in place based on the entry from a LabelledEntry widget.

    Extracts the index and new date from the widget, applies the changes to
    the schedule using `alter_existing_schedule`, and updates the original
    schedule list in place so that any references to it remain valid.

    Args:
        widget (LabelledEntry): Widget containing the task to modify.
        input_schedule (list[dict]): Schedule to update. Each item must include:
            - "task_name" (str)
            - "task_date" (datetime.datetime)
            - "category" (str)

    Returns:
        None
    """
    index, new_date = widget.get_entry()
    updated_schedule: list[dict] = alter_existing_schedule(input_schedule, index, new_date)
    #update schedule in place
    input_schedule.clear()
    input_schedule.extend(updated_schedule)
    return None

def insert_into_schedule(existing_schedule: list[dict], index: int, new_task: dict) -> list[dict]:
    #add a new task into an existing schedule at a specified index
    return None

def remove_from_schedule():
    return None

def gui_add_task() -> dict:
    """
    Open a Tkinter window to create a new task with all relevant fields.

    Returns:
        dict: New task containing keys:
            - "task_name" (str)
            - "task_date" (datetime.date)
            - "category" (str)
            - "wait_time" (int | float)
    """
    new_task_window = tk.Toplevel()
    new_task_window.title("New Task")

    # Task name
    tk.Label(new_task_window, text="Task Name").pack()
    name_entry = tk.Entry(new_task_window)
    name_entry.pack()

    # Task date
    tk.Label(new_task_window, text="Task Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(new_task_window)
    date_entry.pack()

    # Category
    tk.Label(new_task_window, text="Category (soft/hard)").pack()
    category_var = tk.StringVar(value="soft")
    tk.OptionMenu(new_task_window, category_var, "soft", "hard").pack()

    # Wait time (hours)
    tk.Label(new_task_window, text="Wait Time (hours)").pack()
    wait_entry = tk.Entry(new_task_window)
    wait_entry.pack()

    task_result: dict = {}

    def submit_task():
        from datetime import datetime
        task_result["task_name"] = name_entry.get()
        task_result["task_date"] = datetime.fromisoformat(date_entry.get())
        task_result["category"] = category_var.get()
        task_result["wait_time"] = float(wait_entry.get())
        new_task_window.destroy()

    tk.Button(new_task_window, text="Add Task", command=submit_task).pack()

    # Wait for window to close
    new_task_window.grab_set()
    new_task_window.wait_window()

    return task_result

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main")

    test_schedule = [
        {"task_name": "transfection"},
        {"task_name": "media_change", "category": "hard", "wait_time": 24},
        {"task_name": "d3_harvest", "category": "soft", "wait_time": 48},
        {"task_name": "EP1", "category": "soft", "wait_time": 0},
        {"task_name": "EP1_harvest", "category": "hard", "wait_time": 72},
        {"task_name": "EP2", "category": "soft", "wait_time": 0},
        {"task_name": "EP2_harvest", "category": "hard", "wait_time": 72},
    ]
    test_schedule = initialise_schedule(test_schedule, dt.datetime.fromisoformat("2026-01-01"))
    display_schedule(test_schedule)
    #gui_add_task()
    root.mainloop()

    print("yay")