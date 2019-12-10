import os
import urllib

from lxml import etree

from biodes import BioDesDoc
from sutils import Base, sanitize_name
from gerbrandyutils import sh


class Main(Base):

    def download(self):
        urls = """\
        http://www.inghist.nl/retroapp/service_archives/01_01/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_02/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_03/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_04/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_05/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_06/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_07/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_08/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_supplement/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/01_table/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/02_01/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/02_02/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/02_03/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/02_04/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/02_05/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/03_01/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/03_02/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/03_03/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/04_01/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/04_02/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/04_03/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/04_04/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/04_supplement/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/05_01/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/05_02/toc_xml_source?filename=*AK.xml
        http://www.inghist.nl/retroapp/service_archives/05_03/toc_xml_source?filename=*AK.xml"""
        for index, url in enumerate(urls.split('\n'), 1):
            url = url.strip()
            sh("wget %s -O in/%s.xml" % (url, index))
        
    def process(self):
        names = []
        for file in os.listdir('in'):
            tree = etree.parse("in/" + file)
            entries = tree.xpath("//item")
            for index, person in enumerate(entries, 1):
                self.total += 2
                try:
                    name1 = person.xpath('title/from')[0].text
                except IndexError:
                    name1 = None
                try:
                    name2 = person.xpath('title/to')[0].text
                except IndexError:
                    name2 = None
                    
                
                for name in (name1, name2):
                    if name == "...." or not name:
                        self.skip("null name")
                        continue
                    if name.replace('.', '').strip() == "":
                        self.skip("null name")
                        continue
                    if name in names:
                        self.skip("dupe name")
                        continue
                    names.append(name)
                   
        for index, name in enumerate(names, 1):
            base_production = "http://www.inghist.nl/retroboeken/archives/"
            anchor = "#accessor=toc&accessor_href=toc%3Fcorrespondent%253Austring%253Autf-8%3D"
            encoded_name = urllib.quote(urllib.quote(name.encode('utf8')))
            url = base_production + \
                  anchor + \
                  encoded_name 
            bdes = BioDesDoc()
            args = dict(naam = name,
                        naam_publisher = "Instituut voor Nederlandse Geschiedenis",
                        url_publisher = "http://www.inghist.nl/",
                        url_biografie = url,
                       )               
            bdes.from_args(**args)
            self.write_file(bdes, index)


if __name__ == '__main__':
    if not os.path.isdir('in'):
        os.mkdir('in')
    m = Main()
#    m.download()
    m.process()

