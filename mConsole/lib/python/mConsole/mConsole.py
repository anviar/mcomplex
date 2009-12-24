import persistent
from zope.app import pagetemplate

class base(persistent.Persistent):
    greeting = 'Hello'
    subject = 'world'

class MessageView(object):

    def message(self):
        return '%s %s!' % (self.context.greeting, self.context.subject)

    template = pagetemplate.ViewPageTemplateFile('mConsole.pt')
    def __call__(self):
	return self.template()
  