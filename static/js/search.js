document.querySelector('#open-fitler-window').addEventListener('click', () => {
    document.querySelector('#fitler-window').showModal();
});

document.querySelector('#close-dialog-button').addEventListener('click', () => {
    document.querySelector('#fitler-window').close();
});

const minAgeLog = document.querySelector('#min-age-log');
const minAgeInput = document.querySelector('#min-age-input');
const maxAgeLog = document.querySelector('#max-age-log');
const maxAgeInput = document.querySelector('#max-age-input');

minAgeInput.addEventListener('input', () => {
    minAgeLog.innerHTML = minAgeInput.value;
    maxAgeInput.min = minAgeInput.value;
});

maxAgeInput.addEventListener('input', () => {
    maxAgeLog.innerHTML = maxAgeInput.value;
    minAgeInput.max = maxAgeInput.value;
});