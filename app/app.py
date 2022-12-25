import os
from flask import Flask, request, render_template, Response, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from google.cloud import storage

execution_path = os.getcwd()
storage_client = storage.Client()
bucket_name = "result_ojt_after_api"
bucket = storage_client.get_bucket(bucket_name)
blobs = list(bucket.list_blobs())

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/", methods= ['GET','POST'])
@cross_origin()
def homepage(): # Redirecting to home page
    return render_template("index.html")

@app.route("/get_json", methods= ['GET','POST']) # Receives loaded file name and requests JSON file
def get_json():
    data = request.get_data('user_input')
    data = str(data, 'utf-8')
    for blob in blobs:
        print(blob.name)
        print(f"data: {data}")
        blob.download_to_filename(f"{data}")
        print("File downloaded")
        json_file = send_from_directory(execution_path, f"{data}")
        print("FIle sent")
        # return videoplayback.json
        return json_file

@app.route("/<path:path>")
@cross_origin()
def static_dir(path):
    print(request)
    file_name = request.get_data('json_input')
    return send_from_directory(".", path)

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))


