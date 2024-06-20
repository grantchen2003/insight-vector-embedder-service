import os, time, numpy

from gensim.models import KeyedVectors


class Word2VecEmbedder:
    _model = None
    _vocabulary = None

    @classmethod
    def load_model(cls) -> None:
        print("loading model")

        start_time = time.process_time()

        cls._model = KeyedVectors.load_word2vec_format(
            os.environ["MODEL_PATH"], binary=True, limit=None
        )

        cls._vocabulary = set(cls._model.key_to_index.keys())

        end_time = time.process_time()

        print(f"loaded model in {round(end_time - start_time, 1)} seconds")

    @classmethod
    def vector_embed_sentence(cls, sentence: str) -> list[int]:
        return [3.3, 4.4, 5.5]
