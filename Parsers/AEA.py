from parsel import Selector
import re

name = 'AEA'

def parse_file(filename):
    result = {
        'title': "",
        'journal': "",
        'eissn': "",
        'pissn': "",
        'doi': "",
        'raw_url': "",

        'volume': "",
        'issue': "",
        'year': "",
        'pages': "",

        'authors': [],
        'institutions': [],
        'affiliations': [],
        'abstract': "",
        'keywords': [],
        'references': []
    }

    with open(filename, 'r', encoding="utf8", errors='ignore') as f:
        data = f.read()

    selector = Selector(text=data)

    s = selector.xpath('//title/text()').get()
    try:
        result['title'] = s
    except:
        result['title'] = None
        print(filename + ' title not found')

    s = selector.xpath('//span[@class="journal"]/text()').get()
    try:
        result['journal'] = s
    except:
        result['journal'] = None
        print(filename + ' journal not found')

    s = selector.xpath('//meta[@name="citation_issn"]')
    try:
        result['eissn'] = s.attrib['content']
    except:
        result['eissn'] = None
        print(filename + ' eissn not found')

    s = selector.xpath('//meta[@name="citation_doi"]')
    try:
        result['doi'] = s.attrib['content']
        result['raw url'] = 'https://www.aeaweb.org/articles?id=' + result['doi']
    except:
        result['doi'] = None
        print(filename + ' doi not found')

    s = selector.xpath('//meta[@name="citation_volume"]')
    try:
        result['volume'] = s.attrib['content']
    except:
        result['volume'] = None
        print(filename + ' volume not found')

    s = selector.xpath('//meta[@name="citation_issue"]')
    try:
        result['issue'] = s.attrib['content']
    except:
        result['issue'] = None
        print(filename + ' issue not found')

    s = selector.xpath('//meta[@name="citation_publication_date"]')
    try:
        result['year'] = s.attrib['content'].split('/')[0]
    except:
        result['year'] = None
        print(filename + ' year not found')

    s = [selector.xpath('//meta[@name="citation_firstpage"]'),
         selector.xpath('//meta[@name="citation_lastpage"]')]
    try:
        result['pages'] = s[0].attrib['content'] + '-' + s[1].attrib['content']
    except:
        result['pages'] = None
        print(filename + ' pages not found')

    s = [selector.xpath('//meta[@name="citation_author"]'),
         selector.xpath('//meta[@name="citation_author_institution"]')]
    try:
        for a in list(zip(*s)):
            auth = ' '.join(a[0].attrib['content'].split(', ')[::-1])
            inst = a[1].attrib['content']
            if auth:
                result['authors'].append(auth)
                if inst:
                    result['affiliations'].append({'author': auth, "affiliations": [inst]})
                    result['institutions'].append(inst)

        result['authors'] = result['authors'] if result['authors'] else None
        result['affiliations'] = result['affiliations'] if result['affiliations'] else None
        result['institutions'] = result['institutions'] if result['institutions'] else None
    except:
        print(filename + ' authors and institutions not found')

    s = selector.xpath('//section[@class="article-information abstract"]').get()
    try:
        s = " ".join(s.split())
        s = Selector(text=s).xpath('//section/text()')[1].get()
        result['abstract'] = s
    except:
        result['abstract'] = None
        print(filename + ' abstract not found')

    s = selector.xpath('//ul[@class="jel-codes"]').get()
    try:
        s = list(map(lambda x: x.split('; '), re.findall(r'>\n+\t+([A-Z].*)\n*\t*<', s)))
        result['keywords'].extend([tag for code in s for tag in code])
    except:
        result['keywords'] = None
        print(filename + ' keywords not found')

    return result
