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
            url = "http://www.inghist.nl/Onderzoek/Projecten/KPP/data/biodes_query"
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
#            self.print_progress(index)
            id = person[0]
            name = ""
            for x in (person[4], person[2], person[3], person[1]):
                if x is not None:
                    name += x 
                    name += " "
            name = name.decode('latin1')
            name = sanitize_name(name)
            if self.name_already_processed(name):
                self.skip("duplicate name")
                continue
            biourl = "http://www.inghist.nl/Onderzoek/Projecten/KPP/PersoonDetail?Id=%s" % id
            sex = person[5]
            if sex == 'm':
                sex = 1
            elif sex == 'v':
                sex = 2
            else:
                sex = None
            text = (person[16], person[17], person[18])
            text = ' '.join([x for x in text if x])
            text = text.strip()
            text = text.decode('latin1')

            if not text:
                text = person[14]
                if text:
                    text = text.decode('latin1')

            # ----
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = biourl,
                           url_publisher = "http://www.inghist.nl/",
                           sex = sex,
                           text = text,
                           )
            self.write_file(bdes, index)

        
if __name__ == '__main__':
    if not os.path.isdir('cache'):
        os.mkdir("cache")

    m = Main()
    m.process()

