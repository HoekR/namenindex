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
            url = "http://www.inghist.nl/Onderzoek/Projecten/Egodocumenten/sql/biodes_query"
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

            # id 
            id = person[0]
            if not id:
                self.skip("no id")
                continue
            # name
            name = ""
            for x in (person[3], person[4], person[1]):
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
            name = name.decode('latin1')
            print repr(name)

            # dates
            bplace = person[9] and person[9].decode('latin1') or None
            bdate = person[10] and str(person[10]) or None
            ddate = person[13] and str(person[13]) or None
            text = person[15]
            if text is not None:
                text = text.replace("\x00", "")
                text = text.decode('latin1')

            biourl = "http://www.inghist.nl/Onderzoek/Projecten/Egodocumenten/persoon_detail/%s" % id

            # ----
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = biourl,
                           url_publisher = "http://www.inghist.nl/",
                           birth_place = bplace,
                           birth_date = bdate,
                           death_date = ddate,
                           text = text,
                           )
            self.write_file(bdes, index)

        
if __name__ == '__main__':
    if not os.path.isdir('cache'):
        os.mkdir("cache")

    m = Main()
    m.process()

