function CreateElement() {
    var inputs = document.getElementsByClassName('form-input');

    var data_payload = {};
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name == 'role' || inputs[i].name == 'type') {
            data_payload[inputs[i].name] = inputs[i].value.toUpperCase();
        } else { 
            data_payload[inputs[i].name] = inputs[i].value.replace(',', '.');
        }
    }
    fetch(DATA_PATH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_payload)
    })
    .then((response) => { 
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