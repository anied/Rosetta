import json
import os

serial = 0


def transliteration(src, trans):  # source_obj, translation_obj
    for key in src:
        print "\n"+key+"\n"
        if isinstance(src[key], dict):
            print "RECURSION\n"
            transliteration(src[key], trans)
        else:
            print "WRITE\n"
            global serial
            current_serial = str(serial).zfill(6)
            trans[current_serial] = src[key]
            src[key] = current_serial
            serial += 1


def generate_translation_docs(source_file):
    file_basename = os.path.splitext(os.path.basename(source_file))[0]
    filename = file_basename+"-root.json"
    rosetta = file_basename+"-rosetta.json"
    translation = file_basename+"-translation-file.json"

    with open(source_file, 'r') as original_file, open(filename, 'w') as root_file, open(rosetta, 'w') as rosetta_file, open(translation, 'w') as translation_file:

        raw_contents = original_file.read()

        # Copy the contents of the source_file into root
        root_file.write(raw_contents)

        main_contents = json.loads(raw_contents)
        translation_contents = {}

        transliteration(main_contents, translation_contents)

        rosetta_file.write(json.dumps(main_contents))
        translation_file.write(json.dumps(translation_contents))


generate_translation_docs('example_simple.json')
