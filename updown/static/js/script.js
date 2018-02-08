document.addEventListener('DOMContentLoaded', function () {
    var impersonate_select = document.getElementById('impersonate_select');
    if (impersonate_select) {
        impersonate_select.onchange = function (ev) {
            window.open(window.location.origin + '/impersonate/' + this.selectedOptions["0"].value, '_self');
        };
    }
    var file = document.getElementById("file");
    file.onchange = function () {
        if (file.files.length > 0) {
            document.getElementById('filename').innerHTML = file.files[0].name;
        }
    };
});