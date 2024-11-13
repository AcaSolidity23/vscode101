import sys
for k in sys.path:
    print(k)

def add_to_path(folder_path):
    sys.path.append(folder_path)

fp = 'C:/Users/alazarevic/AppData/Local/Programs/Python/Python312/Scripts'
add_to_path(fp)
