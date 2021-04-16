from bs4 import BeautifulSoup
import re

def GoogleScholarProfile(file,prefix='src_'):
    soup = BeautifulSoup(file, 'lxml') # Parse the HTML as a string
    tables = soup.find_all('table')
    if len(tables)>1:
        table =tables[1]
        rows=table.find_all('tr')

    scr_articles=[]
    i=-1
    for row in rows:
        i=i+1
        #*********************
        #Table have 3 columns without authentication (or checkbox column plus 3 columns with authentication): metadadata, citation info and year
        #... Extract the three columns: metadadata, citation info and year
        #... Initialize with non-authentication values
        m=0 # Initialize metada
        c=1 # Initialize citations
        y=2 # Initialize year
        cols=row.find_all('td')
        #...Check that is an article row 
        if len(cols)==0:
            #print('Entries',len(cols))
            continue
        elif len(cols)==4:
            m=m+1
            c=c+1
            y=y+1

        citedby=''; year=''
        if len(cols)>=3:
            metadata=cols[m]
            citedby=cols[c]
            year=cols[y]
        #*********************

        #Metadata scrapping    
        title=metadata.find('a').text
        authors=metadata.find_all('div')[0].text
        #*****************************
        #Metadata → Journal scrapping
        pub=metadata.find_all('div')[1].text.split(', ')
        pages=''
        if len(pub)==3:
            pages=pub[1]
        full_journal=pub[0]
        journal=pub[0]

        #...Intialize
        journal=full_journal
        volume=''
        issue=''
        #...Get real values
        s=re.split(r'\s([0-9]+)+\s',full_journal)
        if len(s)==1:
            s=re.split(r'\s([0-9]+)$',full_journal)
        if len(s)==1:
            s=s+['','']
        if len(s)==2:
            s=s+['']
        #Interpreat real values only if proper length
        if len(s)==3:
            journal=s[0]
            volume=s[1]
            issue=s[2]
        try:
            cite_id=citedby.find('a').get('href').split('cites=')[-1].split(',')[0]
        except:
            cite_id=None
        try:
            cites=citedby.find('a').text
        except:
            cites=None
        #*****************************

        #Fill dictionary
        d={}
        d[f'{prefix}title']=title
        d[f'{prefix}author']=authors
        d[f'{prefix}journal']=journal
        d[f'{prefix}volume']=volume
        d[f'{prefix}number']=issue
        d[f'{prefix}pages']=pages
        d[f'{prefix}year']=year.text
        d['cite_id']=cite_id
        d['cites']=cites
        if d:
            scr_articles.append(d)
        #if i==5:
        #    break
    return scr_articles

if __name__=='__main__':
    f=open('tests/test.html','r')
    file=f.read()
    f.close()
    l=GoogleScholarProfile(file)
    assert [d.get('cite_id') for d in l]==['8662367354358884167', '5671452052826898641', '']
    assert [d.get('cites') for d in l]==['108', '8', '']
    assert [d.get('src_journal') for d in l]==['arXiv preprint hep-ph/9906224', 'Physical Review D', '']
