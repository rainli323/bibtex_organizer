#!/usr/bin/python3

import sys
import os
import re

class Reference:
    """An entry of reference, entire message, author, year, page"""
    

    def __init__ (self, filename, linenumber):
        self.from_file_ = filename
        self.from_line_ = linenumber
        self.all_ref_ = ""
        self.author_ = ""
        self.year_ = ""
        self.page_ = ""
        self.error_ = ""
        self.key_  = ""

    def has_complete_data(self):
        if not self.author_:
            self.error_ = self.error_ + "No auther found! "
        if not self.year_:
            self.error_ = self.error_ + "No year found! "
        if not self.page_:
            self.error_ = self.error_ + "No page found! "
        if self.error_:
            return False
        else:
            return True


    def record(self, line):
        self.all_ref_ = self.all_ref_ + line

    def record_new_ref(self, line):
        message = re.sub('{.+,', '{LABEL_TBD,', line, re.IGNORECASE)
        self.all_ref_ = message

    def set_author(self, line):
        message = re.sub('author *= *', '', line, re.IGNORECASE)
        message = re.sub('\"', '', message, re.IGNORECASE)
        message = re.sub('\"', '', message, re.IGNORECASE)
        message = re.sub('{', '', message, re.IGNORECASE)
        message = re.sub('}', '', message, re.IGNORECASE)
        message = re.sub(',.*', '', message, re.IGNORECASE)
        message = re.sub('and.*', '', message, re.IGNORECASE)
        message = message.rstrip()
        message = message.lstrip()
        if message:
            print(message)
            message = re.findall(r"\S+", message)[-1]
            self.author_ = message
        print(self.author_)

    def set_year(self, line):
        message = re.search(r"[0-9]+", line)
        if message:
            self.year_ = message.group()
        print(self.year_)

    def set_page(self, line):
        message = re.search(r"[0-9]+", line)
        if message:
            self.page_ = message.group()
        print(self.page_)

    def set_key(self, line):
        self.key_ = line
        self.all_ref_ = re.sub('LABEL_TBD', line, self.all_ref_, re.IGNORECASE)
        print(self.key_)

class InputLine:
    """A line from the input file"""
    
    data = ""
    n_brackets = 0

    def __init__ (self, string, read):
        self.data = string
        self.n_brackets = read.n_brackets

    def is_new_ref (self):
        global n_brackets
        if (re.search('@', self.data, re.IGNORECASE) and self.n_brackets == 0):
            return True
        else:
            return False
    
    def is_ref (self):
        if (self.n_brackets > 0):
            return True
        else:
            return False
    
    def is_end_of_ref (self):
        nbra = re.findall('{', self.data)
        nket = re.findall('}', self.data)
        current_n_brackets = self.n_brackets + len(nbra) - len(nket)
        if (current_n_brackets == 0):
            return True
        else:
            return False
    
    def is_garbage (self):
        if (self.n_brackets == 0):
            return True
        else:
            return False

    def is_author(self):
        if re.search('author *=', self.data, re.IGNORECASE):
            print("author")
            return True
        else:
            return False

    def is_year(self):
        if (re.search('year *=', self.data, re.IGNORECASE)):
            print("year")
            return True
        else:
            return False

    def is_page(self):
        if (re.search('(?<!num)pages *=', self.data, re.IGNORECASE)):
            print("page")
            return True
        else:
            return False


class Read:
    """record data from all input files"""
    
    def __init__ (self, *args):
        self.n_brackets = 0
        self.file_list = args


    def read_from_all_files(self):
        for file_name in self.file_list[1:]:
            if not self.read_from_file(file_name):
                print("File {} does not exist. Exiting..".format(file_name))
                sys.exit()


    def read_from_file(self, file_name):
        global ref_list 
        global incomplete_ref_list
        global dictionary
        
        print(ref_list)
        
        if not os.path.isfile(file_name):
            print("File {} does not exist. Exiting..".format(file_name))
            sys.exit()
    
        line_number = 0;
        self.n_brackets = 0;
        with open(file_name, 'r') as infile:
            readline = infile.readline()
            while readline:
                line = InputLine(readline, self)
                line_number += 1
                if line.is_new_ref():
                    print(line.data)
                    current_ref = Reference(file_name, line_number)
                    current_ref.record_new_ref(line.data)
                    self.count_brackets(line.data)
                elif line.is_ref():
                    if line.is_author():
                        current_ref.set_author(line.data)
                    if line.is_page():
                        current_ref.set_page(line.data)
                    if line.is_year():
                        current_ref.set_year(line.data)
                    current_ref.record(line.data)
                    self.count_brackets(line.data)
                    print(line.data)
                    print(self.n_brackets)
                    if line.is_end_of_ref():
                        print("end of ref")
                        if current_ref.has_complete_data():
                            key = current_ref.author_ + ":" + current_ref.year_ + ":" + current_ref.page_
                            value = current_ref
                            current_ref.set_key(key)
                            if (key not in dictionary):
                                dictionary[key] = value
                                ref_list.append(current_ref)
                        else:
                            incomplete_ref_list.append(current_ref)
                elif line.is_garbage():
                    self.count_brackets(line.data)
                else:
                    try:
                        raise SyntaxError('Something wrong with the format, eg. brackets are not closed')
                    except SyntaxError:
                        print("something wrong! At file {} at line {}.".format(file_name, line_number))
                        raise
                readline = infile.readline()

        if (self.n_brackets != 0):
            try:
                raise SyntaxError('Something wrong with the format, eg. brackets are not closed')
            except SyntaxError:
                print("something wrong! At file {} at line {}.".format(file_name, line_number))
                raise

        return True
         
    def count_brackets(self, line):
        nbra = re.findall('{', line)
        nket = re.findall('}', line)
        self.n_brackets = self.n_brackets + len(nbra) - len(nket)



#def main():
ref_list = []
incomplete_ref_list = []
dictionary = {}

read = Read(*sys.argv)
read.read_from_all_files()

for i in sorted (dictionary) : 
    print ((i, dictionary[i].all_ref_), end =" ") 
    
    #print(ref_list[0].all_ref_)
    #sort_references()
    #print_references()
    #print_incomplete_reference()

#if __name__ == '__main__':
#  main()
