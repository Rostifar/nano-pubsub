from datetime import datetime
from nano_pubsub import initialize, Publisher, Consumer
from nano_pubsub.event import JsonEvent

# run init hook in app code
initialize("events.yaml")

# ...

p = Publisher("items_processed")
p.publish_event(JsonEvent({"item_id": 1, "amount": 10}))

# ...
consumer = Consumer("items_processed", "consumer_1")
consumer.listen(
    lambda x: print(f"Processed event {x}.")
)
