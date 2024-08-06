#!/bin/bash

cd ..

export ENV=dev

nodemon --exec ".venv/Scripts/python -u -m vector_embedder_service.main" --ext py