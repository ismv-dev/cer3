const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const icon = document.getElementById('togglePasswordIcon');

function changeButton(type){
    passwordInput.setAttribute('type', type);
    icon.classList.toggle('bi-eye');
    icon.classList.toggle('bi-eye-slash');
}

togglePassword.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    changeButton(type)
});