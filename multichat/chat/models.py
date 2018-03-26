from django.db import models
from six import python_2_unicode_compatible
from channels import Group

# Create your models here.

@python_2_unicode_compatible
class Room(models.Model):
    '''
    A room for people to chat in.
    '''

    # Room title
    title = models.CharField(max_length=255)

    # If only 'staff' users are allowed (is_staff on djano's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property
    def websocket_group(self):
        '''
        Returns the Channels Group that sockets should subscribe to get sent
        messages as they are generated.
        '''
        return Group('room-%s' % self.id)