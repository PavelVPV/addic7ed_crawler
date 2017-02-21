#
#  Copyright (c) 2017 Pavel Vasilyev
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import urllib, urllib2
from BeautifulSoup import *

addicted_url="http://www.addic7ed.com/"
search_ext="search.php?Submit=Search&search="

def get_opener(hdr = None):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0')]
    if hdr is not None :
        opener.addheaders.append(hdr)
    return opener

def perform_search(what):
    url = addicted_url + search_ext + urllib.quote_plus(what)
    print "URL: " + url
    #html = urllib.urlopen(addicted_url + search_ext + urllib.quote_plus(what)).read()
   
    html = get_opener().open(url).read()
    
    #print html
    
    soup = BeautifulSoup(html)
    body = soup.body
    
    ### the third contains results
    navstr = body.contents[3]
    
    # The first table contains results count
    res_count = str(navstr.table.b.contents[0])
    print 'Res count:'
    print res_count
    print '\n'
    
    # The second one contains actual results
    refs = []
    for table in navstr.find('table', recursive=False):
        #print 'Found table:'
        #print table
        #print '<<<'

        a = table.find('a')
        if a is None or a == -1:
            continue
        
        #print a
        
        href = str(a.get('href'))
        name = str(a.contents[0])
        refs.append((name,href))

    print 'Please choise the result or -1 to abort'
        
    i = 1
    for item in refs :
        print str(i) + '. ' + item[0]
        i += 1
        
    r = int(raw_input('Choise: '))
    
    if r == -1: return -1
    return refs[r - 1][1]
    
def get_list_of_subtitles(link):
    url = addicted_url + link
    print 'URL: ' + addicted_url + link
    
    #html = urllib.urlopen(addicted_url + link).read()
    html = get_opener().open(url).read()
    
    soup = BeautifulSoup(html)
    
    refs = {}

    for table in soup.findAll("table", { "class" : "tabel95" }):
        #print 'Found table:'
        #print table
        #print '<<<\n\n\n\n\n\n\n\n\n'
        
        version = table.findAll("td", { "colspan" : "3", "align" : "center", "class" : "NewsTitle" } )
        if version is None or len(version) < 1:
            continue
            
        version = str(version[0].contents[1])
        
        #print "Version: " + version
        
        lang = table.findAll("td", { "class" : "language" })
        
        if lang is None or len(lang) < 1:
            continue
            
        lang = str(lang[0].contents[0])
        
        #print "Language: " + lang
        
        link = table.findAll("a", { "class" : "buttonDownload" })
        
        if link is None or len(link) < 1:
            continue
            
        link = str(link[0].get('href'))
        
        #print "Link: " + link
        
        newsDate = table.findAll("td", { "class" : "newsDate", "colspan" : "2" })
        
        if newsDate is None or len(newsDate) < 1:
            continue
            
        newsDate = str(newsDate[0].contents[2])
        
        #print "News Date: " + newsDate
        
        refs[link] = (version, lang, newsDate)
            
    print 'Please choise the result or -1 to abort:'
            
    i = 1
    for k in refs:
        version,lang,newsDate = refs[k]
        print str(i) + ". " + version + " | " + lang + " | " + newsDate
        i += 1
        
    r = int(raw_input('Choise: '))
    
    if r == -1: return -1
    return refs.keys()[r - 1]
    
def download_subs(link, referer):
    url = addicted_url + link
    print "URL: " + url
        
    #req = urllib2.Request(addicted_url + link)
    #req.add_header("Referer", addicted_url + referer)
    
    #u = urllib2.urlopen(req)
    u = get_opener(("Referer", addicted_url + referer)).open(url)
    meta = u.info()
    
    file_name = meta.getheaders("Content-Disposition")[0].split('=')[1]
    
    # Get rid of quotes and colon
    file_name = file_name[1:-1].replace(':','_')
    
    print "File name: " + file_name
    
    f = open(file_name, 'wb')

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d" % (file_size_dl)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    
name_to_search = raw_input("Enter Serial Name: ")
    
result_link = perform_search(name_to_search)
sub = get_list_of_subtitles(result_link)
download_subs(sub, result_link)
