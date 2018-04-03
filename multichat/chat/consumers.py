from channels.auth import channel_session_user_from_http, channel_session_user

from multichat.chat.settings import NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS, MSG_TYPE_ENTER
from multichat.chat.utils import get_room_or_error, catch_client_error
from .models import Room

import json
from channels import Channel

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

'''
Message Processing:
    For comfortable work we will send the data in the form of "json", so when you receive
    a message we will parse "json", and send the received data into the "channel".
'''

# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of it's own with a few attributes extra so we can route it.
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
def ws_receive(message):
    # All websockets frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding,'
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel('chat.receive').send(payload)


# Channel _session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
@channel_session_user
@catch_client_error
def chat_join(message):
    # Find the room they requested (by ID) and add ourselves to the send group
    # Note that, because of channel_session_user, we have a message.user
    # object that works just like request.user would. Security!
    room = get_room_or_error(message['room'], message.user)

    # Send a "enter message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    # OK, add them in. The websocket_group is what we'll send messages
    # to so that everyone in the chat room gets them.
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.chennel_session['rooms']).union([room.id]))
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })

