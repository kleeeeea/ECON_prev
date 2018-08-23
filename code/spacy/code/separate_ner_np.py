import sys
import json
from tqdm import tqdm
import ipdb

def get_line_count(inFile):
  count = -1
  for count, line in enumerate(open(inFile, 'r')):
     pass
  count += 1
  return count


def writeToJson(inFile, npOutFile, entityOutFile):
  with open(inFile, 'r') as fin, open(npOutFile, 'w') as npout, open(entityOutFile, 'w') as entityout:
    total = get_line_count(inFile)

    for line in tqdm(fin, total=total):
      data = json.loads(line.strip())
      nps = data['np']
      entities = data['entity']

      npout.write(json.dumps(nps))
      npout.write('\n')
      entityout.write(json.dumps(nps))
      entityout.write('\n')

if __name__ == '__main__':

    try:
      inFile = sys.argv[1]
      npOutFile = sys.argv[2]
      entityOutFile = sys.argv[3]
      writeToJson(inFile, npOutFile, entityOutFile)
    except Exception as e:
      print(e)
      ipdb.set_trace();
