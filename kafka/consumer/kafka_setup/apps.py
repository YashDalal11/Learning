import asyncio
import json
import threading
from django.apps import AppConfig
from kafka import KafkaConsumer

class KafkaSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kafka_setup'

    def ready(self):

        brokers =['localhost:9095']


        self.consumer1 = KafkaConsumer(
            'testing1',
            bootstrap_servers=brokers,
            value_deserializer=lambda value: json.loads(value.decode('utf-8')))
        
        self.consumer2 = KafkaConsumer(
            'testing2',
            bootstrap_servers=brokers,
            value_deserializer=lambda value: json.loads(value.decode('utf-8')))
        
        def testing1():
            print("testing1")
            for msg in self.consumer1:
                print("consumer_1",msg.value)

        def testing2():
            for msg in self.consumer2:
                print("consumer_2",msg.value)

        # loop = asyncio.new_event_loop()
        # # asyncio.set_event_loop(loop)
        # loop.create_task(testing1())
        # loop.create_task(testing2())
        # loop.run_forever()

        # testing2()
        # testing1()

        thread_1 = threading.Thread(target=testing1)
        thread_1.daemon = True
        thread_1.start()

        thread_2 = threading.Thread(target=testing2)
        thread_2.daemon = True
        thread_2.start()