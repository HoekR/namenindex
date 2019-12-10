#!/usr/bin/env python

import urllib
import pickle
import os
import re
import atexit
import tarfile
from lxml import etree

from BeautifulSoup import BeautifulSoup

import biodes
from gerbrandyutils import normalize_url

from sutils import Base, sanitize_name


class Main(Base):

    # XXX - dall'HTML (vecchio)
    
    def read_data(self):
        if os.path.isfile('cache/persons-data.pickle'):
            return pickle.load(open('cache/persons-data.pickle', 'r'))

        persons_data = []

        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            url = "http://www.inghist.nl/Onderzoek/Projecten/Thorbecke/index/%s.htm" % letter.lower()
            print url
            f = urllib.urlopen(url)
            data = f.read()
            f.close()
            soup = BeautifulSoup(data)
            div = soup.findAll("div", {"id" : "content-text"})[0]
            pis = div.findAll("p")
            for p in pis:
                persons_data.append(p.renderContents())

        pickle.dump(persons_data, open('cache/persons-data.pickle', 'w'))        
        return persons_data
        
    # XXX - dall'XML (nuovo)
        
    def read_data(self):
        persons_data = []
        tree = etree.parse(open('input.xml', 'r'))
        items = tree.xpath("/*/item/name")
        for iteration, bio in enumerate(items):
            text = bio.text
            persons_data.append(text)
        return persons_data

    def get_name_date_and_descr(self, text):
    
        def execute(pattern):
            date = re.findall(pattern, text)
            if date:
                name = text[:re.search(pattern, text).start()]
                try:
                    born, dead = date[0].split('-')
                except ValueError:
                    born = date[0]
                    dead = ''
                if born:
                    born = born.zfill(4)
                if dead:
                    dead = dead.zfill(4)
                if "v. chr" in text.lower():  # avanti cristo, biodes vuole un negativo
                    if born:
                        born = "-" + born
                    if dead:
                        dead = "-" + dead
                # XXX - retrieve text, this is not common to other scripts
                descr = text[re.search(pattern, text).end():]
                if descr.startswith(','):
                    descr = descr[1:]
                descr = descr.strip()
                return name, born, dead, descr
            else:
                return ()
            
        patterns = [
                    r', (\d{4}-\d{4})',     # first occurrence of ", xxxx-xxxx"
                    r', ca. (\d{4}-\d{4})', # first occurrence of ", ca. xxxx-xxxx"
                    r', geb. (\d{4})',      # first occurrence of ", geb. xxxx"        
                    r', geb. ca. (\d{4})',  # first occurrence of ", geb. ca. xxxx"
                    r', (\d{3}-\d{3})',     # first occurrence of ", xxx-xxx"
                    r', ca. (\d{3}-\d{3})', # first occurrence of ", ca. xxx-xxx"
                   ]
                      
        for p in patterns:
            ret = execute(p)
            if ret:
                break 
        return ret
        
    def write_data(self, persons):
        self.total = len(persons)
        for index, text in enumerate(persons):
            name_and_date = self.get_name_date_and_descr(text)
            if ' zie ' in text:
                continue
            
            if not name_and_date:
                self.skipped += 1
                continue

            name, born, dead, descr = name_and_date
            if self.name_already_processed(name):
                self.skipped += 1
                continue
                
            base_dev = "http://dev.inghist.nl/retrotest2010/thorbecke/"
            base_production = "http://www.inghist.nl/retroboeken/thorbecke/"                          
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = base_production + "#accessor=accessor_index&accessor_href=accessor_index%3FSearchSource%253Autf-8%253Austring%3D" + encoded_name
            bdes = biodes.BioDesDoc()
            bdes.from_args(
                           naam = name,
                           naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                           url_biografie = url,
                           url_publisher = "http://www.inghist.nl/",
                           birth_date = born,
                           death_date = dead,
                           text = descr,
                           )
            self.write_file(bdes, index + 1)


if __name__ == '__main__':      
    if not os.path.isdir('cache'):
        os.mkdir('cache')

    r = Main()
    persons = r.read_data()
    r.write_data(persons)
    r.tear_down()

