class LogFile():

        def __init__(self, filename, filter):
                self.filename = filename
                self.ReadFile(filter)

        # Open file read-only 
        def ReadFile(self, filter):
                try:
                        fh = open(self.filename,"r")
                except:
                        sys.exit("ERROR: could not read log file '" + self.filename + "'")
                # Read line by line and split by space in to array
                self.contents = []
                for line in fh:
                        if filter in line:
                                parts = line.split(" ")
                                self.contents.append(parts)
                fh.close()


