from collections import defaultdict
import csv

def task(csv_str: str):
  outgoing = defaultdict(list)
  incoming = defaultdict(list)
  
  reader = csv.reader(csv_str.splitlines(), delimiter=',')
  for line in reader:
    if line:
      source, target = line
      outgoing[source].append(target)
      incoming[target].append(source)
      
      if source not in incoming:
        incoming[source] = []
      if target not in outgoing:
        outgoing[target] = []

    
    root = next(node for node in incoming if not incoming[node])
    leaves = [node for node in outgoing if not outgoing[node]]

    
    relationships = {
        node: {
            'r1': set(outgoing[node]),  
            'r2': set(incoming[node]),  
            'r3': set(),                
            'r4': set(),                
            'r5': set()                 
        }
        for node in incoming
    }

    
    stack = [root]
    while stack:
        current = stack.pop()
        for target in outgoing[current]:  
            relationships[target]['r4'].update(relationships[current]['r2'])
            relationships[target]['r4'].update(relationships[current]['r4'])
            relationships[target]['r5'].update(relationships[current]['r1'] - {target})
            stack.append(target)

    
    stack = leaves[:]
    while stack:
        current = stack.pop()
        for source in incoming[current]:  
            relationships[source]['r3'].update(relationships[current]['r1'])
            relationships[source]['r3'].update(relationships[current]['r3'])
            if source not in stack:
                stack.append(source)

    
    fields = ('r1', 'r2', 'r3', 'r4', 'r5')
    csv_output = '\n'.join(
        ','.join(str(len(relationships[node][field])) for field in fields)
        for node in sorted(relationships)
    ) + '\n'

    return csv_output

if __name__ == '__main__':
    input_data = "1,2\n1,3\n3,4\n3,5\n"
    print(task(input_data))
