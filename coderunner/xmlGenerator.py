# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

def CDATA(text=None):
    element = etree.Element('![CDATA[')
    element.text = text
    return element

class xmlCodeRunner():

    def addExtraElementWithText(self, node, name, text, attrib = {}):
        temp = etree.SubElement(node, name, attrib)
        elText = etree.SubElement(temp, 'text')
        elText.text = text
        return node

    def addExtraElement(self, node, name, text, attrib = {}):
        temp = etree.SubElement(node, name, attrib)
        temp.text = text
        return node

 
    def __init__(self, qqList, outfile):

        # ============================== XML GENERATOR

        # set the question category
        root = etree.Element('quiz')

        for qq in qqList:
            
            questionTypeCategory = etree.SubElement(root, 'question', attrib={"type": "category"})
            category = etree.SubElement(questionTypeCategory, 'category')
            categoryText = etree.SubElement(category, "text")
            categoryText.text = qq["category"]


            # create the coderunner question
            question = etree.SubElement(root, 'question', attrib={"type": "coderunner"})

            # name
            name = etree.SubElement(question, 'name')
            text = etree.SubElement(name, 'text')
            text.text = qq["name"]
        
            # question text
            questionText = etree.SubElement(question, 'questiontext', attrib={"format": "markdown"})
            text = etree.SubElement(questionText, 'text')
            text.append( CDATA("{}".format(qq["description"].replace("\\n\\n","\n\n")) ) )
        
            # [HARD-CODED] multiple options (hard-coded for our needs)
            question = self.addExtraElementWithText(question, 'generalfeedback', '', attrib = {"format": "html"})
            question = self.addExtraElement(question, 'prototypetype', "0")
            question = self.addExtraElement(question, 'allornothing', "1")
            question = self.addExtraElement(question, 'allornothing', "1")
            question = self.addExtraElement(question, "precheck", "0")
            question = self.addExtraElement(question, "showsource", "0")
            question = self.addExtraElement(question, "answerboxlines", "18")
            question = self.addExtraElement(question, "answerboxcolumns", "100")
            question = self.addExtraElement(question, "useace", "")
            question = self.addExtraElement(question, "resultcolumns","")
            question = self.addExtraElement(question, 'defaultgrade', "1.0000000")
            question = self.addExtraElement(question, 'hidden', "0")
            question = self.addExtraElement(question, 'iscombinatortemplate', '0')
            question = self.addExtraElement(question, 'allowmultiplestdins', '')
            question = self.addExtraElement(question, 'validateonsave', '1')
            question = self.addExtraElement(question, 'testsplitterre', '')
            question = self.addExtraElement(question, 'language', '')
            question = self.addExtraElement(question, 'acelang', '')
            question = self.addExtraElement(question, 'sandbox', '')
            question = self.addExtraElement(question, 'grader', 'TemplateGrader')
            question = self.addExtraElement(question, 'gradercputimelimitsecs', '5')
            question = self.addExtraElement(question, 'sandboxparams', '')
            question = self.addExtraElement(question, 'templateparams', '')
            question = self.addExtraElement(question, 'hoisttemplateparams', '1')
            question = self.addExtraElement(question, 'twigall', '0')
            question = self.addExtraElement(question, 'uiplugin', '')
            question = self.addExtraElement(question, 'attachments', '0')
            question = self.addExtraElement(question, 'attachmentsrequired', '0')
            question = self.addExtraElement(question, 'maxfilesize', '10240')
            question = self.addExtraElement(question, 'filenamesregex', '')
            question = self.addExtraElement(question, 'filenamesexplain', '')
            question = self.addExtraElement(question, 'displayfeedback', '1')
        
            # select type and penalty regime
            question = self.addExtraElement(question, 'coderunnertype', qq["qtype"])
            question = self.addExtraElement(question, 'penaltyregime', qq["penalty"])
        
            # question template
            template = etree.SubElement(question, 'template')
            template.append( CDATA("{}".format(qq["template"])) )
            
            # answer
            answer = etree.SubElement(question, 'answer')
            answer.append( CDATA("{}".format(qq["answer"])) )
                
            # answer preload
            answerpreload = etree.SubElement(question, 'answerpreload')
            answerpreload.append( CDATA("{}".format(qq["answerpreload"])) )

            # build testcases
            testcases = etree.SubElement(question, 'testcases')

            for iTest in range(0, len(qq["testcases"]) ):
                testcase = etree.SubElement(testcases, 'testcase',
                                             attrib={'testtype': '0',
                                                         'useasexample': '0',
                                                         'hiderestiffail': '0',
                                                         'mark': '1.0000000', } )
                tt = qq["testcases"][iTest]
                testcase = self.addExtraElementWithText(testcase, 'testcode', tt["testcode"])
  
                # [HARDCODED]
                testcase = self.addExtraElementWithText(testcase, 'stdin', tt["stdin"])
                testcase = self.addExtraElementWithText(testcase, 'expected', tt["expected"])
                testcase = self.addExtraElementWithText(testcase, 'extra', tt["extra"])
                testcase = self.addExtraElementWithText(testcase, 'display', tt["display"])
  
        # create a new XML file with the results
        tree = etree.ElementTree(root)
        myfile = open(outfile, "wb")
        tree.write(myfile, encoding="utf-8", xml_declaration=True)

