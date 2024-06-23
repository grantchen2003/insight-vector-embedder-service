import torch

from transformers import RobertaTokenizer, RobertaModel


class CodeBert:
    _tokenizer = None
    _model = None

    @classmethod
    def initialize(cls) -> None:
        cls._tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        cls._model = RobertaModel.from_pretrained("microsoft/codebert-base")

    @classmethod
    def vector_embed(cls, text: str) -> list[float]:

        # Tokenize the input source code
        inputs = cls._tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )

        # Get the embeddings
        with torch.no_grad():
            outputs = cls._model(**inputs)

        # The embeddings are in the last hidden state
        embeddings = outputs.last_hidden_state

        # Pool the embeddings (e.g., take the mean of all tokens' embeddings)
        embeddings = embeddings.mean(dim=1).squeeze()

        return embeddings.tolist()
