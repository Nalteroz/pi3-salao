function fetchDataToTable(dataPath) {
    var table = document.getElementById('data-table');
    var thead = table.getElementsByTagName('thead')[0];
    var tbody = table.getElementsByTagName('tbody');

    fetch(dataPath)
    .then(response => response.json())
    .then( (data) => {
        if (data.length > 0) {
            document.getElementById('data-container').toggleAttribute('hidden');
            var headerList = ['id'].concat(Object.keys(data[0]).filter(key => key !== 'id'));
            COLUMNS_NAMES['id'] = 'ID';
            headerList.forEach((key) => {
                var th = document.createElement('th');
                th.innerHTML = COLUMNS_NAMES[key];
                thead.appendChild(th);
            });
            data.forEach( (dataRow) => {
                var tableRow = document.createElement('tr');
                headerList.forEach((key) => {
                    var cell = tableRow.insertCell();
                    cell.innerHTML = dataRow[key];
                });
                tbody[0].appendChild(tableRow);
            });
        };
    })
    .catch(error => console.error(error));
}

fetchDataToTable(DATA_PATH);