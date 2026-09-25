import hashlib
import os

def get_data_version(data_dir: str = "data") -> str:
    """
    Computes a content hash of the JSON files in the data directory 
    to serve as the current data version.
    """
    if not os.path.exists(data_dir):
        return "unknown"
        
    hasher = hashlib.md5()
    files = sorted([f for f in os.listdir(data_dir) if f.endswith(".json")])
    for f in files:
        file_path = os.path.join(data_dir, f)
        with open(file_path, "rb") as fh:
            hasher.update(fh.read())
            
    return hasher.hexdigest()[:8]
