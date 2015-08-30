# -*- coding: utf-8 -*-
import htmlentitydefs
import re

# inputstring = u"Lorem & Ipsum est un générateur de faux textes aléatoires. Vous choisissez le nombre de paragraphes, de mots ou de listes. Vous obtenez alors un texte aléatoire que vous"
# # inputstring = u"Lorem & Ipsum"

# def convertentities(unicode_string):

#     def iterate(striter, startindex=0):
#         for i in xrange(startindex, len(striter)):
#             currentchar = striter[i]
#             code = ord(currentchar)
#             if code != 38:
#                 # print currentchar
#                 if code in htmlentitydefs.codepoint2name:
#                     striter = striter.replace(currentchar, '&'+htmlentitydefs.codepoint2name[code]+';')
#                     striter = iterate(striter, i)
#                     break

#         return striter

#     strip_amps = unicode_string.replace(u'&', u'&amp;')

#     convertedstring = iterate(strip_amps)
#     # convertedstring = strip_amps
#     return convertedstring


# outputstring = convertentities(inputstring)

# print outputstring

outputstring = "Lorem &amp; Ipsum est un g&eacute;n&eacute;rateur de faux textes al&eacute;atoires. Vous choisissez le nombre de paragraphes, de mots ou de listes. Vous obtenez alors un texte al&eacute;atoire que vous"


def decode(encoded_string):

    entity_pattern = r'&[^\s&;]*;'

    def conversion_iterator(matchobj):
        print 'conversion_iterator entered'
        entity_name = matchobj.group(0)[1:len(matchobj.group(0))-1]
        if entity_name in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity_name])
        else:
            return matchobj

    decoded_string = re.sub(entity_pattern, conversion_iterator, encoded_string)

    return decoded_string


test = decode(outputstring)

print test
