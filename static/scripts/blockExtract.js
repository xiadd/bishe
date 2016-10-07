/**
 * Created by xiadd on 16/6/2.
 */
(function ($) {
    var publicPath = '127.0.0.1/static'
    var extract = document.querySelector('.extract');
    extract.addEventListener('click', function () {
        $.ajax({
            url: '/extract',
            type: 'POST',
            data: {'action': 'extract'},
            dataType: 'json',
            success: function (res) {
                console.log(1)
                $('.logo-result').append('<p>提取结果</p>')
                $('.logo-result').append('<img src="../static/'+res.url+'">')
            },
            error: function (err) {
                console.log(err)
            }
        })
    })
})($);