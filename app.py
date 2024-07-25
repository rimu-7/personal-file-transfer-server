from flask import Flask, request, redirect, url_for
import os
import socket
import random

app = Flask(__name__)

# Define the upload directory (replace with your desired path)
UPLOAD_FOLDER = 'use your desired path, where you want saved your uploaded files'

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) 


def find_available_port(default_port=5000):
  """
  Finds an available port within a random range, retrying a few times.
  """
  for _ in range(5):  # Try 5 times to find an available port
    port = random.randint(4000, 9000)  # Choose a random port between 4000 and 9000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try:
        s.bind(('', port))
        return port  # Success! Return the available port
      except OSError:
        pass  # Port in use, try again
  raise OSError("Failed to find an available port after 5 retries.")

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')  # Get a list of files
        filenames = []
        for uploaded_file in uploaded_files:
            if uploaded_file.filename != '':
                filename = uploaded_file.filename
                uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
                filenames.append(filename)
        message = f'Files {", ".join(filenames)} uploaded successfully!'  # Join filenames
        return redirect(url_for('upload_success', message=message))  # Pass message
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload Files</title>
</head>
<body>
    <h1>Upload Files</h1>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="files" multiple>  <input type="submit" value="Upload">
</form>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#uploadForm').submit(function(e) { // Use form ID for selection
                var progressBar = $('#progress-bar .progress-fill');

                var formData = new FormData(this);

                // Simulate upload progress (replace with actual progress calculation)
                var uploadProgress = 0;
                var uploadInterval = setInterval(function() {
                    uploadProgress += 5;
                    progressBar.css('width', uploadProgress + '%');
                    if (uploadProgress >= 100) {
                        clearInterval(uploadInterval);
                    }
                }, 100);
            });
        });
    </script>
</body>
</html>

    '''

@app.route('/upload_success/<message>')
def upload_success(message):
    return message

if __name__ == '__main__':
  try:
    port = find_available_port()
    app.run(debug=True, host='0.0.0.0', port=port)  # Run on all interfaces, chosen port
  except OSError as e:
    print(f"Error finding available port: {e}")
    exit(1)
