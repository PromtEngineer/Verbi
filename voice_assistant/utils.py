# voice_assistant/utils.py

import os
import logging

def delete_file(file_path):
    """
    Delete a file from the filesystem.
    
    Args:
    file_path (str): The path to the file to delete.
    """
    try:
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
    except PermissionError:
        logging.error(f"Permission denied when trying to delete file: {file_path}")
    except OSError as e:
        logging.error(f"Error deleting file {file_path}: {e}")
