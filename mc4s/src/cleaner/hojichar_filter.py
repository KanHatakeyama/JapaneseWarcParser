
from hojichar import Compose, document_filters
import json


base_path = "src/cleaner/hoji_dict/"
cleaner = Compose([
    document_filters.JSONLoader(key="text"),
    document_filters.AcceptJapanese(),
    document_filters.DiscardRareKuten(),
    document_filters.DocumentLengthFilter(min_doc_len=100, max_doc_len=50000),
    document_filters.DiscardAdultContentJa(
        base_path + "adult_keywords_ja.txt"),
    document_filters.DiscardAdultContentEn(
        base_path + "adult_keywords_en.txt"
    ),
    document_filters.DiscardDiscriminationContentJa(
        base_path + "discrimination_keywords_ja.txt"
    ),
    document_filters.DiscardViolenceContentJa(
        base_path + "violence_keywords_ja.txt"
    ),
    document_filters.DiscardBBSComments(),
    document_filters.DiscardAds(
        base_path + "advertisement_keywords_ja.txt"
    ),
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
