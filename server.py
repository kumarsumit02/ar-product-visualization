from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import subprocess
import os
import csv
import base64
import time

app = Flask(__name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/run_web_cam', methods=['GET'])
def run_web_cam():
    # Execute your Python script here
    try:
        # Start the script execution in a subprocess
        process = subprocess.Popen(["python", "detect.py", "--weights", "runs/train/exp19/weights/last.pt", "--source", "0", "--save-csv"])

        # Allow the script to run for 10 seconds
        time.sleep(20)
        # Check if the process is still running, and terminate it if necessary
        if process.poll() is None:
            process.terminate()

        objects_identified = process_csv()

        return jsonify({   
            "success": True,
            "objects_detected": sorted(objects_identified)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        # Get the file path from the request's JSON payload
        request_data = request.json
        file_name = request_data.get('file_name')

        if not file_name:
            return jsonify({"error": "Missing 'file_name' in the request payload"}), 400

        # Expand the ~ character to the user's home directory
        user_home = os.path.expanduser("~")
        file_path = os.path.join(user_home, 'Desktop', file_name)

        # Execute your Python script with the provided file path
        subprocess.run(["python", "detect.py", "--weights", "yolov5s.pt", "--source", file_path, "--view-img", "--save-csv"])

        objects_identified = process_csv()


        return jsonify({   
            "success": True,
            "objects_detected": sorted(objects_identified)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload_video_im', methods=['POST'])
def upload_video2():
    try:
        # Get the file path from the request's JSON payload
        request_data = request.json
        file_name = request_data.get('file_name')

        if not file_name:
            return jsonify({"error": "Missing 'file_name' in the request payload"}), 400

        # Expand the ~ character to the user's home directory
        user_home = os.path.expanduser("~")
        file_path = os.path.join(user_home, 'Desktop', file_name)

        # Execute your Python script with the provided file path
        subprocess.run(["python", "detect.py", "--weights", "runs/train/exp22/weights/last.pt", "--source", file_path, "--view-img", "--save-csv"])

        objects_identified = process_csv()

        return jsonify({   
            "success": True,
            "objects_detected": objects_identified
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:

        UPLOAD_FOLDER = 'demo_images'

        # Check if the 'file' field is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            # Secure the filename to prevent any directory traversal or malicious file names
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Save the uploaded file
            file.save(file_path)

            # Run the YOLOv5 detection subprocess
            subprocess.run(["python", "detect.py", "--weights", "yolov5x.pt", "--source", file_path, "--save-csv"])
            # subprocess.run(["python", "detect.py", "--weights", "runs/train/exp22/weights/last.pt", "--source", file_path, "--save-csv"])

            objects_identified = process_csv()

            return jsonify({
                "success": True,
                "objects_detected": sorted(objects_identified)
            })
        
        return jsonify({"error": "Invalid file format. Allowed formats: png, jpg, jpeg, gif"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_csv():

    im_products = ["chair", "sink", "bottle", "SKU33333", "SKU12345", "SKU54321"]

    # Initialize an empty set to store unique objects
    unique_objects = set()

    # Replace 'your_csv_file.csv' with the actual path to your CSV file
    csv_file_path = 'demo_run/predictions.csv'

    # Open the CSV file and read its content
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Iterate through the rows in the CSV file
        for row in csv_reader:
            # Assuming the object name is in the 2nd column (index 1)
            object_name = row[1]
            # Add the object name to the set
            if object_name in im_products:

                if object_name == "SKU33333":
                    unique_objects.add(object_name + " - sink")
                elif object_name == "SKU12345":
                    unique_objects.add(object_name + " - sports ball")
                elif object_name == "SKU54321":
                    unique_objects.add(object_name + " - bottle")
                else:
                    unique_objects.add(object_name)

    # Print the unique object names
    for obj in unique_objects:
        print(obj)
    
    return list(unique_objects)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
