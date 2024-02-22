import kenlm
import sentencepiece
import unicodedata


class PerplexityChecker:
    def __init__(self, arpa_path, sp_path):
        self.ken_model = kenlm.LanguageModel(arpa_path)
        self.sp = sentencepiece.SentencePieceProcessor()
        self.sp.load(sp_path)

    def __call__(self, inp):
        text = unicodedata.normalize('NFD', inp)
        toks = self.sp.encode(text, out_type=str)
        sentence = " ".join(toks)
        ppl = self.ken_model.perplexity(sentence)
        return ppl


"""
sp_path = "../data/lm_sp/ja.sp.model"
arpa_path = "../data/lm_sp/ja.arpa.bin"
from src.cleaner.perplexity_checker import PerplexityChecker
perp_checker = PerplexityChecker(arpa_path,sp_path)
"""
