import os

path = ""
text = ""

for filename in os.listdir(path):
    if filename.endswith(".txt"):
        with open(path + filename, "r") as f:
            text = f.read()

        text = text.replace("Traffic light", "0")

        with open(path + filename, "w") as f:
            f.write(text)