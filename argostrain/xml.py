from argostrain.dataset import *
from argostrain.utils import *

from collections import deque

from argostranslate import package, translate

MIN_TAG_TEXT_LENGTH = 10
OPEN_TOKEN = '<x>'
CLOSE_TOKEN = '</x>'

def generate_xml_data(dataset, source_code, target_code, num):
    xml_source = deque()
    xml_target = deque()
    source, target = dataset.data()
    installed_languages = translate.get_installed_languages()
    source_translation = list(filter(
            lambda x: x.code == source_code,
            installed_languages))[0]
    target_translation = list(filter(
            lambda x: x.code == target_code,
            installed_languages))[0]
    source_translation = source_translation.get_translation(target_translation)
    for i in range(len(source)):
        if num <= 0:
            break
        source_line = source[i]
        target_line = target[i]
        info(f'Processing xml line {i} ' + \
                'num={num} ' + \
                'source_line={source_line} ' + \
                'target_line={target_line}')
        best_source_start_index = None
        best_source_end_index = None
        best_matching_index = None
        best_target_end_index = None
        best_score = None
        for source_start_index in range(len(source_line) - 1):
            for source_end_index in range(source_start_index, len(source_line) + 1):
                source_sub_string = source_line[source_start_index:source_end_index]
                if len(source_sub_string) < MIN_TAG_TEXT_LENGTH:
                    continue
                translation_hypothesis = source_translation.hypotheses(source_sub_string, 1)[0]
                translated_sub_string = translation_hypothesis.value
                score = translation_hypothesis.score
                matching_index = target_line.find(translated_sub_string)
                if matching_index == -1:
                    continue
                if best_score == None or score > best_score:
                    best_source_start_index = source_start_index
                    best_source_end_index = source_end_index
                    best_matching_index = matching_index
                    best_target_end_index = matching_index + len(translated_sub_string)
                    best_score = score
        if best_score == None:
            continue
        num -= 1
        xml_source.append(
                source_line[:best_source_start_index] + \
                OPEN_TOKEN + \
                source_line[best_source_start_index:best_source_end_index] + \
                CLOSE_TOKEN + \
                source_line[best_source_end_index - 1:])
        xml_target.append(
                target_line[:best_matching_index] + \
                OPEN_TOKEN + \
                target_line[best_matching_index:best_target_end_index] + \
                CLOSE_TOKEN + \
                target_line[best_target_end_index - 1:])

    return Dataset(xml_source, xml_target)

    
