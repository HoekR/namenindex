import os
import re
import urllib
from hashlib import md5
from lxml import etree
from sutils import Base, sanitize_name
from biodes import BioDesDoc


class Main(Base):

    def read(self):
        names = []
        lower_case_names = set()
        for file in ('in/1.xml', 'in/2.xml', 'in/3.xml'):
            tree = etree.parse(open(file, 'r'))
            items = tree.xpath("/*/item")
            for iteration, bio in enumerate(items):
                try:
                    name1 = sanitize_name(bio.xpath('title/from')[0].text)
                except IndexError:
                    name1 = None
                try:
                    name2 = sanitize_name(bio.xpath('title/to')[0].text)
                except IndexError:
                    name2 = None
                
                for name in (name1, name2):
                    if not self.name_already_processed(name):
                        names.append(name)
        return names

    def write(self, names):
        names.sort()
        self.total = len(names)
        for index, name in enumerate(names):
            index += 1
            self.print_progress(index, name)
            
            # URL
            base_dev = "http://dev.inghist.nl/retrotest2010/oldenbarnevelt/"
            base_production = "http://www.inghist.nl/retroboeken/oldenbarnevelt/"
            anchor = "#accessor=toc&accessor_href=toc%3FSearchSource%3D"
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = base_production + \
                  anchor + \
                  encoded_name + \
                  "%26correspondent%3D%26day1%3D%26month1%3D%26year1%3D%26day2%3D%26month2%3D%26year2%3D"
            bdes = BioDesDoc()
            args = dict(naam = name,
                        naam_publisher = "XXX",
                        url_publisher = "http://XXX.nl",
                        url_biografie = url,
                       )               
            bdes.from_args(**args)
            self.write_file(bdes, index)


if __name__ == '__main__':
    r = Main()
    names = r.read()
    r.write(names)


