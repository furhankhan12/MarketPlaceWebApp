# pulls item viewing messages from Kafka and appends them to a logs
import json
from time import sleep
from kafka import KafkaConsumer


sleep_time = 2
retries = 4

for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('track-views-topic', group_id='listing-logger', bootstrap_servers=['kafka:9092'])
        print("consumer", consumer)
        while (True):
            f = open("view_log.txt", "a")
            for message in consumer:
                new_click = json.loads((message.value).decode('utf-8'))
                print("batch new listing", new_click)
                f.write(new_click)

            f.close()
        strerror = None

    except:
        strerror = "error"
        pass

    finally:
        if strerror:
            print("sleeping for", sleep_time)
            sleep(sleep_time)  # wait before trying to fetch the data again
            sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
        else:
            break
    