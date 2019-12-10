"""
http://projects.gerbrandy.com/pm/p/namenindex/ticket/21
"""

import os
import urllib

import biodes
from sutils import Base, sanitize_name

INPUT = "cache/in.txt"


class Main(Base):

    def _get_input_data(self):
        if not os.path.exists(INPUT):
            url = "http://www.inghist.nl/Onderzoek/Projecten/WVO/Lijsten/biodes_query"
            f = urllib.urlopen(url)
            data = f.read()
            f.close()
            f = open(INPUT, 'w')
            f.write(data)
            f.close()
        else:
            f = open(INPUT, 'r')
            data = f.read()
            f.close()
        return data

    def process(self):
        data = eval(self._get_input_data())
        self.total = len(data)
        for index, person in enumerate(data):
            index += 1
            name = ""
            for x in (person[1], person[2], person[0]):
                if x is not None:
                    name += x 
                    name += " "
            name = name.strip()
            if not name:
                self.skip("empty name")
                continue
            else:
                name = sanitize_name(name)
            if self.name_already_processed(name):
                self.skip("duplicate name")
                continue

            encoded_name = urllib.quote(name)
            biourl = "http://www.inghist.nl/Onderzoek/Projecten/WVO/brieven?af_naam_vol=" + encoded_name
            # ----
            name = name.decode('latin1')
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = biourl,
                           url_publisher = "http://www.inghist.nl/",
                           )
            self.write_file(bdes, index)

        
if __name__ == '__main__':
    if not os.path.isdir('cache'):
        os.mkdir("cache")

    m = Main()
    m.process()

