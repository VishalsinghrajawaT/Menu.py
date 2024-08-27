function sendRequest(endpoint, formData) {
    var xhr = new XMLHttpRequest();
    var url = `http://your_public_ip_with_portnumber/${endpoint}`;
    xhr.open("POST", url, true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            alert(response.message);
        } else {
            alert("Request failed.");
        }
    };
    xhr.send(formData);
}
function dockerImgPull() {
    var formData = new FormData(document.getElementById("dockerImgPullForm"));
    sendRequest("docker_image_pull", formData);
}

function dockerLaunch() {
    var formData = new FormData(document.getElementById("dockerLaunchForm"));
    sendRequest("launch_docker", formData);
}

function dockerStop() {
    var formData = new FormData(document.getElementById("dockerStopForm"));
    sendRequest("docker_stop", formData);
}

function dockerStart() {
    var formData = new FormData(document.getElementById("dockerStartForm"));
    sendRequest("docker_start", formData);
}

function dockerStatus() {
    var formData = new FormData(document.getElementById("dockerStatusForm"));
    sendRequest("docker_status", formData);
}

function dockerRemove() {
    var formData = new FormData(document.getElementById("dockerRemoveForm"));
    sendRequest("docker_remove", formData);
}

function dockerLogs() {
    var formData = new FormData(document.getElementById("dockerLogsForm"));
    sendRequest("docker_logs", formData);
}

function dockerImgRemove() {
    var formData = new FormData(document.getElementById("dockerImgRemoveForm"));
    sendRequest("docker_image_remove", formData);
}

