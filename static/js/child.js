const sciences = document.querySelector('#sciences').innerHTML.split(', ');
const scienceSelect = document.querySelector('#science-select');

sciences.forEach(science => {
    scienceSelect.innerHTML += `
        <option value="${science}">${science}</option>
    `;
});

const informationButton = document.querySelector('.full-information-button');
const informationWindow = document.querySelector('.full-information-window');

informationButton.addEventListener('click', () => {
    informationWindow.classList.toggle('display-none');
});

const titleInput = document.querySelector('#title');
const selects = Array.from(document.querySelectorAll('select'));
const submitButton = document.querySelector('#add-button');

function checkForm() {
    if (
        titleInput.value.length != 0 &&
        selects.every(select => select.value != '')
    ) {
        submitButton.disabled = false
    } else {
        submitButton.disabled = true
    }
}

titleInput.addEventListener('input', checkForm);
selects.forEach(select => {
    select.addEventListener('change', checkForm);
});

document.querySelector('#new-achievement-button').addEventListener('click', () => {
    document.querySelector('#form-window').showModal();
});

document.querySelector('#close-dialog-button').addEventListener('click', () => {
    document.querySelector('#form-window').close();
});