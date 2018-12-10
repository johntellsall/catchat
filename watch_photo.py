import boto3

s3_resource = boto3.resource("s3")

my_bucket = s3_resource.Bucket(name="johntellsall-beer")

print("Photos:")
for obj in my_bucket.objects.all():
    print("-", obj.key)
# import ipdb ; ipdb.set_trace()

print("Waiting for messages")
sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName="file-created")

client = boto3.client("sqs")
if 1:
    enqueue_response = client.send_message(
        QueueUrl=queue.url,
        MessageBody="yum",
        MessageAttributes={"Author": {"StringValue": "Daniel", "DataType": "String"}},
    )

# Process messages by printing out body and optional author name
try:
	while True:
	    for message in queue.receive_messages(
	    	MessageAttributeNames=["Author"],
	    	WaitTimeSeconds=3):
	        if not message:
	            print("DONE")
	            break
	        print("=>", message.body)
	        if message.message_attributes is not None:
	            author_name = message.message_attributes.get("Author").get("StringValue")
	            if author_name:
	                print(f" name={author_name}")
	        else:
	            print("??", message)
	        message.delete() # Let the queue know that the message is processed
except KeyboardInterrupt:
	pass

# XX: delete all the other messages
# import ipdb ; ipdb.set_trace()
try:
	print('Purging queue')
	queue.purge()
except client.exceptions.PurgeQueueInProgress:
	print('(queue already purging, ignored)')
	pass
# import ipdb

# ipdb.set_trace()
# # # print(message)
