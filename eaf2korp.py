# Niko Partanen (Language Bank of Finland / IKDP-2 research project)
# See LICENSE and README for further information.

from pathlib import Path
from uralicNLP.cg3 import Cg3
from uralicNLP import uralicApi
from nltk.tokenize import word_tokenize
import pympi
import xml.etree.ElementTree as ET
import re

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
    agreed_tags = set.intersection(*map(set,tags)) # picks the shared tags
    agreed_tags_str = ' '.join(agreed_tags)
    if agreed_tags_str:
        return(agreed_tags_str)
    else:
        return("_")

# This writes some of the annotations into ELAN file immediately,
# now it seems that more reusable approach could be to write first a plain
# VRT file, and then write annotations into that.

def eaf2korp_annotate(elan_file_path, language = "kpv", transcription_tier = "orthT"):
    
    # This needs some check on whether the language models have been downloaded
    
    cg = Cg3(language)

    session_name = Path(elan_file_path).stem

    elan_file = pympi.Elan.Eaf(file_path = elan_file_path)

    transcription_tiers = elan_file.get_tier_ids_for_linguistic_type(transcription_tier)

    root = ET.Element("text")
    
    annotations = []

    pos_tags = ['A', 'Adp', 'Adv', 'CS', 'CC', 'CONJ', 'Det', 'Interj', 'N', 'Num', 'Pcle', 'Po', 'Pr', 'Pron', 'Qnt', 'V', 'CLB']

    for transcription_tier in transcription_tiers:

        annotation_values = elan_file.get_annotation_data_for_tier(transcription_tier)

        for annotation_value in annotation_values:

            text_content = annotation_value[2]
            text_content = re.sub("…", ".", text_content) # It seems word_tokenize doesn't handle "…"
            text_content = re.sub("\[\[unclear\]\]", "", text_content)

            words = word_tokenize(text_content)

            disambiguations = cg.disambiguate(words)

            tokens = []
            lemmas = []            
            tags = []

            for disambiguation in disambiguations:
                tokens.append(disambiguation[0])

            for disambiguation in disambiguations:
                possible_words = disambiguation[1]
                temp_list = []
                for possible_word in possible_words:
                    possible_word.morphology.pop()
                    for analysis in possible_word.morphology:
                        if analysis in pos_tags:
                            temp_list.append(analysis)

                unique_list = list(set(temp_list))

                unique_string = '|'.join(unique_list)
                tags.append('|'.join(unique_list))

            for disambiguation in disambiguations:
                possible_words = disambiguation[1]
                temp_list = []
                for possible_word in possible_words:
                    temp_list.append(possible_word.lemma)
                unique_list = list(set(temp_list))
                lemmas.append('|'.join(unique_list))

            word_ids = range(1, len(lemmas) + 1)

            sentence_text = "\n"

            for word_id, token, lemma, tag in zip(word_ids, tokens, lemmas, tags):
                line_text = str(word_id) + '\t' + token + '\t' + lemma + '\t' + tag + '\n'
                sentence_text += line_text

            ET.SubElement(root, "sentence", name="1").text = sentence_text

        tree = ET.ElementTree(root)
        tree.write(session_name + ".vrt", encoding="UTF-8")

# eaf2korp(elan_file_path = "korp_example.eaf", language = "kpv", transcription_tier = "orthT")