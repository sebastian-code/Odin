$(document).ready(function () {
    $('textarea').on('keypress', function () {
        $('#has-error').hide();
    });
    $('textarea').on('click', function () {
        $('#has-error').hide();
    });
});
