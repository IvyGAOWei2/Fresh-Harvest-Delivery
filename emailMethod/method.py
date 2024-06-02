from emailMethod.sendEmail import sendEmail
from emailMethod.html import fhdContactHTML, resetPasswordHTML
from configparser import RawConfigParser


config, auth = RawConfigParser(), RawConfigParser()
config.read('emailMethod/config.ini')
auth.read('emailMethod/auth.ini')

def sendFhdContact(name, surname, email, message):
    htmlData = fhdContactHTML(name, surname, email, message)
    sendEmail(htmlData, [config['contact']['contactEmail']], config['contact']['subject'], \
        config['contact']['header'], auth, True)

def sendResetPassword(email, temporary_password):
    htmlData = resetPasswordHTML(email, temporary_password)
    sendEmail(htmlData, [config['reset_password']['consumerEmail']], config['reset_password']['subject'], \
        config['reset_password']['header'], auth, True)