from datetime import datetime, timedelta

def parse_time(t):
    return datetime.strptime(t, '%I:%M %p')  # adjust format if needed

def duration_in_minutes(start, end):
    delta = parse_time(end) - parse_time(start)
    return delta.total_seconds() / 60

def validate_schedule(schedule, tasks, free_time, total_available_minutes):
    # schedule: dict day -> list of (task, start_time, end_time, duration)
    # tasks: dict task -> expected total duration (in minutes)
    # free_time: dict day -> list of (start_time, end_time)
    # total_available_minutes: int

    scheduled_time_sum = 0
    task_time_accum = {task: 0 for task in tasks}

    for day, slots in schedule.items():
        # Validate slots fit in free time ranges
        day_free_ranges = free_time.get(day, [])
        for task, start, end, duration in slots:
            # Check slot duration
            dur = duration_in_minutes(start, end)
            if abs(dur - duration) > 1:  # allow 1 minute tolerance
                print(f"Duration mismatch for {task} on {day}: expected {duration}, got {dur}")
                return False

            # Check slot in free time range
            in_free = any(
                parse_time(start) >= parse_time(f_start) and parse_time(end) <= parse_time(f_end)
                for f_start, f_end in day_free_ranges
            )
            if not in_free:
                print(f"Task {task} scheduled outside free time on {day}")
                return False

            # Accumulate time
            scheduled_time_sum += dur
            task_time_accum[task] += dur

        # Check no overlapping slots within day (optional: implement interval overlap check)

    # Check total scheduled time does not exceed availability
    if scheduled_time_sum > total_available_minutes:
        print(f"Total scheduled time {scheduled_time_sum} exceeds available {total_available_minutes}")
        return False

    # Check each task matches expected duration
    for task, expected in tasks.items():
        if abs(task_time_accum[task] - expected) > 1:
            print(f"Task {task} total duration mismatch: expected {expected}, got {task_time_accum[task]}")
            return False

    print("Schedule validated successfully")
    return True
