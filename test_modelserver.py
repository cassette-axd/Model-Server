import grpc
import modelserver_pb2
import modelserver_pb2_grpc

from modelserver_pb2 import (
    PredictRequest,  # type: ignore
    PredictResponse,  # type: ignore
    SetCoefsRequest,  # type: ignore
    SetCoefsResponse,  # type: ignore
)

port = "5440"
addr = f"127.0.0.1:{port}"
channel = grpc.insecure_channel(addr)
stub = modelserver_pb2_grpc.ModelServerStub(channel)

stub.SetCoefs(SetCoefsRequest(coefs=[1, 2, 3]))
stub.Predict(PredictRequest(X=[1, 2, 3]))

# Fill the cache
for i in range(10):
    response = stub.Predict(PredictRequest(X=[3, 2, i]))
    print(response)
    output = 1 * 3 + 2 * 2 + 3 * i
    print(str(response) == f"y: {output}\n", response)
    assert str(response) == f"y: {output}\n", response

# Check first call is no longer cached
response = stub.Predict(PredictRequest(X=[1, 2, 3]))
print(str(response) == "y: 14\n", response)
assert str(response) == "y: 14\n", response

stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs=[1, 2, 3]))
resp = stub.Predict(modelserver_pb2.PredictRequest(X=[1, 2, 3]))
print(f"y={resp.y}, hit={resp.hit}")  # should be 14, false
resp = stub.Predict(modelserver_pb2.PredictRequest(X=[1, 2, 3]))
print(f"y={resp.y}, hit={resp.hit}")  # should be 14, true
resp = stub.Predict(modelserver_pb2.PredictRequest(X=[1.00004, 2.00001, 2.99996]))
print(f"y={resp.y}, hit={resp.hit}")  # should be 14, true
resp = stub.Predict(modelserver_pb2.PredictRequest(X=[2, 3, 4]))
print(f"y={resp.y}, hit={resp.hit}")  # should be 20, false
