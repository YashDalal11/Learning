import json,time
from django.apps import AppConfig
from kafka import KafkaProducer,KafkaConsumer
from live_data import data

class KafkaSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kafka_setup'

    def ready(self):
        brokers = ['localhost:9095']

        # INITIALIZE KAFKA PRODUCER
        self.producer = KafkaProducer(bootstrap_servers=brokers,
                                      value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode('utf-8'))
        # self.consumer = KafkaConsumer(
        #     'testing',
        #     bootstrap_servers=brokers,
        #     value_deserializer=lambda value: json.loads(value.decode('utf-8')))
        
        # print(self.consumer.assignment())
        # for msg in self.consumer:
        #     print("msg",msg)
        
        def produce():
            count=0
            while True:
                print("start producing")
                
                for i in range(1,61):
                    count+=1
                    print(count)
                    self.producer.send('produced-material-v1',data[count-1])
                    self.producer.flush()

                print("------------------------------------------------")
                # self.producer.flush()
                time.sleep(2)
        produce()


        

                   


