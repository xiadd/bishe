(function ($) {
    var imageUpload = document.querySelector('.upload-image');
    var imagePreview = document.querySelector('.image-preview');

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

    imageUpload.addEventListener('change', imageChange);

    imagePreview.addEventListener('click', function () {
        imageUpload.click();
    });

})($);