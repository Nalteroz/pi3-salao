function RefineData(data) {
    var new_data = Object.keys(data).filter(objKey =>
        objKey !== 'id').reduce((newObj, key) =>
        {
            newObj[key] = data[key];
            return newObj;
        }, {}
    );
    return new_data;
}

function UpdateElement() {
    var inputs = document.getElementsByClassName('form-input');

    var data_payload = {};
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name == 'role' || inputs[i].name == 'type') {
            data_payload[inputs[i].name] = inputs[i].value.toUpperCase();
        } else { 
            data_payload[inputs[i].name] = inputs[i].value.replace(',', '.');
        }
    }
    fetch(DATA_PATH + '/' + data_payload['id'], {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(RefineData(data_payload))
    })
    .then((response) => { 
        console.log(response);
        if (response.status == 200) {
            window.location.href = ('/element/' + ELEMENT);
        } else {
            document.getElementById('error-message').innerHTML = 'Dados inválidos';
        }
    })
    .catch((error) => {
        document.getElementById('error-message').innerHTML = 'Invalid email or password';
    });
}