document.addEventListener('DOMContentLoaded', function() {
    flatpickr('#id_start_date', {
        enableTime: false,
        dateFormat: 'Y-m-d',
        locale: 'ru',
        altInput: true,
        altFormat: 'F j, Y'
    });
    flatpickr('#id_end_date', {
        enableTime: false,
        dateFormat: 'Y-m-d',
        locale: 'ru',
        altInput: true,
        altFormat: 'F j, Y'
    });
    flatpickr('#id_start_time', {
        enableTime: true,
        dateFormat: 'Y-m-d H:i',
        time_24hr: true,
        locale: 'ru',
        altInput: true,
        altFormat: 'F j, Y H:i'
    });
    flatpickr('#id_end_time', {
        enableTime: true,
        dateFormat: 'Y-m-d H:i',
        time_24hr: true,
        locale: 'ru',
        altInput: true,
        altFormat: 'F j, Y H:i'
    });
});
