(function ($) {
    var imageUpload = document.querySelector('.upload-image');
    var logoUpload = document.querySelector('.upload-logo');
    var imagePreview = document.querySelector('.image-preview');
    var logoPreview = document.querySelector('.logo-preview');

    var Filter = /^(?:image\/bmp|image\/cis\-cod|image\/gif|image\/ief|image\/jpeg|image\/jpeg|image\/jpeg|image\/pipeg|image\/png|image\/svg\+xml|image\/tiff|image\/x\-cmu\-raster|image\/x\-cmx|image\/x\-icon|image\/x\-portable\-anymap|image\/x\-portable\-bitmap|image\/x\-portable\-graymap|image\/x\-portable\-pixmap|image\/x\-rgb|image\/x\-xbitmap|image\/x\-xpixmap|image\/x\-xwindowdump)$/i;

    function imageChange() {
        var readImage = new FileReader();
        readImage.onload = function (fileSrc) {
            imagePreview.setAttribute('src', fileSrc.target.result);
        };

        if(imageUpload.files.length === 0) return ;
        var image = imageUpload.files[0];
        if(!Filter.test(image.type)){
            alert('选择正确的文件格式');
            return ;
        }
        readImage.readAsDataURL(image)
    }
    function logoChange() {
        var readLogo = new FileReader();
        readLogo.onload = function (fileSrc) {
            var _img = new Image();
            _img.src = fileSrc.target.result;
            _img.onload = function () {
                var w = this.width;
            };
            logoPreview.setAttribute('src', fileSrc.target.result);
        };

        if(logoUpload.files.length === 0) return ;
        var logo = logoUpload.files[0];
        if(!Filter.test(logo.type)){
            alert('选择正确的文件格式');
            return ;
        }
        readLogo.readAsDataURL(logo)
    }

    imageUpload.addEventListener('change', imageChange);
    logoUpload.addEventListener('change', logoChange);

    imagePreview.addEventListener('click', function () {
        imageUpload.click();
    });

    logoPreview.addEventListener('click', function () {
        logoUpload.click();
    });
    

})($);