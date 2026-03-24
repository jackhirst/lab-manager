import datetime as dt
import tkinter as tk
import typing


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
        button_text1 (str, optional): Text for the first button. Defaults to "Update".
        command1 (Callable | None, optional): Callback bound to the first button.

    Attributes:
        index (int): Schedule index associated with this widget.
        label (tk.Label): Label displaying the task name.
        entry (tk.Entry): Entry widget for editing the task value.
        button1 (tk.Button): First action button.
    """

    def __init__(
        self,
        parent: tk.Misc,
        name: str,
        suggestion: str,
        index: int,
        button_text1: str = "Update",
        command1: typing.Any = None,
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

        self.button1.grid(row=2, column=1)

    def get_entry(self) -> tuple[int, str]:
        return self.index, self.entry.get()


class Schedule:
    """
    Sstores an ordered list of tasks, where each task includes:
        - task_name (str): Identifier for the task.
        - task_date (datetime.datetime): Scheduled date and time.
        - category (str): Task type (e.g., "soft" or "hard").

    Responsibilities:
        - Generate a dated schedule from a template and start date.
        - Provide simple GUI interfaces for viewing and editing the schedule.

    Attributes:
        name (str): Name of the schedule.
        schedule (list[dict]): Internal list of scheduled tasks in chronological order.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def initialise_schedule(self, input_schedule: list[dict], start_date: dt.date) -> None:
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
                final_schedule.append(
                    {"task_name": input_schedule[i]["task_name"], "task_date": start_date, "category": "soft"}
                )
            else:
                previous_date = final_schedule[i - 1]["task_date"]
                new_date = previous_date + dt.timedelta(hours=input_schedule[i]["wait_time"])
                final_schedule.append(
                    {
                        "task_name": input_schedule[i]["task_name"],
                        "task_date": new_date,
                        "category": input_schedule[i]["category"],
                    }
                )
        self.schedule = final_schedule
        return None

    def alter_schedule(self, index: int, new_date: str) -> None:
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
        first_part: list[dict] = self.schedule[0:index]
        # get gaps and flags for next parts. basically going to treat this like its own separate schedule
        second_part: list[dict] = self.schedule[index:]
        dates = [x["task_date"] for x in second_part]
        wait_times = [dates[i + 1] - dates[i] for i in range(len(dates) - 1)]  # convert dates back into wait times
        new_schedule = []
        for i in range(len(second_part)):
            if i == 0:  # this is the task that's specifically being altered
                new_schedule.append(
                    {
                        "task_name": second_part[i]["task_name"],
                        "task_date": dt.datetime.fromisoformat(new_date),
                        "category": second_part[i]["category"],
                    }
                )
            else:
                previous_date = new_schedule[i - 1]["task_date"]
                updated_date = previous_date + wait_times[i - 1]
                new_schedule.append(
                    {
                        "task_name": second_part[i]["task_name"],
                        "task_date": updated_date,
                        "category": second_part[i]["category"],
                    }
                )
        new_schedule = first_part + new_schedule
        self.schedule = new_schedule

    def display_schedule(self) -> None:
        """
        Display a schedule in a Tkinter window.

        Creates a new top-level window showing all tasks in chronological order.
        Each task is displayed as a formatted date and task name.

        Returns:
            None
        """
        view_schedule = tk.Toplevel()
        view_schedule.title("Schedule")

        for task in self.schedule:
            label = tk.Label(view_schedule, text=f"{task['task_date'].strftime('%d %b')}: {task['task_name']}")
            label.pack()

        tk.Button(view_schedule, text="Finish", command=view_schedule.destroy).pack()

    def gui_alter_schedule(self) -> None:
        """
        Open a Tkinter window to modify "soft" task dates in the schedule.
        """
        window = tk.Toplevel()
        window.title("Schedule Alterer")

        def refresh() -> None:
            # clear window
            for widget in window.winfo_children():
                widget.destroy()

            for index, task in enumerate(self.schedule):
                if task["category"] == "soft":
                    entry = LabelledEntry(
                        window,
                        name=task["task_name"],
                        suggestion=str(task["task_date"].date()),
                        button_text1="Update",
                        index=index,
                    )

                    def handle_update(w: LabelledEntry = entry) -> None:
                        idx, new_date = w.get_entry()
                        self.alter_schedule(idx, new_date)
                        refresh()
                        return None

                    entry.button1.config(command=handle_update)
                    entry.pack()

                else:  # hard task
                    tk.Label(
                        window,
                        text=f"{task['task_name']}\n{task['task_date'].date()}",
                    ).pack()

            tk.Button(window, text="Finish", command=window.destroy).pack()
            window.grab_set()

        refresh()


class ScheduleManager:
    """
    Stores a list of Schedules and offers GUI interface to manage them.
    """

    def __init__(self, sched_list: list[Schedule]) -> None:
        self.schedule_list = sched_list
        counter: int = 0
        for schedule in self.schedule_list:
            s_label = tk.Label(root, text = schedule.name)
            s_label.grid(row = counter, column=0, padx = 5, pady =2)
            s_button_1 = tk.Button(root, text = "View", command = schedule.display_schedule)
            s_button_1.grid(row = counter, column = 1, padx = 2, pady =2)
            s_button_2 = tk.Button(root, text= "Update", command = schedule.gui_alter_schedule)
            s_button_2.grid(row = counter, column = 2, padx = 2, pady =2)
            counter += 1
        pass


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

    def submit_task() -> None:
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

    print(task_result)
    return task_result


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main")
    root.geometry("400x200")

    test_schedule: list[dict] = [
        {"task_name": "transfection"},
        {"task_name": "media_change", "category": "hard", "wait_time": 24},
        {"task_name": "d3_harvest", "category": "soft", "wait_time": 48},
        {"task_name": "EP1", "category": "soft", "wait_time": 0},
        {"task_name": "EP1_harvest", "category": "hard", "wait_time": 72},
        {"task_name": "EP2", "category": "soft", "wait_time": 0},
        {"task_name": "EP2_harvest", "category": "hard", "wait_time": 72},
    ]
    test1 = Schedule("test_schedule_1")
    test1.initialise_schedule(test_schedule, dt.datetime.fromisoformat("2026-01-01"))
    test2 = Schedule("test_schedule_2")
    test2.initialise_schedule(test_schedule, dt.datetime.fromisoformat("2026-02-01"))
    manager = ScheduleManager ([test1, test2])
    
    #test.alter_schedule(3, "2026-02-01")
    #test.display_schedule()
    #test.gui_alter_schedule()
    root.mainloop()
    print("yay")