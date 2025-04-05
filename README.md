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

### Example
#### Publishing
```
import nano_pubsub
from nano_pubsub import Publisher, JsonEvent 

def app_init():
    # initialize before running application code and supply config file
    nano_pubsub.initialize("events.yaml")
...

def make_decision():
    # async publish event to `items_processed` stream
    Publisher("items_processed").publish_event(JsonEvent({"item_id": 1, "amount": 10}))
```

#### Consumption
```
import nano_pubsub
from nano_pubsub import Consumer, JsonEvent 

def app_init():
    # initialize before running application code and supply config file
    nano_pubsub.initialize("events.yaml")
...

async def main():
    app_init()

    asyncio.create_task(consumer.listen(lambda x: print(f"Event received: {x}")))
    await asyncio.Event().wait()

asyncio.run(main())
```