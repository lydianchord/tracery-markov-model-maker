import json
import os
import shutil
import unittest

import tracery_markov_model


class TraceryMarkovModelTests(unittest.TestCase):
    PUNC_SUBS = {v: k for k, v in tracery_markov_model.PUNCTUATION.items()}
    
    def tearDown(self):
        if os.path.exists('test_corpus.txt'):
            os.remove('test_corpus.txt')
        if os.path.exists('output'):
            shutil.rmtree('output')
    
    def write_test_corpus(self, *lines):
        with open('test_corpus.txt', 'w') as f:
            for line in lines:
                f.write(line + '\n')
    
    def get_tracery_model(self, ngram_size=3, all_lowercase=False):
        tracery_markov_model.corpus_to_tracery_json(
            'test_corpus.txt', ngram_size, all_lowercase
        )
        with open(os.path.join('output', 'test_corpus.json')) as f:
            model = json.load(f)
        return model
    
    def test_no_conflicts_with_the_word_origin(self):
        self.write_test_corpus(
            'Origin of this: this is the origin of our problems.',
            'origin of',
        )
        model = self.get_tracery_model(2, True)
        self.assertIn('#WORD_ORIGIN#', model['start_boundary'])
        self.assertNotIn('origin #of#', model['origin'])
        self.assertIn('the #WORD_ORIGIN#', model['the'])
        self.assertIn('origin #of#', model['WORD_ORIGIN'])
    
    def test_no_spaces_before_punctuation(self):
        self.write_test_corpus(
            'They said "some stuff."',
            'They said some stuff?!',
        )
        model = self.get_tracery_model(2)
        self.assertIn('stuff#{}"#'.format(self.PUNC_SUBS['.']), model['stuff'])
        self.assertIn('stuff#{}#'.format(self.PUNC_SUBS['?']), model['stuff'])
    
    def test_punctuation_substitutes_converted_back(self):
        self.write_test_corpus('Title: "Subtitle!"')
        model = self.get_tracery_model(2)
        self.assertIn(': #"Subtitle#', model[self.PUNC_SUBS[':']])
        self.assertIn('!"', model[self.PUNC_SUBS['!'] + '"'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
