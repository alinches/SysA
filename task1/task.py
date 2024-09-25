import csv
from typing import Tuple
import argparse 

def task(file: str, adress: Tuple[int, int]):
  with open(file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    return list(reader)[address[0]][address[0] - 1]


if __name__ == '__main__':
  parser = argparser.ArgumentParse()
  
  parser.add_argument('filepath')
  parser.add_argument('-r', '--row', type=int)
  parser.add_argument('-c', '--column', type=int)
  
  args = parser.parse_args()
  answer = task(args.filepath, (args.row, args.column))
  
  print(answer)
