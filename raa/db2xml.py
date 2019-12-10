#!../../../bin/python
##---- Lokale settings
base_url = 'http://www.historici.nl/Onderzoek/Projecten/Repertorium/app/personen'
out_fn = 'namenindex_raa.xml'
#------- MySQL Db stuff
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, String, ForeignKey, Table, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relation, backref, scoped_session
from sqlalchemy.orm.query import Query
from biodes.biodes10 import BioDesDoc
from gerbrandyutils import sh
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(this_dir, 'out')

Base = declarative_base()
metadata = Base.metadata 
engine = create_engine('mysql://root@localhost/webraa')

Session = sessionmaker(bind=engine)

class AdellijkeTitel(Base):
    __tablename__ = 'adellijke_titel'
    id = Column(Integer,primary_key=True)
    naam = Column(String)

class AcademischeTitel(Base):
    __tablename__ = 'academische_titel'
    id = Column(Integer,primary_key=True)
    naam = Column(String)

class Persoon(Base):
    __tablename__ = 'persoon'
    id = Column(Integer,primary_key=True)
    voornaam = Column(String)
    tussenvoegsel = Column(String)
    geslachtsnaam = Column(String)
    geboortedatum = Column(String) #yyyy-mm-dd
    geboorteplaats = Column(String)
    overlijdensdatum = Column(String) #yyyy-mm-dd
    overlijdensplaats = Column(String)
    adellijketitel_id = Column(Integer, ForeignKey('adellijke_titel.id'))
    adellijke_titel = relation(AdellijkeTitel, backref="personen")
    academischetitel_id = Column(Integer, ForeignKey('academische_titel.id'))
    academische_titel = relation(AcademischeTitel, backref='personen')

class Alias(Base):
    __tablename__ = 'alias'
    id = Column(Integer, primary_key=True)
    naam = Column(String)
    persoon_id = Column(Integer, ForeignKey('persoon.id'))
    persoon = relation(Persoon, backref='aliassen')


#------- Namenindex stuff ----------
#from NamenIndex.namenindex import NamenIndex
#
from names import Naam
import os
import re
import urllib
from hashlib import md5
from lxml import etree
from sutils import Base, sanitize_name, compress_output_files
from biodes import BioDesDoc


class Main(Base):
    def write(self):
        session=Session() 
        i = 0
        for r in session.query(Persoon).all():
            i += 1
            prepositie= ''
            intrapositie = ''
    
            if r.adellijke_titel and r.adellijke_titel.naam:
                if r.adellijke_titel.naam.lower() == 'jonkheer':
                    prepositie +=  'jonkheer '
                else:
                    intrapositie += r.adellijke_titel.naam
    
            if r.academische_titel and r.academische_titel.naam:
                prepositie += unicode(r.academische_titel.naam, 'latin1') 
    
            if r.tussenvoegsel:
                intrapositie += ' ' + unicode(r.tussenvoegsel, 'latin1')
    
            prepositie = prepositie.strip()
            intrapositie = intrapositie.strip()
            naam = Naam(
                    prepositie=prepositie,
                    voornaam=unicode(r.voornaam or '', 'latin1') ,
                    intrapositie=intrapositie,
                    geslachtsnaam=unicode(r.geslachtsnaam or '', 'latin1') ,
                    )
         
            aliassen = [Naam(unicode(alias.naam, 'latin1')) for alias in r.aliassen]
            names =  [naam] + aliassen
            for n in names:
                assert isinstance(n, Naam), names
            print 'adding %s' % names[0]
            biodesdoc = BioDesDoc()
            self.print_progress(i, names[0])
    
            bdate = r.geboortedatum and str(r.geboortedatum) or ''
            if bdate.endswith('-01-01') or bdate.endswith('-12-31'): 
                bdate = bdate[:4]
    
            ddate = r.overlijdensdatum and str(r.overlijdensdatum) or ''
            if ddate.endswith('-01-01') or ddate.endswith('-12-31'): 
                ddate = ddate[:4]
                
            try:
                birth_place = r.geboorteplaats and unicode(r.geboorteplaats) or ''
                death_place = r.overlijdensplaats and unicode(r.overlijdensplaats) or ''
            except:
                birth_place = r.geboorteplaats and unicode(r.geboorteplaats, 'latin1') or ''
                death_place = r.overlijdensplaats and unicode(r.overlijdensplaats, 'latin1') or ''
        
            biodesdoc.from_args(
                names = names,
                birth_date=bdate or '',
                birth_place=birth_place or '',
                death_date = ddate or '',
                death_place = death_place or '',
                url_biografie='%s/%s' %( base_url, r.id),
    #            url_description='Repertorium van Ambtsdragers',
                naam_publisher="RAA",
                url_publisher=base_url,
                )
            self.write_file(biodesdoc, r.id, folder_name=OUT_DIR)
    
def create_files():
    for x in os.listdir(OUT_DIR):
        fn = os.path.join(OUT_DIR, x)
        if os.path.isfile(fn):
            os.remove(fn)
    r.write()
    compress_output_files(OUT_DIR)
def upload_results():
    cmd = 'cd %s;svn ci . -m ""' % this_dir
    print cmd
    sh(cmd)
    
    

def refresh_bioport_test(): 
    x = urllib.urlopen('http://jelle:j3ll3@dev.inghist.nl/bioport/admin/source?source_id=raa&form.actions.download_biographies=1')
    print x.read()
    
if __name__ == '__main__':
    r = Main()
#    
#    print 'creating files'
    create_files()
    import ipdb;ipdb.set_trace() 
    compress_output_files(OUT_DIR)
    print 'uploading'
    import ipdb;ipdb.set_trace() 
    upload_results()
    print 'refresh bioport test (will take a while...)'
    refresh_bioport_test()
    print 'done!'
