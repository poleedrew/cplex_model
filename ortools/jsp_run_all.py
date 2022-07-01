import os
import json
import collections
from ortools.sat.python import cp_model

def load_instance(filename):
    data = []
    
    f = open(filename)
    line = f.readline()
    while line[0] == '#':
        line = f.readline()
    line = line.split()
    num_job, num_machine = int(line[0]), int(line[1])

    for i in range(num_job):
        job_data = []
        line = f.readline().split()
        for j in range(num_machine):
            machine_id, processing_time = int(line[j * 2]), int(line[j * 2 + 1])
            # print('Machine', machine_id, 'processing_time:', processing_time)
            job_data.append((machine_id, processing_time))
        data.append(job_data)
    return data

def solve(file_name, time_limit=10.0, num_thread=1):
    result = []
    # jobs_data = [  # task = (machine_id, processing_time).
    #     [(0, 3), (1, 2), (2, 2)],  # Job0
    #     [(0, 2), (2, 1), (1, 4)],  # Job1
    #     [(1, 4), (2, 3)]  # Job2
    # ]
    jobs_data = load_instance(file_name)

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Creates the solver.
    solver = cp_model.CpSolver()
    # set limit
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = num_thread
    # solve
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('%s\t%f\t%f\t%r' %(
            file_name, 
            solver.ObjectiveValue(), solver.WallTime(), 
            bool(status == cp_model.OPTIMAL)))
        output_file_name = "result_thread_" + str(num_thread)
        with open(output_file_name, "a") as f:
            print('%s\t%f\t%f\t%r' %(
                  file_name,
                  solver.ObjectiveValue(), solver.WallTime(),
                  bool(status == cp_model.OPTIMAL)), file=f)
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                                       job=job_id,
                                       index=task_id,
                                       duration=task[1]))

        # Create per machine output lines.
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            for assigned_task in assigned_jobs[machine]:
                start = assigned_task.start
                duration = assigned_task.duration
                # Add spaces to output to align columns.
                op_info = {
                    'Order':        None,
                    'job_id':       assigned_task.job,
                    'op_id':        assigned_task.index,
                    'machine_id':   machine,
                    'start_time':   start,
                    'process_time': duration,
                    'finish_time':  start + duration,
                    'job_type':     None,
                }
                result.append(op_info)
    else:
        print('No solution found.')
    return result


if __name__ == '__main__':
    jsp_instance_dir = '../instances'
    time_limit = 30
    num_thread = 32
    for i in range(1,11):
        out_dir = '../thread_%d/test_%d/ortools_result_%d_%d'%(num_thread, i, num_thread, time_limit)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
    
        ### run all cases
        for i, fn in enumerate(os.listdir(jsp_instance_dir)):
             file_name = os.path.join(jsp_instance_dir, fn)
             result = solve(file_name, time_limit=time_limit, num_thread=num_thread)
             out_file = os.path.join(out_dir, fn+'.json')
             with open(out_file, 'w') as f:
                 json.dump(result, f, indent=4)

    ### run one case
    # file_name = 'instances/abz5'
    # time_limit = 6000
    # out_dir = 'ortools_result_%d' %(time_limit)
    # result = solve(file_name, time_limit=time_limit)

    ### run some cases
    # file_names = ['ta71', 'ta72', 'ta73', 'ta74', 'ta75', 'ta76', 'ta77', 'ta78', 'ta79', 'ta80']
    # time_limit = 60
    # num_trial = 100
    # for i, fn in enumerate(file_names):
    #   file_name = os.path.join(jsp_instance_dir, fn)
    #   for _ in range(num_trial):
    #       result = solve(file_name, time_limit=time_limit)
    #   print()
        # out_file = os.path.join(out_dir, fn+'.json')
        # with open(out_file, 'w') as f:
        #     json.dump(result, f, indent=4)

    ### possible number of threads control
    # solver.parameters.num_workers = 4
