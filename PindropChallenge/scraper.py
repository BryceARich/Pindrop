from urllib import FancyURLopener
from bs4 import BeautifulSoup

PHONE_SITE = 'http://gsd-auth-callinfo.s3-website.us-east-2.amazonaws.com/'

class ValidUAOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)'

class PhoneNumberEntry:
    def __init__(self, phone_number, report_count, comment):
        if(phone_number[:1] != u'('):                       #handles the case where phonenumber is of the form (###)#######
            self.area_code  = phone_number[:3]
        else :
            self.area_code  = phone_number[1:4]
        self.phone_number = phone_number
        if(type(report_count) == unicode): # probably a better way to indicate if it is a reading from a web scrape or from the database
            comment = comment[:-21]# remove unnecesary kdxyiun2 6s,so,ltz,fz at the end of each string TODO figure out why this is showing up to find a better long term
        self.report_count = int(report_count) #cast to integer so that the database type is the same as the web scraped type this way the __eq__ function works
        self.comment      = comment.replace('"', '\\"') 

    def __unicode__(self):
        skeleton = u'{{ "area_code": "{}", "phone_number": "{}", "report_count": "{}", "comment": "{}" }}'
        return skeleton.format(self.area_code, self.phone_number, self.report_count, self.comment)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return unicode(self).encode('utf-8')

    #added for comparison of Phone Number Entry classes to ensure database stores the same data as what was webscraped
    def __eq__(self,other):
        if isinstance(self,other.__class__):
            return (self.__dict__ == other.__dict__)
        else:
            return False


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def entry_parse(self, html):
        num_of_reports = html.find(class_='oos_previewSide').getText()
        number         = html.find(class_='oos_previewHeader').getText()
        comment        = html.find('div', class_='oos_previewBody').getText()
        return PhoneNumberEntry(number, num_of_reports, comment)

    def parse(self):
        latest_entries = self.soup.find('ul', id='previews').find_all('li', class_='oos_listItem')
        print latest_entries
        return map(self.entry_parse, latest_entries)

## Main

if __name__ == "__main__":
    parser = Parser(ValidUAOpener().open(PHONE_SITE).read())
    print parser.parse()
