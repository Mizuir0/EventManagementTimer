// For individual timer
const timers = {};
let delay = 0;
let delayTimer;

function startTimer(timerId) {
    const initialMinutes = parseInt(document.getElementById(`initialMinutes${timerId}`).innerText) || 0;

    timers[timerId] = {
        timer: setInterval(() => updateTimer(timerId), 1000),
        isTimerRunning: true,
        hours: 0,
        minutes: initialMinutes,
        seconds: 0,
        pause: document.getElementById(`pause${timerId}`),
        resume: document.getElementById(`resume${timerId}`),
        nextTimer: document.getElementById(`next${timerId}`),
    };

    document.getElementById('defaultTimer').classList.add('d-none');
    document.getElementById(`current${timerId}`).classList.remove('d-none');
    document.getElementById(`row${timerId}`).classList.add('table-danger');

    if (document.getElementById(`next${parseInt(timerId)+1}`)) {
        document.getElementById(`next${parseInt(timerId)+1}`).classList.remove('d-none');
    }

    if ( delay != 0) {
        delayUpdate(timerId);
        document.getElementById(`delayTimer${timerId}`).classList.remove('d-none');
    }
}

function updateTimer(timerId) {
    let timer = timers[timerId];

    // Check if the timer is running
    if (timer.isTimerRunning) {
        timer.seconds--;

        if (timer.seconds < 0) {
            timer.seconds = 59;
            timer.minutes--;

            if (timer.minutes < 0) {
                timer.minutes = 59;
                timer.hours--;

                if (timer.hours < 0) {
                    clearInterval(timer.timer);
                    timer.isTimerRunning = false;
                    timerComplete(timerId);
                    return;
                }
            }
        }

        updateTimerDisplay(timerId);
    }
}

function pauseTimer(timerId) {
    const timer = timers[timerId];

    if (timer.isTimerRunning) {
        clearInterval(timer.timer);
        timer.isTimerRunning = false;
        timer.pause.classList.add('d-none');
        timer.resume.classList.remove('d-none');
        delayTimer = setInterval(pause, 1000, timerId);
    }
}

function resumeTimer(timerId) {
    const timer = timers[timerId];

    if (!timer.isTimerRunning) {
        clearInterval(delayTimer);
        timer.timer = setInterval(() => updateTimer(timerId), 1000);
        timer.isTimerRunning = true;
        timer.pause.classList.remove('d-none');
        timer.resume.classList.add('d-none');
    }
}

function skipTimer(timerId) {
    const timer = timers[timerId];

    if (!timer.isTimerRunning) {
        clearInterval(delayTimer);
    }
    clearInterval(timer.timer);
    timer.isTimerRunning = false;
    delay -= (timer.seconds + (timer.minutes * 60));
    timerComplete(timerId);
}

function timerComplete(timerId) {
    document.getElementById(`current${timerId}`).classList.add('d-none');
    document.getElementById(`row${timerId}`).classList.remove('table-danger');

    if (document.getElementById(`next${parseInt(timerId)+1}`)) {
        document.getElementById(`next${parseInt(timerId)+1}`).classList.add('d-none');
        document.getElementById(`row${parseInt(timerId)+1}`).classList.add('table-danger');

        startTimer(parseInt(timerId) + 1);
    } else {
        document.getElementById('defaultTimer').classList.remove('d-none');
        document.getElementById(`delayTimer${timerId}`).classList.add('d-none');
        delay = 0;
    }
}

function updateTimerDisplay(timerId) {
    let timer = timers[timerId];
    const formattedMinutes = padTime(timer.minutes);
    const formattedSeconds = padTime(timer.seconds);

    document.getElementById(`minutes${timerId}`).innerText = formattedMinutes;
    document.getElementById(`seconds${timerId}`).innerText = formattedSeconds;
}

function pause(timerId) {
    delay++;
    delayUpdate(timerId);
}

function delayUpdate(timerId) {
    const delayText = document.getElementById(`delay${timerId}`);
    
    document.getElementById(`delay-minutes${timerId}`).textContent = padTime(Math.abs(delay / 60 | 0));
    document.getElementById(`delay-seconds${timerId}`).textContent = padTime(Math.abs(delay % 60));
    
    if (delay < 0) {
        delayText.textContent = "巻き";
        document.getElementById(`delayTimer${timerId}`).classList.remove('d-none');
    } else if (delay == 0) {
        document.getElementById(`delayTimer${timerId}`).classList.add('d-none');
    } else {
        delayText.textContent = "押し";
        document.getElementById(`delayTimer${timerId}`).classList.remove('d-none');
    }
}

function padTime(time) {
    return (time < 10) ? `0${time}` : time;
}