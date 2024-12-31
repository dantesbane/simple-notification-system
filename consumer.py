
import pika
import json
import sendmail
import sendsms
import time

class NotificationConsumer:
    def __init__(self):
        self.connect()

    def connect(self):
        """Establish connection with RabbitMQ"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        
        # Declare queue
        self.channel.queue_declare(queue='notification_queue', durable=True)
        
        # Only get one message at a time
        self.channel.basic_qos(prefetch_count=1)

    def callback(self, ch, method, properties, body):
        """
        Process received notifications
        
        Args:
            ch: Channel
            method: Method
            properties: Properties
            body: Message body
        """
        try:
            # Parse notification data
            notification = json.loads(body)
            
            # Send email
            sendmail.sendmail(
                notification['mail_id'],
                notification['message']
            )
            
            # Send SMS
            sendsms.sendmessage(
                notification['message'],
                notification['mobile_no']
            )
            
            print(f"Processed notification: {notification}")
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing notification: {str(e)}")
            # Negative acknowledgment - message will be requeued
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """Start consuming messages from the queue"""
        try:
            self.channel.basic_consume(
                queue='notification_queue',
                on_message_callback=self.callback
            )
            
            print("Started consuming messages. Waiting for notifications...")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            print("Stopping consumer...")
            self.channel.stop_consuming()
        except Exception as e:
            print(f"Error in consumer: {str(e)}")
        finally:
            if self.connection:
                self.connection.close()

if __name__ == "__main__":
    while True:
        try:
            consumer = NotificationConsumer()
            consumer.start_consuming()
        except Exception as e:
            print(f"Consumer disconnected: {str(e)}")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)