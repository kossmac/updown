document.addEventListener( 'DOMContentLoaded', function () {
    var datePicker = new DatePicker( document.getElementById( 'datepicker' ), {
        lang: 'de',
        startDate: new Date(),
        dataFormat: 'yyyy-mm-dd'
    } );
} );