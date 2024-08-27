// Access the webcam
const video = document.getElementById('video');
const captureButton = document.getElementById('captureButton');
const captureBoxes = [
    document.getElementById('captureBox1'),
    document.getElementById('captureBox2'),
    document.getElementById('captureBox3'),
    document.getElementById('captureBox4')
];
const imageElements = [
    document.getElementById('image1'),
    document.getElementById('image2'),
    document.getElementById('image3'),
    document.getElementById('image4')
];
const downloadLinks = [
    document.getElementById('download1'),
    document.getElementById('download2'),
    document.getElementById('download3'),
    document.getElementById('download4')
];
let captureIndex = 0;

// Request access to the user's webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam: ', error);
    });

// Handle the capture button click
captureButton.addEventListener('click', () => {
    // Create a canvas to capture the video frame
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to an image and display it in the current captureBox
    const dataURL = canvas.toDataURL('image/png');
    const imgElement = imageElements[captureIndex];
    imgElement.src = dataURL;
    imgElement.style.display = 'block';

    // Remove the placeholder text
    const placeholderText = captureBoxes[captureIndex].querySelector('.placeholder');
    if (placeholderText) {
        placeholderText.style.display = 'none';
    }
    
    // Set the download link and display the download button
    downloadLinks[captureIndex].href = dataURL;
    downloadLinks[captureIndex].download = `captured_image_${captureIndex + 1}.png`;
    downloadLinks[captureIndex].style.display = 'inline-block';

    // Cycle to the next box for the next capture
    captureIndex = (captureIndex + 1) % 4;
});
