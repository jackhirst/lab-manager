'''
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
'''

import numpy as np

print("test")

class Task:
    def __init__(self, name):
        self.name = name
    runs = []
    fit = None

    def fit_time(self):
        xs = [x[0] for x in self.runs]
        ys = [x[1] for x in self.runs]
        coef = np.polyfit(xs,ys,1)
        self.fit = np.poly1d(coef)

transfection_task = Task("transfection")
transfection_task.runs = [[6, 90], [2, 30], [4,45]]
transfection_task.fit_time()

mediachange_task = Task("media_change")
mediachange_task.runs = [[6, 25], [2, 20], [4,25]]
mediachange_task.fit_time()

task_dict = {"transfection": transfection_task,
             "media_change": mediachange_task}

class Experiment:
    def __init__(self, name, start_date, schedule, sample_count):
        self.name = name
        self.start_date = start_date
        self.schedule = schedule
        self.sample_count = sample_count
    
    def initialise_schedule(self):
        final_schedule = []
        for i in range(len(self.schedule) + 1):
            if i == 0:
                first_task = self.schedule[0][0]
                final_schedule.append(first_task.name, self.start_date, first_task.fit(self.sample_count))
            else:
                task_date = "test"
        pass
    
    # def estimate_time(self):
    #     constituent_tasks = [x for x in task_list if x.name in self.constituent_task_names]
    #     estimated_task_lengths = [x.fit(self.sample_count) for x in constituent_tasks]
    #     self.estimated_time = sum(estimated_task_lengths)
    
'''
input = [
    ["transfection", first],
    ["media_change", hard, 24],
    ["d3_harvest", soft, 48],
    ["EP1", soft, 0],
    ["EP1_harvest", hard, 72],
    ["EP2", soft, 0],
    ["EP2 harvest", hard, 72]
]
'''

class Schedule:
    def __init__(self):
        pass
        '''
        items needs to have a task, a hard/soft/first flag, a hard date from previous (if appropriate), a date
        '''

rescue = Experiment("rescue", "2026-01-01", "REPLACEIWTHSCHEDULE", 8)

print("yay")