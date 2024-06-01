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