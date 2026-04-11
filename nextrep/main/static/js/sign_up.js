const form = document.getElementById('registrationForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

const showError = (input, message) => {
    const errorDisplay = document.getElementById(`${input.id}Error`);
    errorDisplay.innerText = message;
    input.classList.add('invalid');
};

const clearError = (input) => {
    const errorDisplay = document.getElementById(`${input.id}Error`);
    errorDisplay.innerText = '';
    input.classList.remove('invalid');
};

const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
    return re.test(email);
};

const validatePassword = (pw) => {
    const re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    return re.test(pw);
};

form.addEventListener('input', (e) => {
    if (e.target.id === 'email') {
        validateEmail(e.target.value) ? clearError(e.target) : showError(e.target, "Invalid email address");
    }
    if (e.target.id === 'password') {
        validatePassword(e.target.value) ? clearError(e.target) : showError(e.target, "Must be 8+ chars with uppercase and number");
    }
});

form.addEventListener('submit', (e) => {
    e.preventDefault();
    let isFormValid = true;

    if (!validateEmail(emailInput.value)) {
        showError(emailInput, "Please provide a valid email");
        isFormValid = false;
    }

    if (!validatePassword(passwordInput.value)) {
        showError(passwordInput, "Password does not meet requirements");
        isFormValid = false;
    }

    if (isFormValid) {
        alert("Form submitted successfully!");

        window.location.href = "log_in.html"; 
    }
});