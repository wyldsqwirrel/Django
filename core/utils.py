# core/utils.py
def get_pomodoro_context():
    """
    Returns context data for the Pomodoro timer, including durations in seconds.
    """
    return {
        'work_duration': 25 * 60,  # Work duration in seconds (25 minutes)
        'break_duration': 5 * 60,  # Break duration in seconds (5 minutes)
        'initial_phase': 'work',   # Start in the work phase
    }
