
from hojichar import Compose, document_filters
import json


violence_words = """
死ね
4ね
4ぬ
●す殺す
氏ね
タヒね
893
"""
violence_words = violence_words.split("\n")
violence_words = [x for x in violence_words if len(x) > 0]

cleaner = Compose([
    document_filters.JSONLoader(key="text"),
    document_filters.AcceptJapanese(),
    # document_filters.DiscardRareKuten(),
    document_filters.DocumentLengthFilter(min_doc_len=0, max_doc_len=50000),
    document_filters.DiscardAdultContentJa(),
    document_filters.DiscardAdultContentEn(),
    document_filters.DiscardDiscriminationContentJa(),
    # document_filters.DiscardViolenceContentJa(),
    document_filters.DiscardBBSComments(),
    document_filters.DiscardAds(),
    document_filters.MaskPersonalInformation(),
    # document_filters.ExampleHojiChar(),
    document_filters.JSONDumper(),
])


def hoji_filter(text):
    d = {"text": text}
    parsed = cleaner(json.dumps(d))
    if parsed == "":
        return ""
    text = json.loads(parsed)["text"]
    return text
