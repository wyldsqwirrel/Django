
def pomodoro_timer(request):
    # Basic Pomodoro settings (you can make this dynamic later)
    pomodoro_settings = {
        'work_duration': 25,  # Work duration in minutes
        'break_duration': 5,  # Break duration in minutes
        'is_running': False,  # Example: whether the timer is currently running
    }
    return {
        'pomodoro': pomodoro_settings
    }
