import os
import re
import urllib
import codecs
from hashlib import md5
from lxml import etree
from sutils import Base, sanitize_name
from biodes import BioDesDoc

ENCODING = 'latin-1'


class Main(Base):

    def read(self):
        names = []
        urls = [
                "http://www.inghist.nl/retroapp/service_gachard/gachard_1/toc_xml_source?filename=*.xml", 
                "http://www.inghist.nl/retroapp/service_gachard/gachard_2/toc_xml_source?filename=*.xml", 
                "http://www.inghist.nl/retroapp/service_gachard/gachard_3/toc_xml_source?filename=*.xml", 
                "http://www.inghist.nl/retroapp/service_gachard/gachard_4/toc_xml_source?filename=*.xml", 
                "http://www.inghist.nl/retroapp/service_gachard/gachard_5/toc_xml_source?filename=*.xml", 
                "http://www.inghist.nl/retroapp/service_gachard/gachard_6/toc_xml_source?filename=*.xml", 
                ]
                
        for url in urls:
            tree = etree.parse("http://www.inghist.nl/retroapp/service_gachard/gachard_3/toc_xml_source?filename=*.xml")
            items = tree.xpath("/*/item")
            for iteration, bio in enumerate(items):
                try:
                    n1 = bio.xpath('title/from')[0].text
                except IndexError:
                    n1 = None
                try:
                    n2 = bio.xpath('title/to')[0].text
                except IndexError:
                    n2 = None
                if n1 is not None:
                    names.append(n1)
                if n2 is not None:
                    names.append(n2)
        return names

    def write(self, names):
        names.sort()
        self.total = len(names)
        for index, name in enumerate(names):
            index += 1
           
            name = sanitize_name(name)
            if self.name_already_processed(name):
                self.skip("dupe name")
                continue
            # URL
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = "http://www.inghist.nl/retroboeken/gachard/#accessor=toc&accessor_href=toc%3FSearchSource%253Austring%253Autf-8%3D%26van_aan%3D%26correspondent%253Austring%253Autf-8%3D" + encoded_name

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

