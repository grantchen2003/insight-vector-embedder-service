import os
    
from vector_embedder_service import config, database, server, utils


def main() -> None:
    env = os.environ.get("ENV")
    config.load_env_vars(env)
    print(f"ENV={env}")
    
    utils.UniversalSentenceEncoder.initialize()
    utils.SourceCodeSummarizer.initialize()
    
    db = database.get_singleton_instance()
    db.connect()

    server.start()
    
if __name__ == "__main__":
    main()