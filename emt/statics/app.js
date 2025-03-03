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

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('work-table');
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    let draggedRow = null;
    
    // 各行にイベントリスナーを追加
    rows.forEach(row => {
        // ドラッグ開始時
        row.addEventListener('dragstart', function(e) {
            draggedRow = this;
            // ドラッグ中のスタイル適用
            setTimeout(() => {
                this.classList.add('dragging');
            }, 0);
        });
        
        // ドラッグ終了時
        row.addEventListener('dragend', function() {
            this.classList.remove('dragging');
            draggedRow = null;
            
            // テーブルの順序が変更されたらサーバーに通知
            saveTableOrder();
        });
        
        // ドラッグオーバー時（他の要素の上にドラッグ）
        row.addEventListener('dragover', function(e) {
            e.preventDefault(); // デフォルトの動作をキャンセル
        });
        
        // ドロップ可能領域に入ったとき
        row.addEventListener('dragenter', function(e) {
            e.preventDefault();
            if (draggedRow !== this) {
                // ドラッグ中の行と現在の行の位置関係を調べる
                const rect = this.getBoundingClientRect();
                const y = e.clientY - rect.top;
                const height = rect.height;
                
                // カーソルが行の上半分にあるか下半分にあるかで挿入位置を決定
                if (y < height / 2) {
                    tbody.insertBefore(draggedRow, this);
                } else {
                    tbody.insertBefore(draggedRow, this.nextSibling);
                }
            }
        });
    });
    
    // 行の順序変更後にデータを保存する関数
    function saveTableOrder() {
        const rows = tbody.querySelectorAll('tr');
        const timerOrder = Array.from(rows).map(row => {
            // Extract the timer ID from the row id (row{id})
            const rowId = row.id;
            const timerId = rowId.replace('row', '');
            return parseInt(timerId);
        });
        
        // If no changes or only one row, don't send update
        if (timerOrder.length <= 1) {
            return;
        }
        
        // Get the CSRF token for Django
        const csrftoken = getCookie('csrftoken');
        
        // Send the new order to the server
        fetch('/reorder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                timer_order: timerOrder
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Reordered timers successfully');
                // Optional: Reload the page to show the updated order
                window.location.reload();
            } else {
                console.error('Error reordering timers:', data.error);
            }
        })
        .catch(error => {
            console.error('Error reordering timers:', error);
        });
    }
});