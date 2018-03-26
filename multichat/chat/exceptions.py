'''
Users logged into the chat:
    One of the important features of our app is the ability to enter specific chat room,
    but what happens if an unauthorized user tries to do it? And what if the requested
    room does not exist? Or if the user had no rights to enter this room at all? That's right,
    an error will occur! And in the first two cases, it will clearly be thrown at the system level,
    and in the third case the user will likely get to the secret room. To prevent such
    a  trouble from hapenning, we need to add error handling.

    Let's create "chat/exceptions.py" file and declare "ClientError" class in it:
'''

import json


class ClientError(Exception):
    '''
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client
    '''
    def init(self, code):
        super(ClientError, self).init(code)
        self.code = code
    
    def send_to(self, channel):
        channel.send({
            'text': json.dumps({
                'error': self.code,
            }),
        })

'''
In the future, if any error occurs, when using this class we will notify the client-side.
Now let's create "chat/utils.py" and declare decorators needed for error handling there.
'''