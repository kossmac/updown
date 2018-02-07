document.addEventListener('DOMContentLoaded', function () {
    var datePicker = new DatePicker(document.getElementById('datepicker'), {
        lang: 'de',
        startDate: new Date(),
        dataFormat: 'yyyy-mm-dd'
    });

    // Get all "navbar-burger" elements
    var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(function ($el) {
            $el.addEventListener('click', function () {

                // Get the target from the "data-target" attribute
                var target = $el.dataset.target;
                var $target = document.getElementById(target);

                // Toggle the class on both the "navbar-burger" and the "navbar-menu"
                $el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }

    var impersonate_select = document.getElementById('impersonate_select');
    impersonate_select.onchange = function (ev) {
        window.open(window.location.origin + '/impersonate/' + this.selectedOptions["0"].value, '_self');
    }
});