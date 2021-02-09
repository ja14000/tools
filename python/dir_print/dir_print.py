import os,sys,re
from pathlib import Path

find = "^\/?(?:\w+\/)*(\.\w+)"

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ITALICS = '\033[3m'
   END = '\033[0m'
   WHITE = '\033[97m'
   GREY = '\033[90m'
   BLACK = '\033[90m'

class prefixes:
    # prefix components:
    space =  '    '
    branch = '│   '
    # pointers:
    tee =    '├── '
    last =   '└── '

def tree(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [prefixes.tee] * (len(contents) - 1) + [prefixes.last]
    for pointer, path in zip(pointers, contents):
        if path.is_dir():
            yield prefix + pointer + color.GREEN + color.BOLD + path.name + color.END 
        elif path.is_file():
            if os.path.basename(path).startswith("."):
               yield prefix + pointer + color.GREY + path.name + color.END 
            else:
                yield prefix + pointer + color.WHITE + path.name + color.END
        if path.is_dir(): # extend the prefix and recurse:
            extension = prefixes.branch if pointer == prefixes.tee else prefixes.space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)


#if running direcrly
if __name__ == "__main__": 
    def doTheTree(thePath):
        thePath = (Path(sys.argv[1]))
        try:
            for line in tree(thePath):
                print(line)
        except:
            print("Error printing tree for: " + color.RED+str(thePath.resolve())+color.END)

    if sys.argv[1]:
        print((sys.argv[1]))
        doTheTree((sys.argv[1]))
    else:
        try:
            the_path = Path(input("Enter a path: "))
            doTheTree(the_path)
        except:
            print("Couldn't get path")

#if imported as a module
else:
    try:
        doTheTree(the_path)
    except:
        print("Error printing tree for: " + color.RED+str(the_path.resolve())+color.END)

