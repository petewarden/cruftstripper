#!/usr/bin/env python

import sys, string, re
from html2txt import html2txt

common_short_words = {
    'a': True,
    'i': True,
    'ah': True,
    'an': True,
    'as': True,
    'at': True,
    'ax': True,
    'be': True,
    'by': True,
    'do': True,
    'ex': True,
    'go': True,
    'ha': True,
    'he': True,
    'hi': True,
    'id': True,
    'if': True,
    'in': True,
    'is': True,
    'it': True,
    'ma': True,
    'me': True,
    'my': True,
    'no': True,
    'of': True,
    'oh': True,
    'on': True,
    'or': True,
    'ox': True,
    'pa': True,
    'so': True,
    'to': True,
    'uh': True,
    'um': True,
    'un': True,
    'up': True,
    'us': True,
    'we': True
}

default_settings = {
    'words_threshold': 0.75, 
    'sentences_threshold': 0.5,
    'min_words_in_sentence': 4,
    'min_sentences_in_paragraph': 2
}

def debug_log(message):
#    print message
    return

def strip_nonsentences(input, input_settings = { }):

    settings = {}
    for key, value in default_settings.items():
        if key in input_settings:
            settings[key] = input_settings[key]
        else:
            settings[key] = default_settings[key]

    result_lines = []

    lines = input.split("\n")
    for line in lines:
        sentences = re.split(r'[.?!][^a-zA-Z0-9]', line)
        
        # Go through all the 'sentences' and see which ones look valid
        sentences_length = 0
        sentences_matches = 0
        sentences_count = 0
        for sentence in sentences:
            
            sentence = sentence.strip()
            
            sentences_length += len(sentence)
            
            # Is this an empty sentence?
            if len(sentence) == 0:
                continue
                            
            # Does this sentence start with a capital letter?
            first_char_match = re.search(r'[a-zA-Z]', sentence)
            if not first_char_match:
                debug_log(sentence+' - no characters found')
                continue
            if not first_char_match.group(0).isupper():
                debug_log(sentence+' - first character isn\'t uppercase - '+first_char_match.group(0))
                continue
          
            # Split sentence by spaces, punctuation  
            words = re.split(r'[ ]', sentence)
            
            # Is this too short to be a sentence?
            if len(words)<settings['min_words_in_sentence']:
                debug_log(sentence+' - too few words in sentence: '+str(len(words))+' - '+str(words))
                continue
            
            # Go through all the entries and see which ones look like real words
            words_length = 0
            words_matches = 0
            for word in words:
                words_length += len(word)
            
                # Not all letters?
                if re.match(r'[^a-zA-Z\-\'"]', word):
                    debug_log(word+' not all letters')
                    continue
                    
                # Is it a short word, that isn't common?
                if len(word)<2 and not word.lower() in common_short_words:
                    debug_log(word+' short, and not common')
                    continue
                    
                words_matches += len(word)
            
            # No words found?
            if words_length == 0:
                debug_log(sentence+' - no words found')
                continue
            
            # Were there enough valid words to mark this as a sentence?
            words_ratio = words_matches/float(words_length)
            if words_ratio > settings['words_threshold']:
                sentences_matches += len(sentence)
                sentences_count += 1
            else:
                debug_log(sentence + ' - words ratio too low: '+str(words_ratio))
        
        result_line = { 'line': line }
        
        # No sentences found?
        if sentences_length == 0:
            result_line['is_sentence'] = False
        else:
            # Were there enough valid sentences to mark this line as content?
            sentences_ratio = sentences_matches/float(sentences_length)
            if sentences_ratio > settings['sentences_threshold']:
                result_line['is_sentence'] = True
                result_line['sentences_count'] = sentences_count
                result_line['ends_with_period'] = re.search(r'\.[^a-zA-Z]*$', line)
            else:
                result_line['is_sentence'] = False
                debug_log(line + ' - sentences ratio too low: '+str(sentences_ratio))
        
        result_lines.append(result_line)

    result = ''
    found_sentences_count = 0
    found_sentences = ''
    for result_line in result_lines:
        
        is_sentence = result_line['is_sentence']
        
        if not is_sentence:
            if found_sentences_count >= settings['min_sentences_in_paragraph']:
                result += found_sentences + "\n"
                debug_log(found_sentences+' - found '+str(found_sentences_count))
            else:
                debug_log(found_sentences+' - not enough sentences in paragraph: '+str(found_sentences_count))
            found_sentences_count = 0
            found_sentences = ''
        else:
            sentences_count = result_line['sentences_count']
            has_enough_sentences = sentences_count >= settings['min_sentences_in_paragraph']
            ends_with_period = result_line['ends_with_period']
            
            if has_enough_sentences or ends_with_period:
                found_sentences += result_line['line'].strip()+' '
                found_sentences_count += sentences_count
            else:
                debug_log(result_line['line']+' - skipping, not enough sentences: '+str(sentences_count))

    if found_sentences_count >= settings['min_sentences_in_paragraph']:
        result += found_sentences + "\n"

    return result

if __name__ == '__main__':
    input = sys.stdin.read()

    output = strip_nonsentences(input)

    print unicode(output, errors='ignore').encode("utf-8")