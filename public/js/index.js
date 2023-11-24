const links = document.querySelector('.links');

if (localStorage.length != 0) {
    links.innerHTML = `
        <a href="/child?id=${localStorage.getItem('id')}" class="link">Личный кабинет</a>
    `
}