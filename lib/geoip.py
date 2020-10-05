import geoip2.database
import json

class GeoIP:

    def __init__(self, ipv4_address):
        match = None
        self.ipv4_address = ipv4_address
        self.lat = 0
        self.lng = 0
        self.city = None
        self.region_code = None
        self.region_name = None
        self.country_code = None
        self.country_name = None
        if self.ipv4_address == "127.0.0.1":
            return None
        #reader = geoip2.database.Reader('../mmdb/GeoIP2-City.mmdb')
        # Get City Information
        with geoip2.database.Reader('/var/cache/mmdb/GeoIP2-City.mmdb') as reader:
            try:
                response = reader.city(ipv4_address)
            except:
                return
            if response:
                self.lat = response.location.latitude
                self.lng = response.location.longitude
                self.city = response.city.name
                self.country_code = response.country.iso_code.upper()
                self.country_name = response.country.name
                if len(response.subdivisions) > 0:
                    self.region_code = str(response.subdivisions[0].iso_code)
                    self.region_name = str(response.subdivisions[0].name)
        # Get ISP information
        with geoip2.database.Reader('/var/cache/mmdb/GeoIP2-ISP.mmdb') as reader:
            try:
                response = reader.isp(self.ipv4_address)
            except:
                return
            if response:
                self.asn = response.autonomous_system_number
                self.org = response.autonomous_system_organization
                self.isp = response.isp

    def __str__(self):
        output = "{ "
        object_data = vars(self)
        for attribute_name in object_data:
            output += "\"" + attribute_name + "\": "
            if object_data[attribute_name] is None:
                # is Nonetype
                output += "null" + ", "
            elif isinstance(object_data[attribute_name], str):
                # Is string, so wrap with quotes
                output += "\"" + str(object_data[attribute_name]) + "\", "
            else:
                # assumed to be int or float
                output += str(object_data[attribute_name]) + ", "
        output = output[:-2]
        output += " }"
        #return output
        return json.dumps(vars(self))
