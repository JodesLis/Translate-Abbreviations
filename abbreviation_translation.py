"""
Takes in a list of codes with description (in csv format).
Uses a key (in same directory as this file) to attempt to
make it more readable and not abbreviated. Will try to deal
with odd things such as assortments, 'w/', and '/' and '&' .
Can also be told to build an errors file so key can be updated.
    -Jody :)
"""

import csv
import re


def build_dict():
    """
    reads in csv of form:
    abbrev,unabbreviated form
    """
    with open("key.csv", "r") as f:
        dummy_header = f.readline()
        raw_abbrev = list(csv.reader(f))
    abbrev_dict = {}
    for line in raw_abbrev:
        abbrev_dict[line[0]] = line[1]
    return abbrev_dict


def not_in_dictionary(entry, abbrev, errors=[]):
    """
    for words not in dictionary, tries to find them
    by finding annoying patterns with splits/&
    """
    translated = ""
    if len(entry) == 0:
        return ""
    else:   # something needs to be done about all these
            # elif as this is super messy...
        if re.match(r"([A-Z]+[\/]*[A-Z]+x[\d]+)", entry):
            x_split = entry.split("x")
            if x_split[0] in abbrev:
                translated = " " + abbrev[x_split[0]] + " (" + x_split[1] + ")"
            else:
                translated = " " + x_split[0].lower() + " (" + x_split[1] + ")"
        elif "ASS" in entry:
            assortment = entry[:-3]
            try:
                assortment = int(assortment)
                translated = "  *" + str(assortment) + " assorted*"
            except:
                translated = entry.lower()
        elif "w/" in entry:
            if entry[:2] in abbrev:
                translated = " with" + abbrev[entry[2:]]
            else:
                translated = " with " + entry[2:].lower()
        elif "&" in entry:
            amper_split = entry.split("&")
            amper_string = ""
            for split_entry in amper_split:
                if split_entry in abbrev:
                    amper_string += " " + abbrev[split_entry] + " and"
                else:
                    amper_string += " " + split_entry.lower() + " and"
            translated += amper_string[:-4]
        elif "/" in entry:
            slash_split = entry.split("/")
            for word in slash_split:
                if word in abbrev:
                    translated += " " + abbrev[word]
                else:
                    translated += " " + word.lower()
        else:
            translated = " " + entry.lower()
            errors.append(entry)
    build_errors(errors)
    return translated


def build_csv(filename):
    """
    uses csv of form:
    itemid,itemname
    and tries to translate
    """
    abbrev = build_dict()
    with open(filename, "r") as f:
        codes = list(csv.reader(f))
    translated_info = []
    # add a check for duplicates
    for line in codes:
        translated = ""
        #temp_line = re.findall(r"[\w]+", line[1]) # nicer but still need '/'
                                                   # left in for now....
        temp_line = line[1].split(" ")
        for entry in temp_line:
            if entry in abbrev:
                translated += " " + abbrev[entry]
            else:
                translated += not_in_dictionary(entry, abbrev)
        translated = translated[1:]
        translated_info.append([line[0], translated])
    with open(filename, "wb") as f_out:
        writer_obj = csv.writer(f_out, delimiter=",")
        writer_obj.writerows(translated_info)


def build_errors(errors):
    """
    output failed translations, for debugging/adding to key
    """
    with open("errors.csv", "wb") as f_out:
        for line in errors:
            f_out.write(line + "\n")


def main():
    filename = raw_input("Enter the csv filename: ")
    build_csv(filename)

if __name__ == "__main__":
    main()
