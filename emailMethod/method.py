from emailMethod.sendEmail import sendEmail
from emailMethod.html import fhdContactHTML, resetPasswordHTML, orderStatususHTML
from configparser import RawConfigParser


config, auth = RawConfigParser(), RawConfigParser()
config.read('emailMethod/config.ini')
auth.read('emailMethod/auth.ini')
# config.read('/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/emailMethod/config.ini')
# auth.read('/home/COMP639S1GroupAZ/COMP639S1_Group_AZ/emailMethod/auth.ini')

def sendFhdContact(name, email, type, message):
    htmlData = fhdContactHTML(name, email, type, message)
    sendEmail(htmlData, [config['contact']['contactEmail']], config['contact']['subject'], \
        config['contact']['header'], auth, True)

def sendResetPassword(email, temporary_password):
    htmlData = resetPasswordHTML(email, temporary_password)
    sendEmail(htmlData, email, config['reset_password']['subject'], config['reset_password']['header'], auth, True)
    
def sendOrderStatus(email, order_id, name, order_date, order_status):
    htmlData = orderStatususHTML(order_id, name, order_date, order_status)
    sendEmail(htmlData, email, config['order_status']['subject1'] + ' ' + order_status, config['order_status']['header'], auth, True)