import os
import urllib

from lxml import etree

import biodes
from sutils import Base, sanitize_name

INPUT = "in.data"


class Main(Base):

    def process(self):
        with open (INPUT, 'r') as f:
            data = f.read()
        data = data.replace("\n", "")
        people = eval(data)
        self.total = len(people)
        index = 0
        for (url, name) in people:
            index += 1
            if self.name_already_processed(name):
                self.skip("dupe name")
                continue
            #
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = url,
                           url_publisher = "http://www.inghist.nl/",
                           )
            self.write_file(bdes, index)


if __name__ == '__main__':
    m = Main()
    m.process()

