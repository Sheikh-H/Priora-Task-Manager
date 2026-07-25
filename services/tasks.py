from services.database import (
    all_tasks,
    find_task_by_id,
    find_tasks_by_date,
    find_tasks_after_date,
    toggle_task_complete,
    find_tasks_before_date,
)


def load_tasks(user):
    tasks = all_tasks(user)
    if tasks:
        return tasks
    return None


def search_task_by_id(task_id, user):
    user_id = user["user_id"]
    task = find_task_by_id(task_id, user_id)
    if task:
        return task
    return None


def search_tasks_by_date(date, user):
    query = f"{date}"
    user_id = user["user_id"]
    tasks = find_tasks_by_date(query, user_id)
    if tasks:
        return tasks
    return None


def search_upcoming_tasks(date_from, user):
    date_from = f"{date_from}"
    user_id = user["user_id"]
    tasks = find_tasks_after_date(date_from, user_id)
    if tasks:
        return tasks
    return None


def search_overdue_tasks(date, user):
    date = f"{date}"
    user_id = user["user_id"]
    tasks = find_tasks_before_date(date, user_id)
    if tasks:
        return tasks
    return None


def mark_as_complete(task_id, user):
    user_id = user["user_id"]
    task = toggle_task_complete(task_id, user_id)
    if task:
        return "Task marked complete!"
    return "Unable to update!"
