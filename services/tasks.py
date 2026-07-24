from services.database import all_tasks


def load_tasks(user):
    tasks = all_tasks(user)
    if tasks:
        return tasks
    return None
