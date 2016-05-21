from io import open
from pprint import pprint
import collections
import cmd


routes_file = open('routes-tocheck.txt')
output_file = open('output.txt')
routes = routes_file.read()
output = output_file.read()
x = ''

routes_lines = routes.split("\n")
for line in routes_lines:
    result = output.find(line)
    if result == -1:
        print("missing route " +line)



