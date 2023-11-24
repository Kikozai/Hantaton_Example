const firstName = document.querySelector('[name="firstName"]');
const secondName = document.querySelector('[name="secondName"]');
const surname = document.querySelector('[name="surname"]');
const password = document.querySelector('[name="password"]');
const passwordError = document.querySelector('[name="password"]~.error');
const age = document.querySelector('[name="age"]');
const ageError = document.querySelector('[name="age"]~.error');
const sciences = document.querySelector('[name="sciences"]');
const sciencesMenu = document.querySelector('.sciences-menu');
const email = document.querySelector('[name="email"]');
const emailError = document.querySelector('[name="email"]~.error');
const phoneNumber = document.querySelector('[name="phoneNumber"]');
const phoneNumberError = document.querySelector('[name="phoneNumber"]~.error');
const submitButton = document.querySelector('.button');

const sciencesList = ['Русский', 'Математика', 'Физика', 'Химия', 'История', 'Обществознание', 'Информатика', 'Биология', 'География', 'Английский язык', 'Немецкий язык', 'Французкий язык', 'Испанский язык', 'Китайский язык', 'Литература'];

sciencesList.forEach(science => {
    document.querySelector('.sciences-menu ul').innerHTML += `
        <li>
            <label class="science">
                <input type="checkbox" ${sciences.value.includes(science) ? 'checked' : ''}>
                <span>${science}</span>
            </label>
        </li>
    `
});

document.querySelectorAll('[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        sciences.value = Array.from(document.querySelectorAll('input:checked~span')).map(node => node.innerHTML).join(', ')
    });
});

sciences.addEventListener('click', () => {
    sciencesMenu.classList.toggle('display-none');
});

function checkForm() {
    if (
        firstName.value.length != 0 &&
        secondName.value.length != 0 &&
        passwordIsValid() &&
        ageIsValid() &&
        sciences.value.length != 0 &&
        emailIsValud() &&
        (phoneNumber.value.length == 0 || phoneNumberIsValid())
    ) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true
    }
}

function passwordIsValid() {
    return password.value.length >= 8;
}

function ageIsValid() {
    return /^\d\d?$/.test(age.value);
}

function emailIsValud() {
    return /^\S+@\w+\.\w+$/.test(email.value);
}

function phoneNumberIsValid() {
    return /^\+\d\(\d\d\d\)\d\d\d-\d\d-\d\d$/.test(phoneNumber.value)
}

firstName.addEventListener('input', checkForm);
secondName.addEventListener('input', checkForm);
surname.addEventListener('input', checkForm);
password.addEventListener('input', checkForm);
age.addEventListener('input', checkForm);
sciences.addEventListener('input', checkForm);
email.addEventListener('input', checkForm);
phoneNumber.addEventListener('input', checkForm);

password.addEventListener('change', () => {
    if (passwordIsValid() || password.value.length == 0) {
        passwordError.classList.add('opacity-0');
    } else {
        passwordError.classList.remove('opacity-0');
    }
});

age.addEventListener('change', () => {
    if (ageIsValid() || age.value.length == 0) {
        ageError.classList.add('opacity-0');
    } else {
        ageError.classList.remove('opacity-0');
    }
});

email.addEventListener('change', () => {
    if (emailIsValud() || email.value.length == 0) {
        emailError.classList.add('opacity-0');
    } else {
        emailError.classList.remove('opacity-0');
    }
});

phoneNumber.addEventListener('change', () => {
    if (phoneNumberIsValid() || phoneNumber.value.length == 0) {
        phoneNumberError.classList.add('opacity-0');
    } else {
        phoneNumberError.classList.remove('opacity-0');
    }
});