from flask import Flask, jsonify
from pwd import getpwuid
import os

app = Flask(__name__)

@app.before_first_request
def set_root_path():
  if os.environ.get('ROOT_PATH') == '':
    os.environ['ROOT_PATH'] = os.getcwd()

@app.get('/', defaults={'relative_path': ''})
@app.get('/<path:relative_path>')
def get(relative_path):
    path = os.path.join(os.environ.get('ROOT_PATH'), relative_path)

    if os.path.isfile(path):
      return jsonify(process_file(path))
    elif os.path.isdir(path):
      return jsonify(process_directory(path))
    else:
      return jsonify({ 'message': 'File not found' }), 404

def process_file(path):
  with open(path) as f:
    file_contents = f.read()

  return file_contents

def process_directory(path):
  directory_contents = os.listdir(path)
  output = []

  for entry in directory_contents:
    metadata = {}
    stats = os.stat(os.path.join(path, entry))

    metadata['name'] = entry
    metadata['owner'] = getpwuid(stats.st_uid).pw_name
    metadata['size'] = stats.st_size
    metadata['permissions'] = oct(stats.st_mode)[-3:]

    output.append(metadata)

  return output

if __name__ == '__main__':
    app.run()
