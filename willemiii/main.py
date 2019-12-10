import os
import re
import urllib
from hashlib import md5
from lxml import etree
from biodes import BioDesDoc
from sutils import Base, sanitize_name

DEVNULL = open(os.devnull, 'w')


class Main(Base):

    def read(self):
        people_dict = {}
        for file in ('in/1.xml', 'in/2.xml', 'in/3.xml', 'in/4.xml', 'in/5.xml'):
            tree = etree.parse(open(file, 'r'))
            items = tree.xpath("/*/item")
            for iteration, bio in enumerate(items):
                self.total += 1
                try:
                    name1 = sanitize_name(bio.xpath('title/from')[0].text)
                except IndexError:
                    name1 = None
                else:
                    people_dict[name1] = {}
                try:
                    name2 = sanitize_name(bio.xpath('title/to')[0].text)
                except IndexError:
                    name2 = None
                else:
                    people_dict[name2] = {}
        return people_dict

    def write(self, people_dict):
        people = people_dict.keys()
        people.sort()
        self.total = len(people)
        for index, name in enumerate(people):
            index += 1
            info = people_dict[name]
            self.print_progress(index, name)
            # URL
            base_dev = "http://dev.inghist.nl/retrotest2010/willemiii/"
            base_production = "http://www.inghist.nl/retroboeken/willemiii/"           
            anchor = "#accessor=toc1&accessor_href=toc1%3Fvan_aan%3D%26correspondent%253Austring%253Autf-8%3D"
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = base_production + \
                  anchor + \
                  encoded_name 
#                  "%26day1%3D%26month1%3D%26year1%3D%26day2%3D%26month2%3D%26year2%3D"         
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
    people_dict = r.read()
    r.write(people_dict)


