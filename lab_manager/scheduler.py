import datetime as dt
import tkinter as tk
import typing

def initialise_schedule(input_schedule: list[dict], start_date: dt.date) -> list[dict]:
    final_schedule = []
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
    # change the schedule at index and update downstream requirements
    first_part = existing_schedule[0:index]
    second_part = existing_schedule[index:]
    # get gaps and flags for next parts. basically going to treat this like its own separate schedule
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
    view_schedule = tk.Toplevel()
    view_schedule.title("Schedule")
    def refresh():
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
            command=lambda: gui_alter_existing_schedule(existing_schedule, refresh)
        )
        update_button.pack()
    refresh()

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

def trigger_schedule_alteration(widget: LabelledEntry, input_schedule: list) -> None:
    # to be bound to a tkinter button
    index, new_date = widget.get_entry()
    updated_schedule: list[dict] = alter_existing_schedule(input_schedule, index, new_date)
    input_schedule.clear()
    input_schedule.extend(updated_schedule)
    #print(input_schedule)
    return None

def gui_alter_existing_schedule(existing_schedule: list[dict], callback: callable = None) -> None:
    schedule_alterer = tk.Toplevel()
    schedule_alterer.title("schedule alterer")
    counter = 0
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
        widget.button2.config(command=lambda w=widget: trigger_schedule_alteration(w, existing_schedule))
        widget.pack()
        if s["category"] == "hard":
            label = tk.Label(schedule_alterer, text=f"{s['task_name']}\n{str(s['task_date'].date())}")
            label.pack()
        counter += 1
    exit = tk.Button(schedule_alterer, text="Finish", command=lambda: [schedule_alterer.destroy(), callback() if callback else None])
    exit.pack()
    return None

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
    print(test_schedule)
    display_schedule(test_schedule)
    #gui_alter_existing_schedule(test_schedule)
    root.mainloop()
    print(test_schedule)

    print("yay")