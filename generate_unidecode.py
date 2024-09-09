# download avian2/unidecode python module and convert table to golang.
import requests
from io import BytesIO
from zipfile import ZipFile
import json

# in case i need to modify it without downloading the same file again and again
# file = open("master.zip", "rb")

r = requests.get("https://github.com/avian2/unidecode/archive/refs/heads/master.zip")
assert(r.status_code == 200)
file = BytesIO(r.content)

zipfile = ZipFile(file)

output = "package gotextsanitizer\n\nvar defaultUnidecodeMap = map[uint16][]string{\n"
for f in zipfile.namelist():
    if not f.startswith("unidecode-master/unidecode/x"):
        continue
    
    content = zipfile.open(f).read().decode()
    data = eval(content.split("data = ")[1])
    assert(len(data) in (255,256)) # some file have 256 entries and some other 255 (idk why and i won't find why)

    block_num = "0"+f.split("/")[2][:-3]
    assert(len(block_num) == 5)

    output += "\t"+block_num+": {"

    is_first_pass = True
    for val in data:
        if not is_first_pass:
            output += ","
        is_first_pass = False
        if val is None:
            output += '""'
        else:
            output += json.dumps(val) # i hope it matches the golang escaping format

    output += "},\n"

output += "}"

with open("defaultUnidecodeMap.go", "w") as fp:
    fp.write(output)