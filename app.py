from flask import request, jsonify, Flask
import sqlite3
from datetime import datetime
import sendmail
import sendsms
from producer import NotificationProducer
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
#producer object
notification_producer = NotificationProducer()

# Database setup
DATABASE = 'notifications.db'


def init_db():
    """Initialize the database with a notifications table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            mail_id TEXT NOT NULL,
            mobile_no TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database when the application starts
init_db()

def get_db_connection():
    """Create and return a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Get mapping for root endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to the Notification Service API'
    })

# POST endpoint to create a new notification
@app.route('/notifications', methods=['POST'])
def send_notification():
    try:
        data = request.get_json()
        
        # Extract data from request
        user_id = data.get('user_id')
        message = data.get('message')
        mail_id = data.get('mail_id')
        mobile_no = data.get('mobile_no')

        # Validate input
        if not all([user_id, message, mail_id, mobile_no]):
            return jsonify({
                'error': 'All fields (user_id, message, mail_id, mobile_no) are required'
            }), 400

        # Create notification data
        notification_data = {
            'user_id': user_id,
            'message': message,
            'mail_id': mail_id,
            'mobile_no': mobile_no,
            'timestamp': datetime.now().isoformat()
        }

        # Send to queue
        queue_result = notification_producer.send_notification(notification_data)
        
        if not queue_result:
            return jsonify({'error': 'Failed to queue notification'}), 500

        # Insert notification into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (user_id, message, mail_id, mobile_no, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, message, mail_id, mobile_no, datetime.now()))

        conn.commit()
        notification_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'message': 'Notification queued successfully',
            'notification_id': notification_id
        }), 201

    except Exception as e:
        return jsonify({'error': f'Error creating notification: {str(e)}'}), 500



# GET endpoint to retrieve a specific notification by ID
@app.route('/users/<int:user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, user_id, message, mail_id, mobile_no, timestamp
            FROM notifications
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        notifications = cursor.fetchall()  # Using fetchall() instead of fetchone()
        conn.close()

        if not notifications:  # If no notifications found
            return jsonify({
                'user_id': user_id,
                'notifications': []
            })

        # Convert all notifications to a list of dictionaries
        notification_list = [{
            'id': notification['id'],
            'user_id': notification['user_id'],
            'message': notification['message'],
            'mail_id': notification['mail_id'],
            'mobile_no': notification['mobile_no'],
            'timestamp': notification['timestamp']
        } for notification in notifications]

        return jsonify({
            'user_id': user_id,
            'notifications': notification_list
        })

    except Exception as e:
        return jsonify({'error': f'Error fetching notifications: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7080)