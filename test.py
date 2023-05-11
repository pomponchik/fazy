from importlib.machinery import PathFinder

print(PathFinder.find_spec('test.py'))
print(dir(PathFinder.find_spec('test.py')))
