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
        people = eval(data)
        self.total = len(people)
        index = 0
        for (id, firstn, lastn, place) in people:
            index += 1
            name = "%s %s" % (firstn, lastn)
            if self.name_already_processed(name + str(place)):
                self.skip("dupe name")
                continue
            snippet = ("kapitein komende uit %s" % place.capitalize() if place else None)
            url = "http://www.inghist.nl/Onderzoek/Projecten/Elbing/captain/journeys?id=%s" %id
            #
            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = url,
                           url_publisher = "http://www.inghist.nl/",
                           text = snippet,
                           )
            self.write_file(bdes, index)

        
if __name__ == '__main__':
    m = Main()
    m.process()

