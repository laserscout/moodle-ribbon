# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class xmlCloze():

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
            question = ET.SubElement(root, 'question', attrib={"type": "cloze"})

            # name
            name = ET.SubElement(question, 'name')
            text = ET.SubElement(name, 'text')
            text.text = qq["name"]
        
            # question text
            questionText = ET.SubElement(question, 'questiontext', attrib={"format": "markdown"})
            text = ET.SubElement(questionText, 'text')
            text.append( self.CDATA("{}".format(qq["description"].replace("\\n\\n","\n\n")) ) )
            
            # [HARD-CODED] multiple options (hard-coded for our needs)
            question = self.addExtraElementWithText(question, 'generalfeedback', '', attrib = {"format": "html"})
            question = self.addExtraElement(question, 'penalty', "0.00")
            question = self.addExtraElement(question, 'hidden', "0")
                    
        # create a new XML file with the results
        tree = ET.ElementTree(root)
        myfile = open(outfile, "wb")
        tree.write(myfile, encoding="utf-8", xml_declaration=True)
