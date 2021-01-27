class LogFile():

    def __init__(self, filename, filter = None):

        self.filename = filename
        self.ReadFile(filter)

    def ReadFile(self, filter = None):

        try:
            fh = open(self.filename,"r")
        except:
            raise Exception("ERROR: could not read log file '" + self.filename + "'")

        self.contents = []
        for line in fh:
            if filter:    
                if filter in line:
                    parts = line.split(" ")
                    self.contents.append(parts)
            else:
                parts = line.split(" ")
                self.contents.append(parts)

        fh.close()
