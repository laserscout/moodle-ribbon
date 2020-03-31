# -*- coding: utf-8 -*-

import re
from io import StringIO
import csv
import sys
import contextlib
import argparse
from pathlib import Path
import copy
import random
import os

import xml.etree.ElementTree as ET
# ============================== hack for CDATA

def serialize_xml_with_CDATA(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
  if elem.tag == 'CDATA':
    write("<![CDATA[{}]]>".format(elem.text))
    return
  return ET._original_serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs)

ET._original_serialize_xml = ET._serialize_xml
ET._serialize_xml = ET._serialize['xml'] = serialize_xml_with_CDATA


from cloze.xmlGenerator import xmlCloze
from coderunner.xmlGenerator import xmlCodeRunner

# extra imports, useful for generator functions
import subprocess
import datetime
import random
import locale

def dict2csv(dictcsv):
  keys = dictcsv[0].keys()
  f = StringIO()
  dict_writer = csv.DictWriter(f, keys)
  dict_writer.writeheader()
  dict_writer.writerows(dictcsv)
  scsv = f.getvalue()
  print("====")
  print(scsv)
  print("~~~~")


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

    
class Question:

  def coderunner(self, strIn):
    
    ldict = {}
    exec(strIn, globals(), ldict)
    qq = ldict["qq"]

    # put category, name, and description
    qq["name"] = "Q001"
    qq["category"] = "{}/{}".format(self.prefix, self.category)
    qq["description"] = self.questionTemplate
    
    self.crDict = qq
    return True

  def parseCSV(self, strIn):

    if len(strIn) == 0:
      return
    
    if strIn[0] == "@":
      with stdoutIO() as s:
        exec(strIn[1:])
      scsv_search = re.search('====\n((.|\n)*)\n~~~~', s.getvalue(), re.M)
      if scsv_search:
        scsv = scsv_search.group(1)
      else:
        scsv = ""
        
    else:
      scsv = strIn
      
    f = StringIO(scsv)
    reader = csv.DictReader(f, delimiter=',')
    self.variations = dict(enumerate(list(reader)))
    return False

  def parseCloze(self, strIn):

    qq = {}

    # put category, name, and description
    qq["name"] = "Q001"
    qq["category"] = "{}/{}".format(self.prefix, self.category)
    qq["description"] = self.questionTemplate

    self.clozeDict = qq
    
    self.parseCSV(strIn)
    return False
  
  
  availOptions = {
    "csv": parseCSV,
    "cr": coderunner,
    "cloze": parseCloze
  }
  
  def __init__(self, strQuestion, prefix = "", outputdir = "./"):

    self.prefix           = prefix
    self.category         = ""
    self.type             = "markdown"
    self.regexHeader      = "^#\s(.*)"
    self.regexOptions     = "^<!--\s(.*)\n((\n|.)*?)-->"
    self.regexCSV         = "====\n((.|\n)*)\n~~~~"
    self.variations       =  { 0: {} }
    self.questionTemplate = ""
    self.gifts            = []
    self.outputdir        = outputdir
    self.crDict           = {}
    self.parseString(strQuestion)

  def buildCodeRunner(self):
    qq = self.crDict
    
    data_folder = Path(self.outputdir)
    file_name = qq["category"].replace("/", "_") + ".xml"
    file_to_open = data_folder / file_name

    qqList = []
    
    for idx, variation in self.variations.items():
      temp = copy.deepcopy(qq)

      for varName, varValue in variation.items():
        varName = varName.strip()
        varValue = varValue.strip()
        temp["description"] = temp["description"].replace("{{" + varName + "}}", varValue)
        temp["answer"] = temp["answer"].replace("{{" + varName + "}}", varValue)
        temp["template"] = temp["template"].replace("{{" + varName + "}}", varValue)
        temp["answerpreload"] = temp["answerpreload"].replace("{{" + varName + "}}", varValue)

      temp["name"] = "Q{idx:03d}".format(idx = idx + 1)
      qqList.append(temp)
      
    xmlCodeRunner(qqList, file_to_open)

  def buildCloze(self):
    qq = self.clozeDict
    
    data_folder = Path(self.outputdir)
    file_name = qq["category"].replace("/", "_") + ".xml"
    file_to_open = data_folder / file_name

    qqList = []

    for idx, variation in self.variations.items():
      temp = copy.deepcopy(qq)

      for varName, varValue in variation.items():
        varName = varName.strip()
        varValue = varValue.strip()
        temp["description"] = temp["description"].replace("{{" + varName + "}}", varValue)
        
      temp["name"] = "Q{idx:03d}".format(idx = idx + 1)
      qqList.append(temp)
        
    xmlCloze(qqList, file_to_open)
    
  def buildQuestions(self):
    
    for idx, variation in self.variations.items():

      body = self.questionTemplate
      for varName, varValue in variation.items():
        varName = varName.strip()
        varValue = varValue.strip()
        body = body.replace("{{" + varName + "}}", varValue)
        
      gift = """
$CATEGORY: {prefix}/{category}

::Q{idx:03d}::
[{type}]
{body}
""".format(idx      = idx + 1,
           prefix   = self.prefix,
           category = self.category,
           type     = self.type,
           body     = body)
        
      self.gifts.append(gift)
      
  def parseOptions(self, options):
    isCR = False
    isCloze = False
    for option in options:
      if option[0] == "cloze":
        isCloze = True
      if option[0] == "cr":
        isCR = True

      func = self.availOptions.get(option[0])
      if func is not None:
        func( self, option[1] )
      else:
        print( "Unknown option {}, skipping...".format(option[0]))

    return isCR, isCloze
        
  def parseString(self, strQuestion):
    self.category = re.search( self.regexHeader, strQuestion ).group(1)
    options = re.findall( self.regexOptions, strQuestion, flags=re.M )

    strQuestion = re.sub(self.regexHeader, '', strQuestion)
    strQuestion = re.sub(self.regexOptions, '', strQuestion, flags=re.M )

    # double or more blanks correspond to \n
    self.questionTemplate = re.sub( "\n{2,}", "\\\\n\\\\n",
                                      strQuestion.lstrip().rstrip() )
    
    isCR, isCloze = self.parseOptions(options)
    
    if isCR:
      print("Printing CodeRunner")
      self.buildCodeRunner()

    elif isCloze:
      print("Printing Cloze")
      self.buildCloze()
      
    else:
      # if whitespaces at beginning, keep them
      self.questionTemplate = re.sub( r'\n(\s+)', r'\\n\1',
                                      self.questionTemplate )

      self.buildQuestions()

    
def export(questions, filename = None):
    if filename is None:
      for question in questions:
        for m in question.gifts:
          print(m)
    else:
      with open(filename, "w") as gift_file:
        for question in questions:
          gift_file.write("".join(question.gifts))

    
def readQuestionsFromFile(fileName):
  """
  Returns questions from file as a list of string

  """

  reHeaders = "^#[^#]"
  
  # read content from file
  with open(fileName, 'r') as content_file:
    content = content_file.read()

  # split by regex
  indices = [m.start(0) for m in re.finditer(reHeaders, content, flags=re.M)]

  questions = [content[i:j] for i, j in zip(indices, indices[1:] + [None])]

  return questions


def main():

  # parse command line arguments
  parser = argparse.ArgumentParser(
     description="Ribbon: A wrapper over Moodle's GIFT format.")

  # input/output file
  parser.add_argument('input_file', action="store", type=str)
  parser.add_argument('output_file', action="store", type=str)

  # prefix name
  parser.add_argument("-p", "--prefix", action="store",
                      default="autogen",
                      help="prefix in Moodle categories (default 'autogen')")

  # working directory
  parser.add_argument("-d", "--workingdir", action="store",
                      default="./",
                      help="working directory (default './')")

  # working directory
  parser.add_argument("-o", "--outputdir", action="store",
                      default="./",
                      help="output directory (default './')")

  # parse all input arguments
  args = parser.parse_args()

  # change working directory
  os.chdir(args.workingdir)

  # read question templates from file
  questionTemplates = readQuestionsFromFile(args.input_file)

  # generate question objects
  questions = [Question(m, args.prefix, args.outputdir) for m in questionTemplates]

  # export final qustions
  export(questions, args.output_file)
  
  
if __name__ == "__main__":
    main()
