const btnTimer = document.querySelector('.countdown');
const btnMinutes = document.querySelector('.minutes');
const btnSeconds = document.querySelector('.seconds');
const btnMessage = document.querySelector('.message');

const btnPlus = document.querySelector('.plus');
const btnMinus = document.querySelector('.minus');
const btnStart = document.querySelector('.start');
const btnStop = document.querySelector('.stop');
const btnReset = document.querySelector('.reset');

const fieldSec = document.querySelector('[name=inputsec]');
const fieldMin = document.querySelector('[name=inputmin]');

const Grow = document.querySelector('#arrow::-webkit-inner-spin-button');

// общее время в секундах
// 3599 максимум секунд ( 59 минут 59 секунд)
let globalTimeSec = 0;
let nIntervId = null;

const changeNumberView = (value) => (value < 10) ? '0' + value : value;

// проверка допустимого значения таймера
const checkTime = () => {
    globalTimeSec = (globalTimeSec > 3599) ? 3599 : globalTimeSec;
    globalTimeSec = (globalTimeSec < 0) ? 0 : globalTimeSec;
}

// отрисовка таймера
function setTimer() {
    
    checkTime()

    let m = Math.trunc(globalTimeSec / 60);
    let s = globalTimeSec - m * 60;

    btnMinutes.innerText = changeNumberView(m);
    btnSeconds.innerText = changeNumberView(s);
}

setTimer()

// остановка таймера
function stopTimer() {
    clearInterval(nIntervId);
    nIntervId = null;
}

// если в input не нули, то прибавляем из полей ввода
// иначе добавляем секунду
btnPlus.addEventListener('click', () => {
    if (fieldMin.value == 0 & fieldSec.value == 0) {
        globalTimeSec++;
    } else {
        globalTimeSec += 60 * Number(fieldMin.value);
        globalTimeSec += Number(fieldSec.value);
        fieldMin.value = 0;
        fieldSec.value = 0;
    }
    setTimer();
});

btnMinus.addEventListener('click', () => {
    if (fieldMin.value == 0 & fieldSec.value == 0) {
        globalTimeSec--;
    } else {
        globalTimeSec -= 60 * Number(fieldMin.value);
        globalTimeSec -= Number(fieldSec.value);
        fieldMin.value = 0;
        fieldSec.value = 0;
    }
    setTimer();
});

btnStart.addEventListener('click', () => {
    btnMessage.innerText = '';

    if (globalTimeSec > 0 & (!nIntervId)) {
        nIntervId = setInterval(() => {
            if (globalTimeSec > 0) {
                globalTimeSec--;
            } else {
                btnMessage.innerText = "Таймер успешно отработал";
                clearInterval(nIntervId); //останавливаю счетчик
                nIntervId = null; //чтоб снова нажать на старт
            }
            setTimer();
        }, 1000)
    }
});

// останавливаем выполнение тамера
btnStop.addEventListener('click', stopTimer)

btnReset.addEventListener('click', () => {
    globalTimeSec = 0;
    fieldMin.value = 0;
    fieldSec.value = 0;
    btnMinutes.innerText = '00';
    btnSeconds.innerText = '00';
});
