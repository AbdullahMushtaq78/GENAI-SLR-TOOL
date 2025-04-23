import os
from backend.config.configs import UPLOAD_FOLDER, RESULTS_FOLDER

def get_unique_filename(base_path, filename):
    """Generate unique filename by adding number suffix if file exists"""
    name, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(base_path, filename)

    while os.path.exists(new_path):
        new_filename = f"{name}_{counter}{ext}"
        new_path = os.path.join(base_path, new_filename)
        counter += 1

    return new_path