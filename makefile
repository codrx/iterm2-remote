
.PHONY: gen clean

gen: 
   python -m grpc_tools.protoc \
      -I. \
      --python_out=. \
      --grpc_python_out=. \
      server/proto/iterm2_remote.proto

clean:
   rm -f \
      server/proto/iterm2_remote_pb2.py \
      server/proto/iterm2_remote_pb2_grpc.py

