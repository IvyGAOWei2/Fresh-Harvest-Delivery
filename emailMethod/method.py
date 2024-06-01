from emailMethod.sendEmail import sendEmail
from emailMethod.html import fhdContactHTML
from configparser import RawConfigParser


def sendFhdContact(name, surname, email, message):
    config, auth = RawConfigParser(), RawConfigParser()
    config.read('emailMethod/config.ini')
    auth.read('emailMethod/auth.ini')

    htmlData = fhdContactHTML(name, surname, email, message)
    sendEmail(htmlData, [config['contact']['contactEmail']], config['contact']['subject'], \
        config['contact']['header'], auth, True)