# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


class xmlCodeRunner():

  # ============================== hack for CDATA

    def serialize_xml_with_CDATA(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
        if elem.tag == 'CDATA':
            write("<![CDATA[{}]]>".format(elem.text))
            return
        return ET._original_serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs)

    ET._original_serialize_xml = ET._serialize_xml
    ET._serialize_xml = ET._serialize['xml'] = serialize_xml_with_CDATA
    
    def addExtraElementWithText(self, node, name, text, attrib = {}):
        temp = ET.SubElement(node, name, attrib)
        elText = ET.SubElement(temp, 'text')
        elText.text = text
        return node

    def addExtraElement(self, node, name, text, attrib = {}):
        temp = ET.SubElement(node, name, attrib)
        temp.text = text
        return node

    def CDATA(self, text):
        element =  ET.Element("CDATA")
        element.text = text
        return element
 
    def __init__(self, qqList, outfile):

        # ============================== XML GENERATOR

        # set the question category
        root = ET.Element('quiz')

        for qq in qqList:
            
            questionTypeCategory = ET.SubElement(root, 'question', attrib={"type": "category"})
            category = ET.SubElement(questionTypeCategory, 'category')
            categoryText = ET.SubElement(category, "text")
            categoryText.text = qq["category"]


            # create the coderunner question
            question = ET.SubElement(root, 'question', attrib={"type": "coderunner"})

            # name
            name = ET.SubElement(question, 'name')
            text = ET.SubElement(name, 'text')
            text.text = qq["name"]
        
            # question text
            questionText = ET.SubElement(question, 'questiontext', attrib={"format": "markdown"})
            text = ET.SubElement(questionText, 'text')
            text.append( self.CDATA("{}".format(qq["description"]) ) )
        
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
            template = ET.SubElement(question, 'template')
            template.append( self.CDATA("{}".format(qq["template"])) )
            
            # answer
            answer = ET.SubElement(question, 'answer')
            answer.append( self.CDATA("{}".format(qq["answer"])) )
                
            # answer preload
            answerpreload = ET.SubElement(question, 'answerpreload')
            answerpreload.append( self.CDATA("{}".format(qq["answerpreload"])) )

            # build testcases
            testcases = ET.SubElement(question, 'testcases')

            for iTest in range(0, len(qq["testcases"]) ):
                testcase = ET.SubElement(testcases, 'testcase',
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
        tree = ET.ElementTree(root)
        myfile = open(outfile, "wb")
        tree.write(myfile, encoding="utf-8", xml_declaration=True)

