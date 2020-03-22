import json
import socket
import datetime
from database_connection import MongoDB
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from message_filtering import is_valid
from Constants import Constants

with open('properties_user', 'r') as f:
 user_data = json.load(f)

# Set up your credentials
consumer_key = user_data['consumer_key']
consumer_secret = user_data['consumer_secret']
access_token = user_data['access_token']
access_secret = user_data['access_secret']


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        super().__init__()
        self.client_socket = csocket
        self.database = MongoDB()

    def on_data(self, data):
        try:
            msg = json.loads(data)

            if is_valid(msg):
                msg['inserted_at'] = datetime.datetime.utcnow()
                self.database.insert_one(msg)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def send_data(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))

    twitter_stream.filter(track=Constants.TRACKS, languages=Constants.LANGUAGES)


def run_api_twitter():
    s = socket.socket()  # Create a socket object

    s.bind((user_data['host'], user_data['port']))  # Bind to the port

    print("Listening on port: %s" % str(user_data['port']))

    s.listen(5)  # Now wait for client connection.
    print('listen')
    c, addr = s.accept()  # Establish connection with client.

    print("Received request from: " + str(addr))

    send_data(c)


if __name__ == "__main__":
    run_api_twitter()
