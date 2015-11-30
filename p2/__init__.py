import json
from urllib import request
import hashlib
import functools

@functools.total_ordering
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
        self.size = response.headers["Content-Length"]
        md5sum = hashlib.md5()
        total_read = 0
        while True:
            data = response.read(4096)
            total_read += 4096
            if not data:
                break
            md5sum.update(data)

        self.md5 = md5sum.hexdigest()
        self.file_name_no_ext = file_name.split('.')[1]

    def __cmp__(self, other):
        if self.file_name_no_ext > other.file_name_no_ext:
            return 1
        if self.file_name_no_ext < other.file_name_no_ext:
            return -1
        if self.size > other.size:
            return 1
        if self.size < other.size:
            return -1
        if self.index > other.index:
            return 1
        if self.index < other.index:
            return -1
        return 0


file_info_list = []
input_json = "[{\"url\": \"http://www.google.com/\", \"_id\": 9845, \"desc\": \"example domain\"}, {\"url\": \"https://www.github.com/\", \"_id\": 1234, \"desc\": \"doselect\"}]"
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

print(file_info_list[0] == file_info_list[1])
