import os

def listFiles(dir):
    
    files = []
    contents = os.listdir(dir)

    for _ in contents:
        files.append(_)
    
    return files
