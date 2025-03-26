document.addEventListener("DOMContentLoaded", () => {
    // Initialize Pomodoro Timer
    const pomodoro = {
        duration: 25 * 60,
        remaining: 25 * 60,
        timer: null,
        isPaused: true,

        updateDisplay() {
            document.getElementById("pomodoro-timer").textContent = this.formatTime(this.remaining);
        },

        formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        },

        start() {
            if (!this.isPaused) return;
            this.isPaused = false;
            this.timer = setInterval(() => {
                if (this.remaining > 0) {
                    this.remaining--;
                    this.updateDisplay();
                } else {
                    clearInterval(this.timer);
                    alert("Pomodoro complete!");
                }
            }, 1000);
        },

        pause() {
            this.isPaused = true;
            clearInterval(this.timer);
        },

        reset() {
            this.pause();
            this.remaining = this.duration;
            this.updateDisplay();
        },
    };

    document.getElementById("startPomodoro").addEventListener("click", () => pomodoro.start());
    document.getElementById("pausePomodoro").addEventListener("click", () => pomodoro.pause());
    document.getElementById("resetPomodoro").addEventListener("click", () => pomodoro.reset());

    pomodoro.updateDisplay();

    // Initialize FullCalendar
    const calendarEl = document.getElementById("calendar");
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
    });
    calendar.render();
});