function DeleteElement() {
    var Idinput = document.getElementById('id-input');
    var elementId = Idinput.value;

    fetch(DATA_PATH + '/' + elementId, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response) => { 
        console.log(response);
        if (response.status == 201) {
            window.location.href = ('/element/' + ELEMENT);
        } else {
            document.getElementById('error-message').innerHTML = 'Dados inválidos';
        }
    })
    .catch((error) => {
        document.getElementById('error-message').innerHTML = 'Invalid email or password';
    });
}