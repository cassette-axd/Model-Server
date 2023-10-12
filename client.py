import modelserver_pb2_grpc, modelserver_pb2
import grpc

channel = grpc.insecure_channel("localhost:5440")
stub = modelserver_pb2_grpc.ModelServerStub(channel)

resp = stub.SetCoefs([1.0,2.0,3.0])
