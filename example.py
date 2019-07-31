from pathlib import Path
from uralicNLP.cg3 import Cg3
from uralicNLP import uralicApi
import xml.etree.cElementTree as ET
import re

input_xml = "some_file.xml"
output_xml = "new_file.xml"

# This function takes from uralicNLP's output those
# lemmas that all analysis agree on. If there is no
# agreement, underline is returned to mark empty spot.

def get_lonely_lemmas(ambiguities):
    lemmas = set([])
    for analysis in ambiguities:
        analysis_components = analysis[0].split("+")
        lemmas.add(analysis_components[0])
    if len(lemmas) == 1:
        return(''.join(sorted(lemmas)))
    else:
        return("_")

# This function returns all those tags that the different
# analysis agree on. There are multiple ways to resolve this question
# but this could be one way to deal with it. Another solution would
# be to add into 

def get_agreed_tags(ambiguities):
    tags = []
    for analysis in ambiguities:
        analysis_components = analysis[0].split("+")
        analysis_components.pop(0) # removes the lemma
        tags.append(analysis_components)
    # print(tags)
    if tags:
        agreed_tags = set.intersection(*map(set,tags)) # picks the shared tags
        agreed_tags_str = ' '.join(agreed_tags)
        if agreed_tags_str:
            return(agreed_tags_str)
        else:
            return("_")
    else:
        return("_")

# Here we read the XML file 

tree = ET.parse(input_xml)
root = tree.getroot()

# Now we loop over each sentence

for sentence in root.findall('p/sentence'):

    annotated_text = "\n"

    for line in sentence.text.splitlines():
        
        if line:
            line_content = line.split("\t")
            # print(line_content) # Uncommenting this is useful in checking where the script goes
            analysis = uralicApi.analyze(line_content[1], "kpv")
            line_text = line_content[0] + "\t" + line_content[1] + "\t" + get_lonely_lemmas(analysis) + "\t" + get_agreed_tags(analysis) + "\n"
            annotated_text += line_text
    sentence.text = annotated_text

# In the end we write the new XML file
    
tree.write(output_xml, encoding="UTF-8")
