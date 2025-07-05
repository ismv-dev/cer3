const togglePassword = document.getElementById('togglePassword');
const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const icon = document.getElementById('togglePasswordIcon');
const confirmIcon = document.getElementById('toggleConfirmPasswordIcon');

function changeButton(type){
    passwordInput.setAttribute('type', type);
    icon.classList.toggle('bi-eye');
    icon.classList.toggle('bi-eye-slash');
    confirmPasswordInput.setAttribute('type', type);
    confirmIcon.classList.toggle('bi-eye');
    confirmIcon.classList.toggle('bi-eye-slash');
}

togglePassword.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    changeButton(type)
});

toggleConfirmPassword.addEventListener('click', function () {
    const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    changeButton(type)
});