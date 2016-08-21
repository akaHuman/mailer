import json
from urllib import request
import hashlib

class FileInfo:
    url = ""
    file_name = ""
    size = -1
    index = -1
    md5 = ""
    file_name_no_ext = ""

    def __init__(self, url, file_name, index):
        self.url = url
        self.file_name = file_name
        self.index = index
        response = request.urlopen(self.url)
        md5sum = hashlib.md5()
        total_read = 0
        while True:
            data = response.read(4096)
            total_read += 4096
            if not data:
                break
            md5sum.update(data)
        self.size = total_read
        self.md5 = md5sum.hexdigest()
        self.file_name_no_ext = file_name.split('.')[1]

    def __lt__(self, other):
        if self.file_name_no_ext < other.file_name_no_ext:
            return True
        if self.size < other.size:
            return True
        if self.index < other.index:
            return True
        return False

    def __gt__(self, other):
        if self.file_name_no_ext > other.file_name_no_ext:
            return True
        if self.size > other.size:
            return True
        if self.index > other.index:
            return True
        return False

    def __eq__(self, other):
        if self.index == other.index:
            return True


file_info_list = []
input_json = input()
parsed_json = json.loads(input_json)
i = 0

for element in parsed_json:
    url = element["url"]
    split_result = request.urlsplit(url)
    file_name = split_result[2]
    if file_name == "/":
        file_name = "index.html"
    file_info_list.append(FileInfo(url, file_name, i))
    i += 1

file_info_list.sort()
password = ""
for file_info in file_info_list:
    password += file_info.md5

print(password)
