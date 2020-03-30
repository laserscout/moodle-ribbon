# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

def CDATA(text=None):
    element = etree.Element('![CDATA[')
    element.text = text
    return element


class xmlCloze():

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
            question = etree.SubElement(root, 'question', attrib={"type": "cloze"})

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
            question = self.addExtraElement(question, 'penalty', "0.00")
            question = self.addExtraElement(question, 'hidden', "0")
                    

        # create a new XML file with the results
        tree = etree.ElementTree(root)
        myfile = open(outfile, "wb")
        tree.write(myfile, encoding="utf-8", xml_declaration=True)
