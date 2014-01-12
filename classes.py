class DiffLineState:
    INSERT = 0
    DELETE = 1
    UNCHANGED = 2

class DiffLine():
    def __init__(self):
        self.text = None
        self.state = DiffLineState.UNCHANGED

class DiffChange():
    def __init__(self):
        self.oldStartLine = None
        self.newStartLine = None
        self.description = None
        self.lines = []

class DiffFile():
    def __init__(self):
        self.oldPath = None
        self.newPath = None
        self.pathChanged = False
        self.changes = []
        self.diffLine = None

class Settings():
    headingStyle = None
    labelPrefix = None
    shouldAddLabel = None
    outfile = None
    diffPrefixRegex = None
    quiet = None

settings = Settings()

class ParseError(Exception):
    def __init__(self, lineNum, e):
        self.lineNum = lineNum
        self.e = e
    def __str__(self):
        return ("An error occurred while parsing your diff file at line %d" % self.lineNum)

class ToTexError(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return ("An error occurred while converting your diff to TeX")
