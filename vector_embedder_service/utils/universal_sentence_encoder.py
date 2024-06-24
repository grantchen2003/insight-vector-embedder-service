import tensorflow_hub as hub


class UniversalSentenceEncoder:
    _embed = None

    @classmethod
    def initialize(cls):
        model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        cls._embed = hub.load(model_url)

    @classmethod
    def vector_embed_sentence(cls, sentence: str) -> list[float]:
        return cls._embed([sentence]).numpy()[0].tolist()
