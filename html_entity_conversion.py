# -*- coding: utf-8 -*-
import htmlentitydefs
import re


def encode(unicode_string):

    def iterate(striter, startindex=0):
        for i in xrange(startindex, len(striter)):
            currentchar = striter[i]
            code = ord(currentchar)
            if code != 38:
                # print currentchar
                if code in htmlentitydefs.codepoint2name:
                    striter = striter.replace(currentchar, '&'+htmlentitydefs.codepoint2name[code]+';')
                    striter = iterate(striter, i)
                    break

        return striter

    strip_amps = unicode_string.replace(u'&', u'&amp;')

    convertedstring = iterate(strip_amps)

    return convertedstring


def decode(html_encoded_string):

    entity_pattern = r'&[^\s&;]*;'

    def conversion_iterator(matchobj):
        entity_name = matchobj.group(0)[1:len(matchobj.group(0))-1]
        if entity_name in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity_name])
        else:
            #TODO - add warning (output log?)
            return matchobj.group(0)

    decoded_string = re.sub(entity_pattern, conversion_iterator, html_encoded_string)

    return decoded_string
