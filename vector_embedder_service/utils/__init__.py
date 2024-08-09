from .batchifier import Batchifier
from .source_code_summarizer import get_singleton_instance
from .universal_sentence_encoder import UniversalSentenceEncoder


def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened
