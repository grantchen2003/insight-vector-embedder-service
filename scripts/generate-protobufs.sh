#!/bin/bash

cd ../vector_embedder_service/protobufs

python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. *.proto

cd ..

if [ -d "services" ]; then
    cd services
    for dir in */ ; do
        # Check if the item is a directory
        if [ -d "$dir" ]; then
            echo "Entering directory: $dir"
            cd "$dir" || exit
            if [ ! -d "pb" ]; then
                mkdir pb
            fi
            # Execute the specified command
            python -m grpc_tools.protoc -I . --python_out=./pb/ --grpc_python_out=./pb/ *.proto
            # Return to the parent directory
            cd ..
        fi
    done
    cd ..

fi

# Add "from . " to all lines that match "import *_pb2"
files=$(find . -name '*_pb2_grpc.py')

for file in $files; do
    sed -i -e 's/import \([^ ]*\)_pb2/from . import \1_pb2/' "$file"
done