function prepare_formdata(formSelector) {
    if (formSelector) {
        data = new FormData();
        //Form data
        var form_data = $(formSelector).serializeObject();
        console.log(form_data)
        $.each(form_data, function(key, value) {
            console.log(key, value);
            data.append(key, value);
        });

        //File data
        $(formSelector).find("input[type='file']").each(function(i, val) {
            var file_data = val.files;
            for (var i = 0; i < file_data.length; i++) {
                data.append("images" + i, file_data[i]);
            }
        });
        return data;
    } else {
        return data = new FormData();
    }
}

function prepare_stringifyData(data) {
    return data = JSON.stringify(data);
}

function jajax(url, type, data, formSelector) {
    if (formSelector) {
        data = prepare_formdata(formSelector)
    }
    return $.ajax({
        url: 'http://localhost:5000/' + url,
        contentType: false,
        processData: false,
        method: type,
        data: data
    }).done(function(data) {
        console.log('SUCCEEEEEEED', data);
    }).fail(function(jqXHR, textStatus, err) {
        console.log('Error: ' + err);
    }).always(function() {
        console.log('ALWAYS ');
    });
}

function ajax_data(url, method, data) {
    data = prepare_stringifyData(data);
    return $.ajax({
        url: 'http://localhost:5000/' + url,
        contentType: "application/json; charset=utf-8",
        method: method,
        data: data
    }).done(function(data) {
        console.log('SUCCEEEEEEED', data);
    }).fail(function(jqXHR, textStatus, err) {
        console.log('Error: ' + err);
    }).always(function() {
        console.log('ALWAYS ');
    });
}