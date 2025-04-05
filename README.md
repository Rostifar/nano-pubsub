# NanoPubSub

Nanopubsub is simple pub-sub framework for IPC on a single node. 

### Requirements 
- Support for multiple concurrent publishers to a stream with atomic writes.
- Support for multiple consumers, one per group. 
- Durable across multiple application runs. 
- Simple (< 500 lines).

### Limitations
- Reliant on filesystem operations (i.e. fsync) to ensure durability.
- Atomicity of writes is reliant on the atomicity of filesystem appends.

### Prospective Improvements
- Support for AWS S3 with S3 Express Zone One
- Protobuf schematization
