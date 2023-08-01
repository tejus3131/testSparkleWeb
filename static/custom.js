function updateTime() {
    const clockElement = document.getElementById('clock');
    if (!clockElement || clockElement == null) {
        setTimeout(() => {
            updateTime();
          }, 100);
        return;
    }
    const startDateTime = new Date(clockElement.dataset.currentTime);

    function updateClock() {
        const currentTime = new Date();
        const timeDifference = currentTime - startDateTime;
        const hours = String(Math.floor(timeDifference / 3600000)).padStart(2, '0');
        const minutes = String(Math.floor((timeDifference % 3600000) / 60000)).padStart(2, '0');
        const seconds = String(Math.floor((timeDifference % 60000) / 1000)).padStart(2, '0');
        const timePassedString = `${hours}:${minutes}:${seconds}`;
        clockElement.innerText = `Server is running for ${timePassedString}.`;
    }
    updateClock();
    setInterval(updateClock, 1000);
}

updateTime();