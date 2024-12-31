# TO run the code 
run docker compose up --build 

#
this will build the docker container with a functioning rabbitmq server, it will also start a flask server and the consumer.py to send the api calls

# To send mail 
simply send a post request here
http://localhost:7080/notifications
#
{
  "user_id": 3,
  "message": "message",
  "mail_id":"mail",
  "mobile_no": "number",
  "type":"email"
}
#
this is thejson format

To send messages you will need make a CONF.py and then add your own api key  from twilio. Messages can only be sent to your own registered mobile number using the free version of the api. 

Rabbitmq server will stay active for 10 mins without any inactivity, if you exceed 10 mins then the server will start to shutdown. You can easily reconfigure this. 
https://github.com/dantesbane/notification-app

you can also use the flutter app to see all the notifications from this url
