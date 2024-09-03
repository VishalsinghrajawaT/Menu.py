import cv2
import random
import sys
import time
import subprocess
import requests
from flask import Flask, request,jsonify,render_template,Response,send_from_directory
from flask_cors import CORS
import logging
import bs4
import smtplib
from bs4 import BeautifulSoup
from twilio.rest import Client
import pywhatkit
import pyautogui
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)




# ----------------------------WHATSAPP MESSAGE--------------------------------------------
@app.route("/WhatsapppMsg", methods=["POST"])
def send_whatsapp_message():
    if request.method == "POST":
        phone_number = request.form.get("PhoneNo")
        message = request.form.get("message")

        if not phone_number or not message:
            return "Phone number and message are required.", 400

        try:
            # Send the message to WhatsApp Web instantly without needing to press Enter
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            return 'Sent WhatsApp message', 200
        except Exception as e:
            return f"Message not sent: {e}", 500
        

#--------------------------TEXT MESSAGE------------------------------
@app.route("/TextMsg", methods=["POST"])
def send_text_message():
    try:
        # Retrieve the credentials securely
        account_sid = 'AC837fac639039b66ff1b55776d8e0ed75'
        auth_token = 'd3acfcd6e730b7482eb5509445911934'

        # Get the phone number and message from the request JSON
        data = request.get_json()
        phone_number = data.get("phone")
        message_body = data.get("message")

        # Initialize the Twilio client
        client = Client(account_sid, auth_token)

        # Send the message
        message = client.messages.create(
            body=message_body,
            from_='+13345649657',
            to=phone_number
        )
        return jsonify({'status': 'success', 'message_sid': message.sid})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

# -----------------------------PHONE Call-------------------------
@app.route("/Phonecall", methods=["POST"])
def phone_call():
    # Retrieve the credentials securely
    account_sid = 'AC837fac639039b66ff1b55776d8e0ed75'
    auth_token = 'd3acfcd6e730b7482eb5509445911934'   
    # Initialize the Twilio client
    client = Client(account_sid, auth_token)    
    # Get the phone number from the request
    number = request.form.get("phone")   
    try:
        # Make the phone call
        call = client.calls.create(
            to=number,
            from_='+13345649657',
            url='http://demo.twilio.com/docs/voice.xml'
        )
        
        # Return a JSON response
        return jsonify({'status': 'success', 'call_sid': call.sid})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# ----------------------------Email Send------------------------
@app.route("/Email", methods=["POST"])
def send_email():
    # Retrieve the email ID and password from environment variables for security
    email_id = request.form.get('email_id')
    password = 'pwnbdalrtgzrvnoy'  # Replace with your actual password securely

    # Get recipient email and content from the form
    to = request.form.get('Recipient_Email')
    content = request.form.get('content')

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_id, password)

        # Send the email
        server.sendmail(email_id, to, content)
        server.close()

        # Return a success response
        return jsonify({'status': 'success', 'message': 'Email sent successfully'})

    except Exception as e:
        # Return an error response
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# _________________instagram______________________________________
# logging.basicConfig(level=logging.DEBUG)

# @app.route('/upload-to-instagram', methods=['POST'])
# def upload_to_instagram():
#     try:
#         # Check if the required fields are present
#         if 'image' not in request.files or 'caption' not in request.form or 'username' not in request.form or 'password' not in request.form or 'phone' not in request.form:
#             return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

#         image_file = request.files['image']
#         caption = request.form['caption']
#         username = request.form['username']
#         password = request.form['password']
#         phone = request.form['phone']

#         # Validate the file
#         if image_file.filename == '':
#             return jsonify({'status': 'error', 'message': 'No selected file'}), 400

#         # Save the image temporarily
#         image_path = os.path.join('uploads', image_file.filename)
#         image_file.save(image_path)

#         # Instagram API configuration (update with your credentials and details)
#         access_token = 'YOUR_INSTAGRAM_ACCESS_TOKEN'
#         instagram_graph_url = 'https://graph.facebook.com/v12.0/{your-instagram-business-account-id}/media'
#         media_params = {
#             'image_url': image_path,
#             'caption': caption,
#             'access_token': access_token
#         }

#         response = requests.post(instagram_graph_url, data=media_params)
#         response.raise_for_status()  # Raise an exception for HTTP errors

#         response_data = response.json()

#         if 'error' in response_data:
#             app.logger.error(f"Instagram API error: {response_data['error']['message']}")
#             return jsonify({'status': 'error', 'message': response_data['error']['message']}), 500

#         media_id = response_data.get('id')
#         publish_url = f'https://graph.facebook.com/v12.0/{your-instagram-business-account-id}/media_publish'
#         publish_params = {'creation_id': media_id, 'access_token': access_token}

#         publish_response = requests.post(publish_url, data=publish_params)
#         publish_response.raise_for_status()

#         publish_data = publish_response.json()
#         return jsonify({'status': 'success', 'message': 'Image uploaded successfully!', 'data': publish_data})
    
#     except requests.RequestException as e:
#         app.logger.error(f"Request exception: {str(e)}")
#         return jsonify({'status': 'error', 'message': 'Request failed'}), 500
#     except Exception as e:
#         app.logger.error(f"Unexpected error: {str(e)}")
#         return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500


# ************************************Google Search************************************************
@app.route('/search', methods=['GET'])
def search_five_results():
    search_term = request.args.get('text')
    url = f'https://www.google.com/search?q={search_term}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    
    request_result = requests.get(url, headers=headers)
    soup = BeautifulSoup(request_result.text, "html.parser")

    results = []
    for i, info in enumerate(soup.find_all('h3'), 1):
        results.append(info.getText())
        if i == 5:
            break

    return jsonify(results)



# _______________________RainbowConvert________________
@app.route("/RainbowConvert", methods=['POST'])
def rainbow_convert():
    text = request.form['user_input']
    
    colors = [
        'red',
        'orange',
        'yellow',
        'green',
        'blue',
        'indigo',
        'violet'
    ]
    
    def generate():
        color_index = 0
        for char in text:
            if char.isspace():
                yield char
            else:
                color = colors[color_index]
                yield f'<span style="color: {color};">{char}</span>'
                color_index = (color_index + 1) % len(colors)
            time.sleep(0.05)  # Adjust delay as needed

    return Response(generate(), content_type='text/html')
# ____________________________Camera_______________________________
@app.route("/OpenCamera")
def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        status, photo = cap.read()
        cv2.imshow("", photo)
        if cv2.waitKey(100) == 13: 
            break
    cv2.destroyAllWindows()
    cap.release()




# ******************************Filter ***********************************

app = Flask(__name__)

# Directories for uploads and filtered images
UPLOAD_FOLDER = 'uploads'
FILTERED_FOLDER = 'filtered'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FILTERED_FOLDER, exist_ok=True)

# HTML template for the single-page application
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Filter Application</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #1e1e1e; color: #fff; display: flex; flex-direction: column; min-height: 100vh; padding: 20px; }
        main { max-width: 800px; margin: auto; background-color: #2a2a2a; padding: 20px; border-radius: 10px; }
        header { text-align: center; margin-bottom: 20px; }
        header h1 { font-size: 2.5rem; color: #a782f9; }
        form { background-color: #34495e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); text-align: center; margin-bottom: 20px; }
        input[type="file"] { margin-bottom: 10px; }
        button { padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .image-box { margin: 10px 0; padding: 10px; background-color: #34495e; border-radius: 10px; position: relative; }
        .image-box img { max-width: 100%; border-radius: 10px; }
        .image-box .download-button { display: block; width: 100%; padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; text-align: center; margin-top: 10px; text-decoration: none; }
        .image-box .download-button:hover { background-color: #218838; }
        .image-box .image-label { position: absolute; top: 10px; left: 10px; background-color: rgba(0, 0, 0, 0.7); color: #fff; padding: 5px; border-radius: 5px; }
    </style>
</head>
<body>
    <header>
        <h1>Image Filter Application</h1>
    </header>
    <main>
        <form id="upload-form" action="/uploadfilter" method="post" enctype="multipart/form-data">
            <input type="file" id="upload-photo" name="file" accept="image/*" required>
            <button type="submit">Apply Filters</button>
        </form>
        <div id="filtered-images"></div>
    </main>
    <script>
        document.getElementById('upload-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('/uploadfilter', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('filtered-images');
                    container.innerHTML = '';
                    data.images.forEach(image => {
                        const box = document.createElement('div');
                        box.className = 'image-box';
                        const img = document.createElement('img');
                        img.src = image.url;
                        img.alt = 'Filtered Image';
                        const label = document.createElement('div');
                        label.className = 'image-label';
                        label.textContent = image.label;
                        const downloadButton = document.createElement('a');
                        downloadButton.href = image.url;
                        downloadButton.download = image.filename;
                        downloadButton.className = 'download-button';
                        downloadButton.textContent = 'Download';
                        box.appendChild(label);
                        box.appendChild(img);
                        box.appendChild(downloadButton);
                        container.appendChild(box);
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    </script>
</body>
</html>
'''

def apply_color_filter(image_path, filter_color, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}.")
        return
    filtered_image = image.copy()
    if filter_color.lower() == 'red':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    elif filter_color.lower() == 'green':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filter_color.lower() == 'blue':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 1] = 0
    else:
        print(f"Invalid color filter: {filter_color}.")
        return
    success = cv2.imwrite(output_path, filtered_image)
    if not success:
        print(f"Error: Could not save image to {output_path}.")

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/uploadfilter', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        filters = ['red', 'green', 'blue']
        filtered_images = []

        for filter_color in filters:
            output_path = os.path.join(FILTERED_FOLDER, f'{filter_color}_{filename}')
            apply_color_filter(file_path, filter_color, output_path)
            filtered_images.append({
                'url': f'/filtered/{filter_color}_{filename}',
                'filename': f'{filter_color}_{filename}',
                'label': filter_color.capitalize()
            })

        return jsonify({'images': filtered_images})

@app.route('/filtered/<filename>')
def get_filtered_image(filename):
    return send_from_directory(FILTERED_FOLDER, filename)






# __________________________Dokcer Opertion___________________
@app.route("/docker_image_pull", methods=["POST"])
def docker_img_pull():
    image = request.form.get('image')
    cmd = f"docker pull {image}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": "Image downloaded successfully.", "status": "success"})
    else:
        return jsonify({"message": "Image download failed.", "status": "fail"})


@app.route("/launch_docker", methods=["POST"])
def docker_launch():
    container_name = request.form.get('container_name')
    image = request.form.get('image')
    cmd = f"docker run -dit --name {container_name} {image}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": "Docker container launched successfully.", "status": "success", "container_id": output[1]})
    else:
        return jsonify({"message": "Failed to launch Docker container.", "status": "fail"})


@app.route("/docker_stop", methods=["POST"])
def docker_stop():
     container_name = request.form.get('container_name')
     cmd = f"docker stop {container_name}"
     output = subprocess.getstatusoutput(cmd)
     if output[0] == 0:
        return jsonify({"message": "Docker container stopped successfully.", "status": "success"})
     else:
        return jsonify({"message": "Failed to stop Docker container.", "status": "fail"})

@app.route("/docker_start", methods=["POST"])
def docker_start():
    container_name = request.form.get('container_name')
    cmd = f"docker start {container_name}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": "Docker container started successfully.", "status": "success"})
    else:
        return jsonify({"message": "Failed to start Docker container.", "status": "fail"})

@app.route("/docker_status", methods=["POST"])
def docker_status():
    container_name = request.form.get('container_name')
    cmd = f"docker ps -a --filter name={container_name} --format '{{{{.ID}}}} {{{{.Names}}}} {{{{.Status}}}}'"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": output[1], "status": "success"})
    else:
        return jsonify({"message": "Failed to get Docker container status.", "status": "fail"})

@app.route("/docker_remove", methods=["POST"])
def docker_remove():
    container_name = request.form.get('container_name')
    cmd = f"docker rm {container_name}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": "Docker container removed successfully.", "status": "success"})
    else:
        return jsonify({"message": "Failed to remove Docker container.", "status": "fail"})

@app.route("/docker_logs", methods=["POST"])
def docker_logs():
    container_name = request.form.get('container_name')
    cmd = f"docker logs {container_name}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": output[1], "status": "success"})
    else:
        return jsonify({"message": "Failed to get Docker container logs.", "status": "fail"})

@app.route("/docker_image_remove", methods=["POST"])
def docker_img_remove():
    image = request.form.get('image')
    cmd = f"docker rmi -f {image}"
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 0:
        return jsonify({"message": "Docker image removed successfully.", "status": "success"})
    else:
            return jsonify({"message": "Failed to remove Docker image.", "status": "fail"})

app.run()