from channels.auth import channel_session_user_from_http, channel_session_user

from .models import Room

'''
Event Handler: When User Connects to the WebSocket
When a user connects to the websocket, first of all we have to identify it. In this case,
there is a decorator "channel_session_user_from_http" in the "django-channels" arsenal,
but how does this work?
This decorator takes a user from http session and inserts it into the "channel-base session"
(which uses the django standard "SESSION_ENGINE"), after which it will be available in the
"message.user" attribute.
We must also take care of creating a "channel_session rooms" for the user. It is
necessary to be able to subscribe the user to the events in a particular room.
To do this, we create a chat/consumers.py file and declare ws_connect function in it:
'''

'''
Event Handler: When User Disconnects from the WebSocket
When a user disconnects from the websocket, we need to clean up his opening session.
To identify the user, we'll need the "channel_session_user" which adds the user instance
to the received message, based on the user ID from the "channel_session".
Unlike "channel_session_user_from_http", it turns on channel session implicitly.

In order to provide a possibility to send a message to all users who are in a particular
room, "django-channels" provides an excellent opportunity to group "channels"

Let's add a method "websocket_group" in "Room" models, which will return a unique
"channels.Group" for each room through id:
'''

# This decorator copies the user from the HTTP session(only available in
# websocket.connect or http.request.messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    message.channel_session['rooms'] = []

@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    for room_id in message.channel_session.get('rooms', set()):
        try:
            room = Room.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass