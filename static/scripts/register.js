/**
 * Created by xiadd on 16/5/29.
 */
(function ($) {
    var password = document.querySelector('#password');
    var repeatPassword = document.querySelector('#repeat');
    var confirm = document.querySelector('button[type=submit]');

    repeatPassword.addEventListener('blur', function () {
        if(password.value !== this.value) {
            console.error('error');
            return;
        }
        confirm.removeAttribute('disabled');

    })
})($);