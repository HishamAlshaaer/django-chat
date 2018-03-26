'''
Since we want to notify users about something, let's add some gradation of messages
by a level of importance. To do this, let's create a "chat/settings.py", where we
define the types of messages.
'''
from django.conf import settings

NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS = getattr(settings, 'NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS', True)

MSG_TYPE_MESSAGE = 0 # For Standard Messages
MSG_TYPE_WARNING = 1 # For Yellow Messages
MSG_TYPE_ALERT = 2 # For red and dangerous alerts
MSG_TYPE_MUTED = 3 # For Just OK information that doesn't bother users
MSG_TYPE_ENTER = 4 # For Just OK information that doesn't bother users
MSG_TYPE_LEAVE = 5 # For Just Ok information that doesn't bother users

MESSAGE_TYPES_CHOICES = getattr(settings, 'MESSAGE_TYPES_CHOICES', (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_ALERT, 'ALERT'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE')))

MESSAGE_TYPES_LIST = getattr(settings, 'MESSAGE_TYPES_LIST',
                             [MSG_TYPE_MESSAGE,
                              MSG_TYPE_WARNING,
                              MSG_TYPE_ALERT,
                              MSG_TYPE_MUTED,
                              MSG_TYPE_ENTER,
                              MSG_TYPE_LEAVE])