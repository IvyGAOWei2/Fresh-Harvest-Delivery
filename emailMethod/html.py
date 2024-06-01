from markupsafe import escape


def fhdContactHTML(name, type, email, message):
    data = """
        <html><head><style>p{color:#000}</style><title></title></head><body><div>
        <p>First Name: """ + str(escape(name)) + """</p>
        <p>Type: """ + str(escape(type)) + """</p>
        <p>Contact Email: """ + email + """</p>
        <p>Message: """ + str(escape(message)) + """</p><br>
        </div></body></html>
    """
    return data


def resetPasswordHTML(email, temporary_password):
    data = """
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset Notification</title>
        <style>
        body{font-family:Arial,sans-serif;background-color:#f4f4f4;margin:0;padding:0}
        .container{max-width:600px;margin:20px auto;background-color:#fff;border-radius:8px;padding:20px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
        h2{color:#333}
        p{margin-bottom:10px}
        strong{font-weight:bold}
        em{font-style:italic}
        </style>
        </head>
        <body>
        <div class="container">
        <h2>Password Reset Notification</h2>
        <p>Dear User,</p>
        <p>Hello! We have received a request to reset the password for your account (<strong>""" + str(escape(email)) + """</strong>). Your temporary password is: <strong>""" + str(escape(temporary_password)) + """</strong>.</p>
        <p>Please use this password to log in to your account. After logging in, please change your password as soon as possible to ensure account security.</p>
        <p><strong>Note:</strong> Your temporary password will expire after 24 hours. Please make sure to use it before then.</p>
        <p>If you have any questions or need assistance, please contact our customer service team.</p>
        <p>Thank you for your cooperation and support.</p>
        <p>Best regards,</p>
        <p><em>FreshHarvestDelivery Ltd</em></p>
        </div>
        </body>
        </html>
    """
    return data