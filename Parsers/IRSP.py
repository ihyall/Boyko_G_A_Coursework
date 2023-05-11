from parsel import Selector
import re

name = 'CSH'


def parse_file(filename):
    result = {
        'title': "",
        'journal': "",
        'journal abbrev': "",
        'journal short abbrev': "",
        'pissn': "",
        'eissn': "",
        'doi': "",
        'raw_url': "",

        'volume': "",
        'year': "",
        'pages': "",

        'authors': [],
        'affiliations': [],
        'institutions': None,
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

    s = selector.xpath('//meta[@name="citation_journal_abbreviation"]')
    if s:
        result['journal abbrev'] = s[0].attrib['content']
        result['journal short abbrev'] = s[1].attrib['content']
    else:
        print(filename + ' journal abbrev not found')

    s = selector.xpath('//meta[@name="citation_issn"]')
    if s:
        result['pissn'] = s[1].attrib['content']
        result['eissn'] = s[0].attrib['content']
    else:
        print(filename + ' issn not found')

    s = selector.xpath('//meta[@name="citation_doi"]')
    if s:
        result['doi'] = s.attrib['content']
    else:
        print(filename + ' doi not found')

    s = selector.xpath('//meta[@name="citation_abstract_html_url"]')
    if s:
        result['raw_url'] = s.attrib['content']
    else:
        print(filename + ' raw url not found')

    s = selector.xpath('//meta[@name="citation_volume"]')
    if s:
        result['volume'] = s.attrib['content']
    else:
        print(filename + ' volume not found')

    s = selector.xpath('//meta[@name="citation_publication_date"]')
    if s:
        result['year'] = s.attrib['content'].split('/')[0]
    else:
        print(filename + ' year not found')

    s_f = selector.xpath('//meta[@name="citation_firstpage"]')
    s_l = selector.xpath('//meta[@name="citation_lastpage"]')
    if s_f and s_l:
        result['pages'] = s_f.attrib['content'] + '-' + s_l.attrib['content']
    else:
        print(filename + ' pages not found')

    s_auth = selector.xpath('//div[@class="bb"]/h3/text()').getall()
    s_auth_sup = [re.findall(r'(\d+)', sup) for sup in selector.xpath('//div[@class="bb"]/h3/sup/text()').getall()]
    s_org = selector.xpath('//div[@class="author_address"]/descendant-or-self::*[not(name()="sup" or name()="i")]/text()').getall()

    try:
        s_auth.pop(s_auth.index('\n'))
        for i in range(len(s_auth)):
            auth = s_auth[i].replace('*', '').replace(', ', '')
            result['authors'].append(auth)
            if s_auth_sup:
                affil = {'author': auth, 'affiliations': []}
                for j in range(len(s_auth_sup[i])):
                    for sup in s_auth_sup[i][j]:
                        sup = int(sup)-1
                        affil['affiliations'].append(s_org[sup])
                result['affiliations'].append(affil)
            if not result['affiliations']:
                raise
        if not result['authors']:
            raise
    except:
        result['authors'] = ' '.join(selector.xpath('//div[@class="bb"]/h3/descendant-or-self::*/text()').getall())
        result['affiliations'] = None
        result['institutions'] = ' '.join(selector.xpath('//div[@class="author_address"]/descendant-or-self::*[not(name()="i")]/text()').getall())


    s = selector.xpath('//p[@class="abstract_block"]/descendant-or-self::*/text()').getall()
    if s:
        result['abstract'] = ' '.join(' '.join(i.split()) for i in s).replace('ABSTRACT: ', '')
    else:
        print(filename + ' abstract not found')

    return result
