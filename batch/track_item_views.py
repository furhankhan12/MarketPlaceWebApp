# pulls item viewing messages from Kafka and appends them to a logs
import json, time
from kafka import KafkaConsumer

sleep_time = 2
retries = 5
for x in range(0, retries):  
    try:
        consumer = KafkaConsumer('track-views-topic', group_id='listing-logger', bootstrap_servers=['kafka:9092'])
        while (True):
            for message in consumer:
                f = open("view_log.txt", "a")
                new_click = json.loads((message.value).decode('utf-8'))
                to_write = str(new_click['user_id']) + " " + str(new_click['item_id'])
                print(to_write)
                f.write(str(to_write)+'\n')
                f.close()
        strerror = None

    except:
        strerror = "error"
        pass

    if strerror:
        print("track: sleeping for", sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2 
    else:
        break
    