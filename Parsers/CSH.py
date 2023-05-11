from parsel import Selector
import re

name = 'CSH'

def parse_file(filename):
    result = {
        'title': "",
        'journal': "",
        'journal abbrev': "",
        'print issn': "",
        'online issn': "",
        'doi': "",
        'raw url': "",

        'volume': "",
        'issue': "",
        'date': "",
        'first page': "",
        'last page': "",

        'authors': [],
        'institutions': [],
        'abstract': "",

    }

    with open(filename, 'r', encoding="utf8", errors='ignore') as f:
        data = f.read()

    selector = Selector(text=data)

    s = selector.xpath('//meta[@name="citation_title"]')
    if s:
        result['title'] = s.attrib['content']
    else:
        print(filename + ' title not found')

    s = selector.xpath('//meta[@name="citation_journal_title"]')
    if s:
        result['journal'] = s.attrib['content']
    else:
        print(filename + ' journal not found')

    s = selector.xpath('//meta[@name="citation_journal_abbrev"]')
    if s:
        result['journal abbrev'] = s.attrib['content']
    else:
        print(filename + ' journal abbrev not found')

    s = selector.xpath('//meta[@name="citation_issn"]')
    if s:
        result['print issn'] = s[0].attrib['content']
        result['online issn'] = s[1].attrib['content']
    else:
        print(filename + ' issn not found')

    s = selector.xpath('//meta[@name="citation_doi"]')
    if s:
        result['doi'] = s.attrib['content']
    else:
        print(filename + ' doi not found')

    s = selector.xpath('//meta[@name="citation_public_url"]')
    if s:
        result['raw url'] = s.attrib['content']
    else:
        print(filename + ' raw url not found')

    s = selector.xpath('//meta[@name="citation_volume"]')
    if s:
        result['volume'] = s.attrib['content']
    else:
        print(filename + ' volume not found')

    s = selector.xpath('//meta[@name="citation_issue"]')
    if s:
        result['issue'] = s.attrib['content']
    else:
        print(filename + ' issue not found')

    s = selector.xpath('//meta[@name="citation_date"]')
    if s:
        result['date'] = s.attrib['content']
    else:
        print(filename + ' date not found')

    s = selector.xpath('//meta[@name="citation_firstpage"]')
    if s:
        result['first page'] = s[0].attrib['content']
    else:
        print(filename + ' first page not found')

    s = selector.xpath('//meta[@name="citation_lastpage"]')
    if s:
        result['last page'] = s[0].attrib['content']
    else:
        print(filename + ' last page not found')

    s = selector.xpath('//meta[@name="citation_author"]')
    if s:
        for auth in s:
            result['authors'].append(auth.attrib['content'])
    else:
        result['authors'] = None
        print(filename + ' authors not found')

    s = selector.xpath('//ol[@class="affiliation-list"]/li/address/text()')
    if s:
        for i in s:
            result['institutions'].append(' '.join(i.get().split()).replace(';', ''))
    else:
        result['institutions'] = None
        print(filename + ' institutions not found')

    s = selector.xpath('//div[@class="section abstract"]/p/descendant-or-self::*/text()') # selector.xpath('//div[@class="section abstract"]/p/em/text()')
    if s:
        result['abstract'] = ' '.join(' '.join(i.get().split()) for i in s)
    else:
        print(filename + ' abstract not found')

    return result
