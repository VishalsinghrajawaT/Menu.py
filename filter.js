document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload-photo');
    const imagePreview = document.getElementById('image-preview');
    const captionInput = document.getElementById('caption');
    const postButton = document.getElementById('post-button');
    const captureGrid = document.getElementById('captureGrid');

    let uploadedImage = null;

    // Handle image upload and preview
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                postButton.style.display = 'block'; // Show post button
                uploadedImage = file; // Store the uploaded image
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle posting image with caption
    postButton.addEventListener('click', () => {
        if (!uploadedImage) {
            alert('Please upload an image first.');
            return;
        }

        const formData = new FormData();
        formData.append('image', uploadedImage);
        formData.append('caption', captionInput.value);
        formData.append('filter', document.querySelector('input[name="filter"]:checked').value);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add the filtered image to the grid
                const img = document.createElement('img');
                img.src = data.filteredImageUrl;
                img.alt = 'Filtered Image';
                img.className = 'captureBox';
                captureGrid.appendChild(img);
            } else {
                alert('Error uploading image.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error uploading image.');
        });
    });
});
