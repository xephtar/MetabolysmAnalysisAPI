import sqlite3
import xml.sax  # To access and parse the xml files without having to store the whole file on ram
import gzip  # To open .gz files
from decouple import config
import psycopg2
import datetime

DATABASE_NAME = config('DATABASE_NAME')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')

conn_str = "host=manny.db.elephantsql.com dbname={} user={} password={}".format(DATABASE_NAME, DATABASE_NAME,
                                                                                DATABASE_PASSWORD)
articleNum = 0
meshNum = 0
diseaseNum = 0


def stripString(name):
    """Strip string from redundant spaces and newlines."""
    return " ".join(name.split())


class MeshHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.conn = psycopg2.connect(conn_str)
        self.c = self.conn.cursor()
        # Variables to keep the important information you want to work with
        self.ArticleTitle = ''
        self.doi = ''
        self.AbstractText = ''
        self.PubDate = ''

        # Flags checking the element/tag being read
        self.inPubmedArticle = 0  # Flag for finishing getting the mesh info tuple (UI, name)
        self.inArticleTitle = 0
        self.inArticleId = 0
        self.inAbstractText = 0
        self.inPubDate = 0
        self.inYear = 0
        self.inMonth = 0
        self.inDay = 0
        self.inReference = 0

    # Call when an element starts
    def startElement(self, tag, attributes):
        # self.CurrentData = tag
        if tag == "PubmedArticle":
            self.ArticleTitle = ''
            self.doi = ''
            self.AbstractText = ''
            self.PubDate = ''
            self.inPubmedArticle = 1
        elif tag == "ArticleTitle":
            self.inArticleTitle = 1
        elif tag == "ReferenceList":
            self.inReference = 1
            self.inArticleId = 0
        elif tag == "ArticleId" and not self.inReference:
            self.doi = ''
            self.inArticleId = 1
        elif tag == "PubMedPubDate":
            self.PubDate = ''
            self.inPubDate = 1
        elif tag == "AbstractText":
            self.inAbstractText = 1
        elif tag == "Year":
            self.inYear = 1
        elif tag == "Month":
            self.inMonth = 1
        elif tag == "Day":
            self.inDay = 1

    # Call when an elements ends
    def endElement(self, tag):
        global articleNum
        # self.CurrentData = tag
        if tag == "PubmedArticle":
            self.inPubmedArticle = 0
            now = datetime.datetime.now()
            year = '{:02d}'.format(now.year)
            month = '{:02d}'.format(now.month)
            day = '{:02d}'.format(now.day)
            day_month_year = '{}-{}-{}'.format(year, month, day)
            print(articleNum)
            try:
                self.c.execute(
                    "INSERT INTO articles_article (abstract_text, pub_date, name, doi, created_at, updated_at, is_active) VALUES(%s, %s,%s, %s, %s, %s, true)",
                    (self.AbstractText, self.PubDate, self.ArticleTitle, self.doi, now, now))
                self.conn.commit()
            except Exception as inst:
                print(inst)

            print('#################\n')
            self.ArticleTitle = ''
            self.doi = ''
            self.AbstractText = ''
            self.PubDate = ''
            articleNum += 1

        elif tag == "ArticleTitle":
            self.inArticleTitle = 0
        elif tag == "ReferenceList":
            self.inReference = 0
        elif tag == "ArticleId":
            self.inArticleId = 0
        elif tag == "PubMedPubDate":
            self.inPubDate = 0
        elif tag == "AbstractText":
            self.inAbstractText = 0
        elif tag == "Year":
            self.inYear = 0
        elif tag == "Month":
            self.inMonth = 0
        elif tag == "Day":
            self.inDay = 0

    # Call when a character is read
    def characters(self, content):
        if self.inArticleTitle:
            self.ArticleTitle = self.ArticleTitle + content
        # character yerine text olarak okumaya
        elif self.inArticleId:
            self.doi = self.doi + content

        elif self.inPubDate:
            if self.inYear:
                self.PubDate += str(content)
            if self.inMonth:
                var = "-" + str(content) if len(content) == 2 else "-0" + str(content)
                self.PubDate += var
            if self.inDay:
                var = "-" + str(content) if len(content) == 2 else "-0" + str(content)
                self.PubDate += var

        elif self.inAbstractText:
            self.AbstractText = self.AbstractText + content

    # Call when parsing ends
    def endDocument(self):
        # Commiting our command
        self.conn.commit()

        # Close our connection
        self.c.close()


MESH_FILE = "pubmed21n1039.xml.gz"


def getMeshesInfo():
    """Get all Mesh info. Fills "meshes" table."""

    # Create and return a SAX XMLReader object.
    parser = xml.sax.make_parser()

    # override the default ContextHandler
    parser.setContentHandler(MeshHandler())
    parser.parse(gzip.open(MESH_FILE, 'rb'))


file_name = MESH_FILE + ".txt"

try:
    getMeshesInfo()
except Exception as e:
    print(e)
    print(MESH_FILE)
    f = open(file_name, "w")
    txt = "articleNum: {}".format(articleNum)
    f.write(txt)
    f.close()
