import json
import os
from collections import OrderedDict
import csv


serial = 0


def generate_translation_docs(source_file):

    def transliterator(src, trans):  # source_obj, translation_obj

        global serial
        print "\n\n\n"
        print "# # # # #"
        print ""
        print "src:"
        print src
        print ""

        if isinstance(src, dict):
            print ""
            print "src is dict"
            print ""
            for key in src:
                print "\n\n~~~~iterant~~~~"
                print "key:"
                print key
                print ""
                if isinstance(key, dict):
                    print "KEY IS DICT - RECURS"
                    transliterator(key, trans)
                elif isinstance(src[key], dict) or isinstance(src[key], list):
                    print "SRC[KEY] IS DICT OR LIST - RECURS"
                    transliterator(src[key], trans)
                else:
                    print "---"
                    print "SRC[KEY] OK FOR TRANSLITERATION"
                    print "---"
                    current_serial = str(serial).zfill(6)
                    trans[current_serial] = src[key]
                    src[key] = current_serial
                    serial += 1
        elif isinstance(src, list):
            print "\nsrc is list\n"
            for x in xrange(0, len(src)):
                print "\n\n~~~~iterant~~~~"
                if isinstance(src[x], dict):
                    print "LIST ITEM AT LOCATION %i IS DICT - RECURS" % x
                    transliterator(src[x], trans)
                else:
                    print "---"
                    print "LIST ITEM AT LOCATION %i OK FOR TRANSLITERATION" % x
                    print "---"
                    current_serial = str(serial).zfill(6)
                    trans[current_serial] = src[x]
                    src[x] = current_serial
                    serial += 1

    file_basename = os.path.splitext(os.path.basename(source_file))[0]
    filename = file_basename+"-root.json"
    rosetta = file_basename+"-rosetta.json"
    translation = file_basename+"-translation-file.json"

    with open(source_file, 'r') as original_file, open(filename, 'w') as root_file, open(rosetta, 'w') as rosetta_file, open(translation, 'w') as translation_file:

        raw_contents = original_file.read()

        # Copy the contents of the source_file into root
        root_file.write(raw_contents)

        main_contents = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(raw_contents)

        # print main_contents

        translation_contents = OrderedDict({})

        transliterator(main_contents, translation_contents)

        rosetta_file.write(json.dumps(main_contents))
        translation_file.write(json.dumps(translation_contents))


def merge_translation(translation_doc, rosetta_doc, language):

    def converge_entry(src, trans):
        if isinstance(src, dict):
            for key in src:
                if isinstance(key, dict):
                    converge_entry(key, trans)
                elif isinstance(src[key], dict) or isinstance(src[key], list):
                    converge_entry(src[key], trans)
                else:
                    src[key] = trans[src[key]]
        if isinstance(src, list):
            for x in xrange(0, len(src)):
                if isinstance(src[x], dict):
                    converge_entry(src[x], trans)
                else:
                    src[x] = trans[src[x]]

    # gets rosetta basename then strips off the "-rosetta.json" to get true basename
    file_basename = os.path.splitext(os.path.basename(rosetta_doc))[0]
    file_basename = file_basename[0:len(file_basename)-len("-rosetta")]
    translated_json_doc = file_basename+"-"+language+".json"

    with open(translation_doc, 'r') as translations, open(rosetta_doc, 'r') as rosetta, open(translated_json_doc, 'w') as merge_doc:

        translated_content = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(translations.read())

        rosetta_stone = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(rosetta.read())

        converge_entry(rosetta_stone, translated_content)

        merge_doc.write(json.dumps(rosetta_stone))


def generate_csv(source_file):
    file_basename = os.path.splitext(os.path.basename(source_file))[0]
    csv_filename = file_basename+"-csv.csv"

    with open(source_file, 'r') as translations, open(csv_filename, 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=['id', 'original', 'translation'])

        writer.writeheader()

        translation_content = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(translations.read())

        for key in translation_content:
            writer.writerow({'id': key, 'original': translation_content[key], 'translation': ''})
