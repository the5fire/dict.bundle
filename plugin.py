# coding:utf-8
from __future__ import unicode_literals

import urllib2
import urllib
import xml.etree.ElementTree as ET

KEY = 'E0F0D336AF47D3797C68372A869BDBC5'
URL = 'http://dict-co.iciba.com/api/dictionary.php'


def get_response(word):
    word = word.encode('utf8')
    query = urllib.quote_plus(word)
    return urllib2.urlopen(URL + '?key=' + KEY + '&w=' + query)


def read_xml(xml):
    tree = ET.parse(xml)
    return tree.getroot()


result = []
ban_tag = ['pron', 'pos', 'key', 'ps']
trans_dict = {
    'fy': '<b>中文</b>',
    'orig': '<b>短句</b>',
    'trans': '<b>翻译</b>',
    'acceptation': '(解释)',
}


def show(root):
    for node in root.getchildren():
        if node.text and node.tag not in ban_tag:
            result.append("%s:%s" % (trans_dict.get(node.tag, node.tag), node.text))
        show(node)
    return result


def results(fields, original_query):
    message = fields['~message']

    root = read_xml(get_response(message))
    result = show(root)
    body = '<br/>'.join(result)
    html = "<h1>{0}</h1><body>{1}".format(message, body)
    return {
        "title": "dict '{0}'".format(message),
        "run_args": [message],  # ignore for now,
        "html": html
    }


def main():
    message = '美味的'
    root = read_xml(get_response(message))
    result = show(root)
    body = '<br/>'.join(result)
    html = "<h1>{0}</h1><body>{1}".format(message, body)
    print html


if __name__ == '__main__':
    main()
