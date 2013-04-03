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

class Settings():
    headingStyle = None
    labelPrefix = None
    shouldAddLabel = None
    outfile = None
    diffPrefixRegex = None
