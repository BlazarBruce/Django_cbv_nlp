class Best(object):
    def __init__(self, text, best_match, nlp_score):
        self.text = text
        self.best_match = best_match
        self.nlp_score = nlp_score

class Word(object):
    def __init__(self, string, tag):
        self.string = string  # 分词
        self.tag = tag  # 分词词性
class Segment(object):
    def __init__(self, raw_text, filter_text, rawtext_solution=None):
        self.raw_text = raw_text
        self.filter_text = filter_text
        self.raw_text_solution = rawtext_solution
