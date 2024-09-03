document.getElementById('upload1').addEventListener('change', function(event) {
    previewImage(event.target.files[0], 'image1');
});

document.getElementById('upload2').addEventListener('change', function(event) {
    previewImage(event.target.files[0], 'image2');
});

document.getElementById('swapButton').addEventListener('click', function() {
    swapImages();
});

function previewImage(file, imageId) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.getElementById(imageId);
        img.src = e.target.result;
        img.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function swapImages() {
    const image1Src = document.getElementById('image1').src;
    const image2Src = document.getElementById('image2').src;

    if (image1Src && image2Src) {
        document.getElementById('swappedImage').src = image2Src;
        document.getElementById('swappedImage').style.display = 'block';
    } else {
        alert('Please upload images in both boxes before swapping.');
    }
}
