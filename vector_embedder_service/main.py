import os
    
from vector_embedder_service import config, server, utils


def main() -> None:
    env = os.environ.get("ENV")
    config.load_env_vars(env)
    print(f"ENV={env}")
    
    utils.Word2VecEmbedder.load_model()

    server.start()
    
if __name__ == "__main__":
    main()