import json
import pickle
import pathlib
import os

class FileHandler():
    def __init__(self):
        self.data_folder_path = pathlib.Path().resolve()  / "data"
        self.data_files = [
            "posts.json",
            "likers.json",
            "credentials.json"
        ]
        self.check_data_folder()      

    def check_data_folder(self):
        pathlib.Path(self.data_folder_path).mkdir(exist_ok=True)
        for data_file in self.data_files:
            file_path = self.data_folder_path / data_file
            if not pathlib.Path(file_path).is_file():
                with file_path.open('w') as f: 
                    f.write('') 

    def enter_credentials(self, user, passwd):
        self.dump('credentials', {'username': user, 'password': passwd})

    def get_credentials(self):
        return self.load('credentials')

    
    def dump(self, filename, data):
        with open(self.data_folder_path / (filename+'.json'), 'w') as f:
            json.dump(data, f, indent=2)


    def load(self, filename):
        j = self.data_folder_path / (filename+'.json')
        if os.stat(j).st_size == 0:
            return dict()
        with open(j, 'r') as f:
            data = json.load(f)
        return data