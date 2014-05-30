from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder
from ajenti.ui import on
from email.message import Message
from email.header import decode_header
import dateutil.parser
import mailbox
import pwd
import os

class MessageProxy(object):
    def __init__(self, message):
        self.message = message
        self.date = dateutil.parser.parse(message.get('date'))
        self.selected = False

    def __getattr__(self, name):
        name = name.replace('_', '-')
        return self.get(name) if name in self.message else getattr(self.message, name)

    def get(self, name, default=None):
        return u''.join(map(lambda h: unicode(h[0], h[1] or 'latin1'),
            decode_header(self.message.get(name))))

def message_factory(messageClass):
    def factory(data):
        return MessageProxy(messageClass(data))
    return factory

@plugin
class MailPlugin(SectionPlugin):

    def init(self):
        # meta-data
        self.title = _('Mail')
        self.icon = 'envelope'
        self.category = _("Software")

        self.append(self.ui.inflate('mail:main'))

    def on_first_page_load(self):
        username = 'beamin' # pwd.getpwuid(os.getuid()).pw_name
        self.mbox = mailbox.mbox('/home/kstep/beamin', factory=message_factory(mailbox.mboxMessage))
        self.binder = Binder(self, self.find('main'))
        self.binder.populate()

    @on('refresh', 'click')
    def refresh(self):
        self.binder.populate()

