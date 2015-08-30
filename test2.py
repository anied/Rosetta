# -*- coding: utf-8 -*-
from html_entity_conversion import encode, decode

inputstring = u"Lorem & Ipsum est un générateur de faux textes aléatoires. Vous choisissez le nombre de paragraphes, de mots ou de listes. Vous obtenez alors un texte aléatoire que vous"

outputstring = encode(inputstring)
print 'encoded:'
print outputstring

outputstring = "Lorem &alex; Ipsum est un g&eacute;n&eacute;rateur de faux textes al&eacute;atoires. Vous choisissez le nombre de paragraphes, de mots ou de listes. Vous obtenez alors un texte al&eacute;atoire que vous"

finalstring = decode(outputstring)
print 'decoded:'
print finalstring
