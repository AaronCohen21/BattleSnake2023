import json

def write(obj, fileName):
  with open(fileName + ".txt", "w") as fp:
    json.dump(obj, fp)


def load(fileName):
  with open(fileName + ".txt", "r") as fp:
    obj = json.load(fp)
  return obj