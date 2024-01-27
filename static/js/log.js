const redirectLog = document.getElementById('log');
const redirectSignUp = document.getElementById('signup');
const registerLink = document.querySelector('.register-link');
const wrapper = document.querySelector('.wrapper');
const loginlink = document.querySelector('.login-link')

redirectLog.onclick = (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('pass').value;

    if (username && password) {
        redirectToMainPage();
    } else {
        alert('Please fill in all fields for Sign Up.');
    }
};

registerLink.onclick = () => {
    wrapper.classList.add('active');
};
loginlink.onclick = () => {
    wrapper.classList.remove('active');
};

redirectSignUp.onclick = (event) => {
    event.preventDefault();
    const signUpUsername = document.getElementById('signUpUsername').value;
    const email = document.getElementById('email').value;
    const signUpPassword = document.getElementById('signUpPass').value;

    // Validate the input (you can add more validation as needed)
    if (signUpUsername && email && signUpPassword) {
        // Redirect to the main page
        redirectToMainPage();
    } else {
        alert('Please fill in all fields for Sign Up.');
    }
};

function redirectToMainPage() {
    // Change the URL to the desired destination (your Flask route for the main page)
    var destinationURL = "/index_html";
    window.location.href = destinationURL;
}
