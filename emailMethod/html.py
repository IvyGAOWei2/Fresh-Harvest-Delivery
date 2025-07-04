from markupsafe import escape

def fhdContactHTML(name, email, type, message):
    data = """<!doctype html>
    <html ⚡4email data-css-strict>

    <head>
    <meta charset="utf-8">
    <meta name="x-apple-disable-message-reformatting">
    <style amp4email-boilerplate>
        body {
        visibility: hidden
        }
    </style>

  <script async src="https://cdn.ampproject.org/v0.js"></script>


  <style amp-custom>
    .u-row {
      display: flex;
      flex-wrap: nowrap;
      margin-left: 0;
      margin-right: 0;
    }
    
    .u-row .u-col {
      position: relative;
      width: 100%;
      padding-right: 0;
      padding-left: 0;
    }
    
    .u-row .u-col.u-col-100 {
      flex: 0 0 100%;
      max-width: 100%;
    }
    
    @media (max-width: 767px) {
      .u-row:not(.no-stack) {
        flex-wrap: wrap;
      }
      .u-row:not(.no-stack) .u-col {
        flex: 0 0 100%;
        max-width: 100%;
      }
    }
    
    body {
      margin: 0;
      padding: 0;
    }
    
    table,
    tr,
    td {
      vertical-align: top;
      border-collapse: collapse;
    }
    
    p {
      margin: 0;
    }
    
    .ie-container table,
    .mso-container table {
      table-layout: fixed;
    }
    
    * {
      line-height: inherit;
    }
    
    table,
    td {
      color: #000000;
    }
    
    #u_body a {
      color: #0000ee;
      text-decoration: underline;
    }
  </style>


</head>

<body class="clean-body u_body" style="margin: 0;padding: 0;background-color: #f9f9f9;color: #000000">
  <!--[if IE]><div class="ie-container"><![endif]-->
  <!--[if mso]><div class="mso-container"><![endif]-->
  <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #f9f9f9;width:100%" cellpadding="0" cellspacing="0">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse;vertical-align: top">
          <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #f9f9f9;"><![endif]-->

          <div style="padding: 0px;">
            <div style="max-width: 600px;margin: 0 auto;">
              <div class="u-row">

                <div class="u-col u-col-100" style="display:flex;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                  <div style="width: 100%;padding:0px;">

                  </div>
                </div>

              </div>
            </div>
          </div>

          <div style="padding: 0px;">
            <div style="max-width: 600px;margin: 0 auto;background-color: #ffffff;">
              <div class="u-row">

                <div class="u-col u-col-100" style="display:flex;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                  <div style="width: 100%;padding:0px;">

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Cabin',sans-serif;" align="left">

                            <div style="font-family: arial black,AvenirNext-Heavy,avant garde,arial; font-size: 34px; font-weight: 700; color: #a5dc45; line-height: 140%; text-align: center; word-wrap: break-word;">
                              <p style="line-height: 140%;">FRESH HARVEST DELIVERY</p>
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>
                </div>

              </div>
            </div>
          </div>

          <div style="padding: 0px;">
            <div style="max-width: 600px;margin: 0 auto;background-color: #003399;">
              <div class="u-row">

                <div class="u-col u-col-100" style="display:flex;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                  <div style="width: 100%;padding:0px;">

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:40px 10px 10px;font-family:'Cabin',sans-serif;" align="left">

                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                              <tr>
                                <td style="padding-right: 0px;padding-left: 0px;" align="center">

                                  <amp-img alt="Image" src="https://cdn.templates.unlayer.com/assets/1597218650916-xxxxc.png" width="335" height="93" layout="intrinsic" style="width: 26%;max-width: 26%;">

                                  </amp-img>
                                </td>
                              </tr>
                            </table>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Cabin',sans-serif;" align="left">

                            <div style="font-size: 14px; color: #e5eaf5; line-height: 140%; text-align: center; word-wrap: break-word;">
                              <p style="font-size: 14px; line-height: 140%;"><span style="font-size: 20px; line-height: 28px;"><strong>""" + str(escape(type)) + """</strong></span></p>
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:0px 10px 31px;font-family:'Cabin',sans-serif;" align="left">

                            <div style="font-size: 14px; color: #e5eaf5; line-height: 140%; text-align: center; word-wrap: break-word;">
                              <p style="font-size: 14px; line-height: 140%;"><span style="font-size: 28px; line-height: 39.2px;"><strong><span style="line-height: 39.2px; font-size: 28px;">USER: """ + str(escape(name)) + """</span></strong>
                                </span>
                              </p>
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>
                </div>

              </div>
            </div>
          </div>

          <div style="padding: 0px;">
            <div style="max-width: 600px;margin: 0 auto;background-color: #ffffff;">
              <div class="u-row">

                <div class="u-col u-col-100" style="display:flex;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                  <div style="width: 100%;padding:0px;">

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:33px 55px;font-family:'Cabin',sans-serif;" align="left">

                            <div style="font-size: 14px; line-height: 160%; text-align: center; word-wrap: break-word;">
                              <p style="line-height: 160%;">Email: """ + str(escape(email)) + """</p>
                              <p style="line-height: 160%;">Contact Message: """ + str(escape(message)) + """</p>
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Cabin',sans-serif;" align="left">

                            <!--[if mso]><style>.v-button {background: transparent;}</style><![endif]-->
                            <div align="center">
                              <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" style="height:45px; v-text-anchor:middle; width:120px;" arcsize="9%"  stroke="f" fillcolor="#3AAEE0"><w:anchorlock/><center style="color:#FFFFFF;"><![endif]-->
                              <a target="_blank" class="v-button" style="box-sizing: border-box;display: inline-block;text-decoration: none;text-align: center;color: #FFFFFF; background-color: #3AAEE0; border-radius: 4px;  width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; font-size: 14px;">
                                <span style="display:block;padding:10px 20px;line-height:120%;"><span style="font-size: 14px; line-height: 16.8px;">Button Text</span></span>
                              </a>
                              <!--[if mso]></center></v:roundrect><![endif]-->
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>
                </div>

              </div>
            </div>
          </div>

          <div style="padding: 0px;">
            <div style="max-width: 600px;margin: 0 auto;background-color: #003399;">
              <div class="u-row">

                <div class="u-col u-col-100" style="display:flex;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                  <div style="width: 100%;padding:0px;">

                    <table style="font-family:'Cabin',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
                      <tbody>
                        <tr>
                          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Cabin',sans-serif;" align="left">

                            <div style="font-size: 14px; color: #fafafa; line-height: 180%; text-align: center; word-wrap: break-word;">
                              <p style="font-size: 14px; line-height: 180%;"><span style="font-size: 16px; line-height: 28.8px;">Copyrights © Company All Rights Reserved</span></p>
                            </div>

                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>
                </div>

              </div>
            </div>
          </div>

          <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
        </td>
      </tr>
    </tbody>
  </table>
  <!--[if mso]></div><![endif]-->
  <!--[if IE]></div><![endif]-->
</body>

</html> """
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
        <p>Dear Customer,</p>
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


def orderStatususHTML(order_id, name, order_date, order_status):
    data = """
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <!--[if gte mso 9]>
        <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="x-apple-disable-message-reformatting">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title></title>
        <style type="text/css">
        @media only screen and (min-width: 620px) {.u-row {width: 600px !important;}.u-row .u-col {vertical-align: top;}.u-row .u-col-100 {width: 600px !important;}}
        @media (max-width: 620px) {.u-row-container {max-width: 100% !important;padding-left: 0px !important;padding-right: 0px !important;}.u-row .u-col {min-width: 320px !important;max-width: 100% !important;display: block !important;}.u-row {width: 100% !important;}.u-col {width: 100% !important;}.u-col > div {margin: 0 auto;}}
        body {margin: 0;padding: 0;}
        table, tr, td {vertical-align: top;border-collapse: collapse;}
        p {margin: 0;}
        .ie-container table, .mso-container table {table-layout: fixed;}
        * {line-height: inherit;}
        a[x-apple-data-detectors='true'] {color: inherit !important;text-decoration: none !important;}
        table, td {color: #000000;} @media (max-width: 480px) { #u_content_heading_1 .v-container-padding-padding { padding: 40px 10px 0px !important; } #u_content_heading_1 .v-font-size { font-size: 28px !important; } #u_content_text_1 .v-container-padding-padding { padding: 0px 10px 10px !important; } #u_content_text_2 .v-container-padding-padding { padding: 10px 10px 20px !important; } }
            </style>
        <link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css">
        </head>
        <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #ecf0f1;color: #000000">
        <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #ecf0f1;width:100%" cellpadding="0" cellspacing="0">
        <tbody>
        <tr style="vertical-align: top">
            <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
            <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
            <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="background-color: #ffffff;height: 100%;width: 100% !important;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 10px solid #ff2828;border-left: 10px solid #ff2828;border-right: 10px solid #ff2828;border-bottom: 10px solid #ff2828;">
        <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding-right: 0px;padding-left: 0px;" align="center">
            <img align="center" border="0" src="https://vir.mengya.date/images/order2.jpg" alt="image" title="image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 600px;" width="600"/>
            </td>
        </tr>
        </table>
            </td>
            </tr>
        </tbody>
        </table>
        <table id="u_content_heading_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:61px 10px 0px;font-family:'Raleway',sans-serif;" align="left">
            <h1 class="v-font-size" style="margin: 0 0 2rem 0; line-height: 140%; text-align: center; word-wrap: break-word; font-size: 30px; font-weight: 400;"><span><strong>Dear """ + str(escape(name)) + """</strong></span></h1>
            </td>
            </tr>
        </tbody>
        </table>
        <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px 10px 10px;font-family:'Raleway',sans-serif;" align="left">
            <h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-size: 16px; font-weight: 400;"><p>Your Order is """ + str(escape(order_status)) + """.</p></h1>
            </td>
            </tr>
        </tbody>
        </table>
        <table id="u_content_text_1" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px 50px 10px;font-family:'Raleway',sans-serif;" align="left">
        <div class="v-font-size" style="font-size: 14px; line-height: 140%; text-align: left; word-wrap: break-word;">
            <p style="line-height: 140%;">Thank you for your recent order with Fresh Harvest Delivery! We are currently processing your order #""" + str(escape(order_id)) + """ placed on """ + str(escape(order_date)) + """.</p>
        <p style="line-height: 140%;"> </p>
        <p style="line-height: 140%;">Your order is now in the '""" + str(escape(order_status)) + """' status. We will notify you as soon as it progresses to the next stage.</p>
        <p style="line-height: 140%;"> </p>
        <p style="line-height: 140%;">Thank you for choosing Fresh Harvest Delivery. If you have any questions, feel free to contact our customer support.</p>
        <p style="line-height: 140%;"> </p>
        <p style="line-height: 140%;">Best regards,</p>
        <p style="line-height: 140%;">The Fresh Harvest Delivery Team</p>
        </div>
            </td>
            </tr>
        </tbody>
        </table>
        <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;" align="left">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding-right: 0px;padding-left: 0px;" align="center">
            <img align="center" border="0" src="https://vir.mengya.date/images/order1.png" alt="border" title="border" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 600px;" width="600"/>
            </td>
        </tr>
        </table>
            </td>
            </tr>
        </tbody>
        </table>
        <table id="u_content_text_2" style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
            <tr>
            <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 50px 20px;font-family:'Raleway',sans-serif;" align="left">
        <div class="v-font-size" style="font-size: 14px; line-height: 140%; text-align: left; word-wrap: break-word;">
            <p style="line-height: 140%;">If you didn't place this order, please contact our support team immediately.</p>
        </div>
            </td>
            </tr>
        </tbody>
        </table>
        </div>
        </div>
            </div>
            </div>
        </div>
        </div>
            </td>
        </tr>
        </tbody>
        </table>
        </body>
        </html>
    """
    return data