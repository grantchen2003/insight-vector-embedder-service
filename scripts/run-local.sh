#!/bin/bash

cd ..

export ENV=dev

nodemon --exec ".venv/Scripts/python -m vector_embedder_service.main" --ext py