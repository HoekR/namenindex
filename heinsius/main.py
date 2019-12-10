from __future__ import with_statement

"""
http://projects.gerbrandy.com/pm/p/namenindex/ticket/21
"""

import os
import urllib

from lxml import etree

import biodes
from sutils import Base, sanitize_name

INPUT = "in.xml"


class Main(Base):

    def process(self):
        tree = etree.parse(INPUT)
        entries = tree.xpath("//item")
        self.total = len(entries)
        for index, person in enumerate(entries):
            index += 1
            self.print_progress(index)
            text = person.xpath("name")[0].text
            name = text[:text.find('.')]
            snippet = text[text.find('.') + 1:]
            snippet = snippet.strip()
           
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8'))) 
            biourl = "http://www.inghist.nl/retroboeken/heinsius/#accessor=accessor_index&accessor_href=accessor_index%3FSearchSource%253Autf-8%253Austring%3D" + encoded_name

            # skip
            if not name:
                self.skip("empty name")
                continue
            if self.name_already_processed(name):
                self.skip("duplicate name")
                continue

            bdes = biodes.BioDesDoc()
            bdes.from_args(naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = biourl,
                           url_publisher = "http://www.inghist.nl/",
                           text = snippet,
                           )
            self.write_file(bdes, index)

        
if __name__ == '__main__':
    m = Main()
    m.process()

