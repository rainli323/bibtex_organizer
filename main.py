#!/usr/bin/python3

import sys
import os
import re

class Reference:
    """An entry of reference, entire message, author, year, page"""
    
    all_ref_ = ""
    author_ = ""
    year_ = ""
    page_ = ""
    error_ = ""
    key_  = ""

    def __init__ (self, filename, linenumber):
        self.from_file_ = filename
        self.from_line_ = linenumber

    def has_complete_data():
        if not author_:
            error_.append("No auther found! ")
        if not year_:
            error_.append("No year found! ")
        if not page_:
            error_.append("No page found! ")
        if error_:
            return False
        else:
            return True


    def record(line):
        all_ref_ = all_ref_ + line

    def record_new_ref(line):
        message = re.sub('.+:.+:.+', '', line, re.IGNORECASE)
        all_ref_ = message

    def set_author(line):
        message = re.sub('author *= *', '', line, re.IGNORECASE)
        message = re.sub('\"', '', line, re.IGNORECASE)
        message = re.sub('\"', '', line, re.IGNORECASE)
        message = re.sub('{', '', line, re.IGNORECASE)
        message = re.sub('}', '', line, re.IGNORECASE)
        message = re.sub(',.*', '', line, re.IGNORECASE)
        message = re.sub('and.*', '', line, re.IGNORECASE)
        author_ = message

    def set_year(line):
        message = re.search('[0-9]\4', line)
        year_ = message.group()

    def set_page(line):
        message = re.search('[0-9]\4', line)
        year_ = message.group()

    def set_key(line):
        key_ = line

    def is_author(line):
        if re.search('author *=', line, re.IGNORECASE):
            return True
        else:
            return False

    def is_year(line):
        if (re.search('year *=', line, re.IGNORECASE)):
            return True
        else:
            return False

    def is_page(line):
        if (re.search('(?!num)pages *=', line, re.IGNORECASE)):
            return True
        else:
            return False

class InputLine:
    """A line from the input file"""
    
    data = ""
    n_brackets = 0

    def __init__ (self, string, read):
        self.data = string
        self.n_brackets = read.n_brackets

    def is_new_ref ():
        global n_brackets
        if (re.search('@article', self.data, re.IGNORECASE) and self.n_brackets == 0):
            return True
        else:
            return False
    
    def is_ref ():
        if (self.n_brackets > 0):
            return True
        else:
            return False
    
    def is_end_of_ref ():
        if (self.n_brakets == 0):
            return True
        else:
            return False
    
    def is_garbage ():
        if ( not re.search('@article', self.data, re.IGNORECASE) and self.n_brackets == 0):
            return True
        else:
            return False


class Read:
    """record data from all input files"""
    
    n_brackets = 0
    
#    def read_from_all_files():
#        for file_name in sys.argv[1:]:
#            read = ReadOneFile()
#            if not read.read_from_file(file_name):
#                print("File {} does not exist. Exiting..".format(file_name))
#                sys.exit()
#

    def read_from_file(file_name):
        global ref_list 
        global incomplete_ref_list 
        global dictionary 
        if not os.path.isfile(file_name):
            print("File {} does not exist. Exiting..".format(file_name))
            sys.exit()
    
        line_number = 0;
        self.n_brackets = 0;
        with open(file_name, 'r') as infile:
            for readline in infile():
                line = InputLine(readline, self)
                line_number += 1
                if line.is_new_ref():
                    print("here")
                    current_ref = Reference(file_name, line_number)
                    current_ref.record_new_ref(line)
                    count_bracket(line.data)
                elif line.is_ref():
                    if line.is_author():
                        current_ref.set_author(line.data)
                    if line.is_page():
                        current_ref.set_page(line.data)
                    if line.is_year():
                        current_ref.set_year(line.data)
                    current_ref.record(line.data)
                    count_bracket(line.data)
                    if is_end_of_ref():
                        if current_ref.has_complete_data():
                            key = current_ref.author_ + ":" + current_ref.year_ + ":" + current_ref.page_
                            value = current_ref.all_ref_
                            current_ref.set_key(key)
                            if (key not in dictionary):
                                dictionary[key] = value
                                ref_list.append(current_ref)
                        else:
                            incomplete_ref_list.append(current_ref)
                elif line.is_garbage():
                    count_bracket(line.data)
                else:
                    try:
                        raise SyntaxError('Something wrong with the format')
                    except SyntaxError:
                        print("something wrong! At file {file_name} at line {line_number}")
                        raise

        if (self.n_brackets != 0):
            try:
                raise SyntaxError('Something wrong with the format')
            except SyntaxError:
                print("something wrong! At file {file_name} at line {line_number}")
                raise
         
    def count_bracket(line):
        nbra = re.findall('{', line)
        nket = re.findall('}', line)
        self.n_bracket = self.n_bracket + len(nbra) - len(nket)

def read_from_file(file_name):
    global ref_list 
    global incomplete_ref_list 
    global dictionary 
    if not os.path.isfile(file_name):
        print("File {} does not exist. Exiting..".format(file_name))
        sys.exit()

    line_number = 0;
    self.n_brackets = 0;
    with open(file_name, 'r') as infile:
        for readline in infile():
            line = InputLine(readline, self)
            line_number += 1
            if line.is_new_ref():
                print("here")
                current_ref = Reference(file_name, line_number)
                current_ref.record_new_ref(line)
                count_bracket(line.data)
            elif line.is_ref():
                if line.is_author():
                    current_ref.set_author(line.data)
                if line.is_page():
                    current_ref.set_page(line.data)
                if line.is_year():
                    current_ref.set_year(line.data)
                current_ref.record(line.data)
                count_bracket(line.data)
                if is_end_of_ref():
                    if current_ref.has_complete_data():
                        key = current_ref.author_ + ":" + current_ref.year_ + ":" + current_ref.page_
                        value = current_ref.all_ref_
                        current_ref.set_key(key)
                        if (key not in dictionary):
                            dictionary[key] = value
                            ref_list.append(current_ref)
                    else:
                        incomplete_ref_list.append(current_ref)
            elif line.is_garbage():
                count_bracket(line.data)
            else:
                try:
                    raise SyntaxError('Something wrong with the format')
                except SyntaxError:
                    print("something wrong! At file {file_name} at line {line_number}")
                    raise

    if (self.n_brackets != 0):
        try:
            raise SyntaxError('Something wrong with the format')
        except SyntaxError:
            print("something wrong! At file {file_name} at line {line_number}")
            raise


def main():
    ref_list = []
    incomplete_ref_list = []
    dictionary = {}

    file_name = sys.argv[1]
    print(file_name)
    read_from_file(file_name)


#    for file_name in sys.argv[1:]:
#        read = Read();
#        print(file_name)
#        read.read_from_file(file_name)
        #    try:
        #        raise SyntaxError('Something wrong with the format')
        #    except SyntaxError:
        #        print("Reading file '{file_name}' wrong. Exiting...")
        #        raise
        #        sys.exit()
    
    
    #read.read_from_all_files()
    
    #print(ref_list[0].all_ref_)
    #sort_references()
    #print_references()
    #print_incomplete_reference()

if __name__ == '__main__':
  main()
