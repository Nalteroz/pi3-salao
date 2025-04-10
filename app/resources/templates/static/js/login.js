function Login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Try to login on /user/login endpoint
    fetch('api/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.login === true) {
            window.location.href = '/';
        } else {
            document.getElementById('error-message').innerHTML = 'Invalid email or password';
        }
    })
    .catch((error) => {
        document.getElementById('error-message').innerHTML = 'Invalid email or password';
    });
}