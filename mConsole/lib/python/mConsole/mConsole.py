import persistent
from zope.app import pagetemplate
from zope import interface, schema


class base(persistent.Persistent):
    greeting = 'Hello'
    subject = 'world'
    
class IHelloWorld(interface.Interface):
    greeting = schema.TextLine()
    subject = schema.TextLine()


class MessageView(object):
    interface.implements(IHelloWorld)
    def message(self):
        return '%s %s!' % (self.context.greeting, self.context.subject)

    template = pagetemplate.ViewPageTemplateFile('mConsole.pt')
    def __call__(self):
	return self.template()
  