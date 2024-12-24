
def get_file_content(path):
    with open(path) as f:
        content = f.read()
    return content
