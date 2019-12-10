"""
http://projects.gerbrandy.com/pm/p/namenindex/ticket/21
"""

import os
import urllib

import biodes
from sutils import Base, sanitize_name
from gerbrandyutils import normalize_url

INPUT = "cache/in.txt"


class Main(Base):

    def _get_input_data(self):
        if not os.path.exists(INPUT):
            url = "http://www.inghist.nl/Onderzoek/Projecten/RapportenCentraleInlichtingendienst1919-1940/data/Lijsten/biodes_query"
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
        DateTime = lambda x: None
        data = eval(self._get_input_data())
        self.total = len(data)
        for index, person in enumerate(data):
            index += 1
            self.print_progress(index)
            id = person[0]
            name = person[1]
            if not id:
                self.skip("id is None")
                continue
            if name is None:
                self.skip("name is None")
                continue
            name = name.decode('latin1')
            name = sanitize_name(name)
            if self.name_already_processed(name):
                self.skip("duplicate name: %s" %name)
                continue
            
            encoded_name = urllib.quote(name.encode('utf8'))
            biourl = "http://www.inghist.nl/Onderzoek/Projecten/RapportenCentraleInlichtingendienst1919-1940/data/GeavanceerdResult.html?batch_size=15&persoon=" + encoded_name
                       
            text = person[7]
            if text is not None:
                text = text.strip()
                text = text.decode('latin1')

            if "Berger, L.M., zie Morisset" in name:
                self.skip("name causing unknwon encoding error: %s" %name)
                continue

            # ----
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = biourl,
                           url_publisher = "http://www.inghist.nl/",
                           text = text,
                           )

            self.write_file(bdes, index)

        
if __name__ == '__main__':
    if not os.path.isdir('cache'):
        os.mkdir("cache")

    m = Main()
    m.process()

