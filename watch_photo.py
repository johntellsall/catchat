import boto3
s3_resource = boto3.resource('s3')

my_bucket = s3_resource.Bucket(name='johntellsall-beer')

print('Photos:')
for obj in my_bucket.objects.all():
    print('-', obj.key)
# import ipdb ; ipdb.set_trace()

print("Waiting for messages")
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='file-created')

# Process messages by printing out body and optional author name
for message in queue.receive_messages(): # MessageAttributeNames=['Author']):
	print(message)