
import pika
import json

class NotificationProducer:
    def __init__(self):
        # Initialize RabbitMQ connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        
        # Declare queue
        self.channel.queue_declare(queue='notification_queue', durable=True)

    def send_notification(self, notification_data):
        """
        Send notification to RabbitMQ queue
        
        Args:
            notification_data (dict): Dictionary containing notification details
        """
        try:
            # Convert notification data to JSON
            message = json.dumps(notification_data)
            
            # Send message to queue
            self.channel.basic_publish(
                exchange='',
                routing_key='notification_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            print(f"Sent notification to queue: {message}")
            return True
            
        except Exception as e:
            print(f"Error sending to queue: {str(e)}")
            return False

    def close(self):
        """Close the connection"""
        if self.connection:
            self.connection.close()