const passwordField = document.getElementById('passwordField');
const toggleCheckbox = document.getElementById('togglePassword');

toggleCheckbox.addEventListener('change', function() {
    if (this.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
});