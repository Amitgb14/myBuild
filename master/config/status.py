import os
from buildbot.plugins import reporters

template=u'''\
<h4>Build status: {{ summary }}</h4>
<p> Worker used: {{ workername }}</p>
{% for step in build['steps'] %}
<p> {{ step['name'] }}: {{ step['result'] }}</p>
{% endfor %}
<p><b> -- The Buildbot</b></p>
'''
fromaddr = "amitg.b14@gmail.com"
extraRecipients = ["amitg.b14@gmail.com"]
password = os.environ.get("email_pass", "")

def get_status():
    return [reporters.MailNotifier(fromaddr = fromaddr,
                            sendToInterestedUsers = False,
                            extraRecipients = extraRecipients,

                            useTls=True, relayhost = "smtp.gmail.com",
                            smtpPort = 587, smtpUser = "amitg.b14@gmail.com",
                            smtpPassword = password,

                            messageFormatter = reporters.MessageFormatter(
                            template = template, template_type = 'html',
                            wantProperties = True, wantSteps = True))
            ]

