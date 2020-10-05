from __future__ import print_function

class DataTable():
    def __init__(self, name = "", fields = None, linkable_fields = None, data = None, output_type = "text"):
        self.name = name
        if fields is None:
            self.fields = {}
        else:
            self.fields = fields

        if linkable_fields is None:
            self.linkable_fields = dict()
        else:
            self.linkable_fields = linkable_fields

        if data is None:
             self.data = []
        else:
             self.data = data

        self.output_type = output_type
        self.num_rows = len(self.data)

    def AddRow(self, row):
        if type(row) is dict:
            self.data.append(row)
        else:
            self.data.append(row.__dict__)
        self.num_rows += 1

    def __str__(self):
        if self.output_type == "json":
            return self.PrintAsJSON()
        if self.output_type == "html":
            return self.PrintAsHTML()
        return self.PrintAsText()

    def PrintAsText(self):
        output = ""
        for field_name in self.fields:
            output += field_name + "\t"
        output += "\n"
        for row in self.data:
            for field_name in self.fields:
                output += row[field_name] + "\t"
            output += "\n"
        return output

    def PrintAsJSON(self):

        output = "[\n"
        for row in self.data:
            output += "  {"
            for field_name in self.fields:
                if "\\" in row[field_name]:
                    data = row[field_name].replace("\\", "\\\\")
                else:
                    data = row[field_name]
                output += "\"" + field_name + "\": \"" + data + "\", "
            output = output[:-2]
            output += " },\n"
        output = output[:-2] + "\n]\n"
        #output += "\n]\n"
        return output

    def PrintAsHTML(self):

        output = "<TABLE BORDER=1 CELLPADING=2 WIDTH=90%>"
        for field_name in self.fields:
            output += "<TH>" + field_name + "</TH>"
        output += "\n"

        for row in self.data:
            output += "<TR>"
            for field_name in self.fields:
                output += "<TD>"
                if field_name in self.linkable_fields:
                    output += "<A HREF='lkajsdflkjasdf?get_details="+ field_name +"'>"
                if row[field_name] is None:
                    output += "&nbsp;"
                else:
                    output += row[field_name]
                output += "</TD>"
            output += "</TR>\n"
        output += "</TABLE>"
        return output
