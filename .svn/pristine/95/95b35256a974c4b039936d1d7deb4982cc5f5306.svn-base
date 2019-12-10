import os
import urllib
from lxml import etree
from sutils import Base, sanitize_name
from biodes import BioDesDoc


class Main(Base):

    def read(self):
        people_dict = {}
        tree = etree.parse(open('in/input.xml', 'r'))
        for index, bio in enumerate(tree.xpath("/*/item")):
            # Name
            text = bio.find('title').text
            if text == None or text.count(' aan ') != 1:
                continue               
            for name in text.split('aan'):
                name = sanitize_name(name)
                # URL
                base_dev = "http://dev.inghist.nl/retrotest2010/staatsregeling/"
                base_production = "http://www.inghist.nl/retroboeken/staatsregeling/"
                anchor = "#accessor=toc1&accessor_href=toc1%3FSearchSource%3D"
                encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
                url = base_production + \
                      anchor + \
                      encoded_name
                people_dict[name] = {"url":url}
        return people_dict
        
    def write(self, people):
        self.total = len(people)
        for index, name in enumerate(people):
            if self.name_already_processed(name):
                self.skipped += 1
                continue
            url = people[name]['url']
            bdes = BioDesDoc()
            args = dict(naam = name,
                        naam_publisher = "XXX",
                        url_publisher = "http://XXX.nl",
                        url_biografie = url,
                        )
            bdes.from_args(**args)
            self.write_file(bdes, index)


if __name__ == '__main__':
    m = Main()
    people = m.read()
    m.write(people)

