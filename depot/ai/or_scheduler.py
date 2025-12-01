from ortools.sat.python import cp_model
from datetime import timedelta
from django.utils.timezone import now
from depot.models import Trainset, Bay  # adjust import path
from .induction_rules import compute_train_priority

def schedule_induction():
    model = cp_model.CpModel()
    current_time = now()

    trains = list(Trainset.objects.all())
    bays = list(Bay.objects.all())

    num_trains = len(trains)
    num_bays = len(bays)

    start_vars = []
    end_vars = []
    assign = {}

    # Create decision variables
    for i, train in enumerate(trains):
        start = model.NewIntVar(0, 1440, f"start_{train.id}")
        end   = model.NewIntVar(0, 1440, f"end_{train.id}")

        start_vars.append(start)
        end_vars.append(end)

        for b, bay in enumerate(bays):
            assign[(i, b)] = model.NewBoolVar(f"assign_t{train.id}_b{bay.id}")

    # Constraints
    for i, train in enumerate(trains):
        priority, _ = compute_train_priority(train)

        duration = 30  # minutes per induction
        model.Add(end_vars[i] == start_vars[i] + duration)

        # One bay per train
        model.Add(sum(assign[(i, b)] for b in range(num_bays)) == 1)

        # Bay capacity rule
        for b, bay in enumerate(bays):
            if train.cars > bay.capacity:
                model.Add(assign[(i, b)] == 0)

    # Avoid bay overlaps
    for b in range(num_bays):
        for i in range(num_trains):
            for j in range(i + 1, num_trains):
                no_overlap = model.NewBoolVar("")

                model.Add(end_vars[i] <= start_vars[j]).OnlyEnforceIf(no_overlap)
                model.Add(end_vars[j] <= start_vars[i]).OnlyEnforceIf(no_overlap.Not())

                model.AddBoolOr([
                    assign[(i, b)].Not(),
                    assign[(j, b)].Not(),
                    no_overlap
                ])

    # Objective: maximize priority - waiting time
    objective_terms = []

    for i, train in enumerate(trains):
        priority, _ = compute_train_priority(train)
        objective_terms.append(priority * 10 - start_vars[i])

    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10

    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return None

    # Build schedule
    plan = []

    for i, train in enumerate(trains):
        assigned_bay = None
        for b, bay in enumerate(bays):
            if solver.Value(assign[(i, b)]) == 1:
                assigned_bay = bay.name

        priority, reasons = compute_train_priority(train)

        plan.append({
            "train": train.number,
            "train_name": train.train_name,
            "bay": assigned_bay,
            "start_min": solver.Value(start_vars[i]),
            "end_min": solver.Value(end_vars[i]),
            "priority": priority,
            "reasons": reasons,
        })

    return plan
