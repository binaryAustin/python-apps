import glob

myfiles = glob.glob("files/*.txt")

for filepath in myfiles:
    with open(filepath, "r", encoding="utf8") as fr:
        print(fr.read())
