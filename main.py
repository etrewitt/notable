"""
Erik Trewitt, submission for Notable coding assessment.
"""

"""
Example text:

Patient presents today with several issues. Number one BMI has increased by 10% since their last visit. Number next patient reports experiencing dizziness several times in the last two weeks. Number next patient has a persistent cough that hasn’t improved for last 4 weeks.
"""

import re


def capitalize(sentence: str) -> str:
    sentence = sentence.strip(' ')
    return sentence.capitalize()


def transform_numbered_list(text: str) -> str:
    allowed_phrases = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
    }
    output_str = ''

    split_text = re.split(r'(number)\s', text, flags=re.I)  # match 'Number' or 'number'
    ongoing_list = False
    current_num = 0
    # This is a bit of a hack-y solution to the issue that 'number' not followed by a legal phrase otherwise
    # requires some guesswork; this feels sloppy and I would prefer a different implementation of this fix.
    previous_num = ''
    for i, s in enumerate(split_text):
        if s.lower() == 'number':
            previous_num = s
            continue
        s = s.strip(' ')
        if not s:
            # string is empty
            continue
        match = re.match(r'(\w+)\s(.*)', s, flags=re.I)  # match the first word in the sentence
        phrase = match.group(1).lower()
        if match is None:
            # string is likely empty. TODO: need to investigate this further
            continue

        if not ongoing_list and phrase in allowed_phrases:
            current_num = allowed_phrases[phrase]
            output_str += f'\n{current_num}. {capitalize(match.group(2))}'
            ongoing_list = True
        elif ongoing_list and phrase.lower() == 'next':
            # continue a list
            current_num += 1
            output_str += f'\n{current_num}. {capitalize(match.group(2))}'
        elif ongoing_list and phrase in allowed_phrases:
            # This may not be an error! Should be defined in spec, possible it should be folded into the following case
            raise RuntimeError('Starting a new list in an ongoing list')
        else:
            # Just continue on, it's not a new list point.
            if i == 0:
                output_str += s
            else:
                output_str += f' {previous_num} {match.group(0)}'

    return output_str.strip('\n ')


test_cases = [
    (
        'Patient presents today with several issues. Number one BMI has increased by 10% since their last visit. Number next patient reports experiencing dizziness several times in the last two weeks. Number next patient has a persistent cough that hasn’t improved for last 4 weeks.',
        'Patient presents today with several issues.\n1. Bmi has increased by 10% since their last visit.\n2. Patient reports experiencing dizziness several times in the last two weeks.\n3. Patient has a persistent cough that hasn’t improved for last 4 weeks.'
    ),
    (
        'Number one hello',
        '1. Hello'
    ),
    (
        'Here is a list that starts from something besides one. Number four this is the first item. Number next this is the second item.',
        'Here is a list that starts from something besides one.\n4. This is the first item.\n5. This is the second item.'
    ),
    (
        'Here is a sentence without a list but it uses the word number, like this.',
        'Here is a sentence without a list but it uses the word number, like this.'
    ),
    (
        'Here is a sentence with a list and the word number inside its list points. Number three the word number will appear right here. Number next It will not appear in this line. Number next the word number will appear in this line.',
        'Here is a sentence with a list and the word number inside its list points.\n3. The word number will appear right here.\n4. It will not appear in this line.\n5. The word number will appear in this line.'
    )
]


if __name__ == '__main__':
    # Run test cases
    for i, case in enumerate(test_cases):
        if case[1] == transform_numbered_list(case[0]):
            print(f'Output matches for test case {i}!')
            print(f'Input text:\n{case[0]}')
            print(f'Output text:\n{case[1]}')
        else:
            print(f'Mismatch for test case {i}')
