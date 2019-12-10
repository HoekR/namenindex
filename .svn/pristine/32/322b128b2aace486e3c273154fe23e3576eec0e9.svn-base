import os
import re
from hashlib import md5
import urllib

from lxml import etree
from biodes import BioDesDoc
from sutils import Base, sanitize_name


class Read:

    def get_name_and_date(self, text):
        # first occurrence of " (xxxx-xxxx)"
        expr = r'(\d{4}-\d{4})'
        date = re.findall(expr, text)
        if date:
            name = text[:re.search(expr, text).start()]
            if name.endswith('('):
                name = name[:-1]
            name = name.strip()
            born, dead = date[0].split('-')
            return name, born, dead

        # first occurrence of " (xxxxxxxx)"
        expr = r'\((\d{8})\)'
        date = re.findall(expr, text)
        if date:
            name = text[:re.search(expr, text).start()]
            if name.endswith('('):
                name = name[:-1]
            name = name.strip()
            born = date[0][:4]
            dead = date[0][4:]
            return name, born, dead
        return ()

    def process(self):
        people_dict = {}
        tree = etree.parse(open('in/input.xml', 'r'))
        items = tree.xpath("/*/item")
        for iteration, bio in enumerate(items):
            line = bio.find('name').text
            if line.startswith('* '):
                line = line[2:]
            if line.endswith(':'):
                line = line[:-1]
            line = line.replace('. . .', '')
            line = line.strip()
            name_and_date = self.get_name_and_date(line)
            if name_and_date:
                name, born, dead = name_and_date
            else:
                name = line
                born, dead = None, None
            people_dict[name] = {'born':born, 'dead':dead}
        return people_dict


class Write(Base):

    def process(self, people_dict):
        people = people_dict.keys()
        people.sort()
        self.total = len(people)
        x = 0
        for name in people:
            x += 1
            info = people_dict[name]
            print "processing: %s/%s - %s" %(x, len(people), name)
            name = sanitize_name(name)
            if self.name_already_processed(name):
                self.skipped += 1
                continue           
            
            # URL
            base_dev = "http://dev.inghist.nl/retrotest2010/groen/"
            base_production = "http://www.inghist.nl/retroboeken/groen/"                          
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = base_production + \
                  "#accessor=accessor_index&accessor_href=accessor_index%3FSearchSource%253Autf-8%253Austring%3D" + \
                  encoded_name
            
            bdes = BioDesDoc()
            args = dict(naam = name,
                        naam_publisher = "XXX",
                        url_publisher = "http://XXX.nl",
                        url_biografie = url,
                   )
            """
            args = dict(naam = name,
                        figures =[(people_dict[id]['img_url'], 
                                   people_dict[id]['caption'],
                                  )],
                        naam_publisher = "Het Geheugen van Nederland",
                        url_biografie = people_dict[id]['bio_url'],
                        url_publisher = "http://geheugenvannederland.nl",
                        tekst = people_dict[id]['tekst']
                        )
            """
            birth_date = info['born']
            death_date = sterfdatum = info['dead']
            if bdes.is_date(birth_date):
                args['geboortedatum'] = birth_date
            if bdes.is_date(death_date):
                args['sterfdatum'] = death_date
                
            bdes.from_args(**args)
            self.write_file(bdes, x)


def main():
    assert os.path.isfile("in/input.xml"), "Input file does not exist"
    r = Read()
    people_dict = r.process()
    w = Write()
    w.process(people_dict)


if __name__ == '__main__':
    main()

