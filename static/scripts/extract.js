(function ($) {
    var publicPath = '127.0.0.1/static'
    var extract = document.querySelector('.extract');
    var blockExtract = document.querySelector('.block-extract');

    extract.addEventListener('click', function () {
        $.ajax({
            url: '/extract',
            type: 'POST',
            data: {'action': 'extract'},
            dataType: 'json',
            success: function (res) {
                console.log(1)
                $('.result').append('<h3>提取结果</h3>')
                $('.result').append('<img src="../static/'+res.url+'">')
            },
            error: function (err) {
                console.log(err)
            }
        })
    })
    blockExtract.addEventListener('click', function () {
        $.ajax({
            url: '/extract',
            type: 'POST',
            data: {'action': 'extract', 'block': true},
            dataType: 'json',
            success: function (res) {
                console.log(1)
                $('.logo-result').append('<h3>提取结果</h3>')
                $('.logo-result').append('<img src="../static/'+res.url+'/logo.ld.png">');
                $('.logo-result').append('<img src="../static/'+res.url+'/logo.lu.png">');
                $('.logo-result').append('<img src="../static/'+res.url+'/logo.rd.png">');
                $('.logo-result').append('<img src="../static/'+res.url+'/logo.ru.png">');
            },
            error: function (err) {
                console.log(err)
            }
        })
    })
})($);