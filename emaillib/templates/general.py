from sendgrid.helpers.mail.email import Email
from .base import EmailTemplate


class GeneralEmail(EmailTemplate):

    def GetRequiredArguments(self):
        return ['title', 'content']

    def GetOptionalArguments(self):
        return ['name', 'sendername']

    def _GenerateEmail(self, **keywords) -> str:
        if 'name' not in keywords:
            keywords['name'] = 'there'
        if 'sendername' not in keywords:
            keywords['sendername'] = 'Time2Meet Team'
        return EmailTemplate.KeywordSubstitution(self.template, **keywords)

    def __init__(self) -> None:
        self.template = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html data-editor-version="2" class="sg-campaigns" xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge">
  <!--<![endif]-->
  <!--[if (gte mso 9)|(IE)]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
      <![endif]-->
  <!--[if (gte mso 9)|(IE)]>
  <style type="text/css">
    body {width: 600px;margin: 0 auto;}
    table {border-collapse: collapse;}
    table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
    img {-ms-interpolation-mode: bicubic;}
  </style>
<![endif]-->
  <style type="text/css">
    body,
    p,
    div {
      font-family: arial, helvetica, sans-serif;
      font-size: 14px;
    }

    body {
      color: #000000;
    }

    body a {
      color: #1188E6;
      text-decoration: none;
    }

    p {
      margin: 0;
      padding: 0;
    }

    table.wrapper {
      width: 100% !important;
      table-layout: fixed;
      -webkit-font-smoothing: antialiased;
      -webkit-text-size-adjust: 100%;
      -moz-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }

    img.max-width {
      max-width: 100% !important;
    }

    .column.of-2 {
      width: 50%;
    }

    .column.of-3 {
      width: 33.333%;
    }

    .column.of-4 {
      width: 25%;
    }

    ul ul ul ul {
      list-style-type: disc !important;
    }

    ol ol {
      list-style-type: lower-roman !important;
    }

    ol ol ol {
      list-style-type: lower-latin !important;
    }

    ol ol ol ol {
      list-style-type: decimal !important;
    }

    @media screen and (max-width:480px) {

      .preheader .rightColumnContent,
      .footer .rightColumnContent {
        text-align: left !important;
      }

      .preheader .rightColumnContent div,
      .preheader .rightColumnContent span,
      .footer .rightColumnContent div,
      .footer .rightColumnContent span {
        text-align: left !important;
      }

      .preheader .rightColumnContent,
      .preheader .leftColumnContent {
        font-size: 80% !important;
        padding: 5px 0;
      }

      table.wrapper-mobile {
        width: 100% !important;
        table-layout: fixed;
      }

      img.max-width {
        height: auto !important;
        max-width: 100% !important;
      }

      a.bulletproof-button {
        display: block !important;
        width: auto !important;
        font-size: 80%;
        padding-left: 0 !important;
        padding-right: 0 !important;
      }

      .columns {
        width: 100% !important;
      }

      .column {
        display: block !important;
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
      }

      .social-icon-column {
        display: inline-block !important;
      }
    }
  </style>
  <!--user entered Head Start-->
  <!--End Head user entered-->
</head>

<body>
  <center class="wrapper" data-link-color="#1188E6"
    data-body-style="font-size:14px; font-family:arial,helvetica,sans-serif; color:#000000; background-color:#FFFFFF;">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
        <tr>
          <td valign="top" bgcolor="#FFFFFF" width="100%">
            <table width="100%" role="content-container" class="outer" align="center" cellpadding="0" cellspacing="0"
              border="0">
              <tr>
                <td width="100%">
                  <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td>
                        <!--[if mso]>
    <center>
    <table><tr><td width="600">
  <![endif]-->
                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                          style="width:100%; max-width:600px;" align="center">
                          <tr>
                            <td role="modules-container"
                              style="padding:0px 0px 0px 0px; color:#000000; text-align:left;" bgcolor="#FFFFFF"
                              width="100%" align="left">
                              <table class="module preheader preheader-hide" role="module" data-type="preheader"
                                border="0" cellpadding="0" cellspacing="0" width="100%"
                                style="display: none !important; mso-hide: all; visibility: hidden; opacity: 0; color: transparent; height: 0; width: 0;">
                                <tr>
                                  <td role="module-content">
                                    <p></p>
                                  </td>
                                </tr>
                              </table>
                              <table class="wrapper" role="module" data-type="image" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="a363eca5-627e-46a1-b7d2-259423860ae9">
                                <tbody>
                                  <tr>
                                    <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top"
                                      align="center">
                                      <img class="max-width" border="0"
                                        style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;"
                                        width="600" alt="" data-proportionally-constrained="true" data-responsive="true"
                                        src="https://static.yyjlincoln.com/time2meet/time2meet-logo.jpg">
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="text" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="05b1f275-aea5-4b03-a50b-db5e88696561" data-mc-module-version="2019-10-22">
                                <tbody style="margin-left: 10px; margin-right: 10px;">
                                  <tr>
                                    <td style="padding:18px 0px 0px 0px; line-height:30px; text-align:inherit;"
                                      height="100%" valign="top" bgcolor="" role="module-content">
                                      <div>
                                        <h1 style="text-align: inherit; font-weight: 700; letter-spacing: -0.025em;">{{title}}</h1>
                                        <div></div>
                                      </div>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="text" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="a6c6c08c-5197-43da-8a59-c63636940820" data-mc-module-version="2019-10-22">
                                <tbody>
                                  <tr>
                                    <td style="padding:0px 0px 18px 0px; line-height:22px; text-align:inherit;"
                                      height="100%" valign="top" bgcolor="" role="module-content">
                                      <div>
                                        <div style="font-family: inherit; text-align: inherit; white-space: pre-line; font-size: 1.17em;">
                                          Hello <div style="font-style: italic; display: inline; font-size: inherit;">{{name}}</div>,

                                          {{content}}

                                          Regards,
                                          {{sendername}}
                                        </div>
                                        <div></div>
                                      </div>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="spacer" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="d6cd2f9f-1c9e-42c1-a39d-4d472f698e62">
                                <tbody>
                                  <tr>
                                    <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe"
                                style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:center;"
                                data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
                                <div class="Unsubscribe--addressLine"></div>
                                <p style="font-size:12px; line-height:20px;"><a class="Unsubscribe--unsubscribeLink"
                                    href="{{$unsubscribe}}" target="_blank" style="">Unsubscribe</a>
                                </p>
                                <p style="font-size:12px; line-height:20px;">
                                  By pressing unsubscribe, you'll unsubscribe to all emails including account verification emails. Contact us if you accidentally unsubscribed.
                                </p>
                                <p style="font-size:12px; line-height:20px;">
                                  Time2Meet
                                </p>
                              </div>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]>
                                  </td>
                                </tr>
                              </table>
                            </center>
                            <![endif]-->
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </center>
</body>

</html>'''


class OTPEmail(EmailTemplate):

    def GetRequiredArguments(self):
        return ['code']

    def GetOptionalArguments(self):
        return ['name', 'sendername', 'permission']

    def _GenerateEmail(self, **keywords) -> str:
        if 'name' not in keywords:
            keywords['name'] = 'there'
        if 'sendername' not in keywords:
            keywords['sendername'] = 'Time2Meet Team'
        if 'permission' not in keywords:
            keywords['permission'] = '<not specified>'
        return EmailTemplate.KeywordSubstitution(self.template, **keywords)

    def __init__(self) -> None:
        self.template = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html data-editor-version="2" class="sg-campaigns" xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge">
  <!--<![endif]-->
  <!--[if (gte mso 9)|(IE)]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
      <![endif]-->
  <!--[if (gte mso 9)|(IE)]>
  <style type="text/css">
    body {width: 600px;margin: 0 auto;}
    table {border-collapse: collapse;}
    table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
    img {-ms-interpolation-mode: bicubic;}
  </style>
<![endif]-->
  <style type="text/css">
    body,
    p,
    div {
      font-family: arial, helvetica, sans-serif;
      font-size: 14px;
    }

    body {
      color: #000000;
    }

    body a {
      color: #1188E6;
      text-decoration: none;
    }

    p {
      margin: 0;
      padding: 0;
    }

    table.wrapper {
      width: 100% !important;
      table-layout: fixed;
      -webkit-font-smoothing: antialiased;
      -webkit-text-size-adjust: 100%;
      -moz-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }

    img.max-width {
      max-width: 100% !important;
    }

    .column.of-2 {
      width: 50%;
    }

    .column.of-3 {
      width: 33.333%;
    }

    .column.of-4 {
      width: 25%;
    }

    ul ul ul ul {
      list-style-type: disc !important;
    }

    ol ol {
      list-style-type: lower-roman !important;
    }

    ol ol ol {
      list-style-type: lower-latin !important;
    }

    ol ol ol ol {
      list-style-type: decimal !important;
    }

    @media screen and (max-width:480px) {

      .preheader .rightColumnContent,
      .footer .rightColumnContent {
        text-align: left !important;
      }

      .preheader .rightColumnContent div,
      .preheader .rightColumnContent span,
      .footer .rightColumnContent div,
      .footer .rightColumnContent span {
        text-align: left !important;
      }

      .preheader .rightColumnContent,
      .preheader .leftColumnContent {
        font-size: 80% !important;
        padding: 5px 0;
      }

      table.wrapper-mobile {
        width: 100% !important;
        table-layout: fixed;
      }

      img.max-width {
        height: auto !important;
        max-width: 100% !important;
      }

      a.bulletproof-button {
        display: block !important;
        width: auto !important;
        font-size: 80%;
        padding-left: 0 !important;
        padding-right: 0 !important;
      }

      .columns {
        width: 100% !important;
      }

      .column {
        display: block !important;
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
      }

      .social-icon-column {
        display: inline-block !important;
      }
    }
  </style>
  <!--user entered Head Start-->
  <!--End Head user entered-->
</head>

<body>
  <center class="wrapper" data-link-color="#1188E6"
    data-body-style="font-size:14px; font-family:arial,helvetica,sans-serif; color:#000000; background-color:#FFFFFF;">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
        <tr>
          <td valign="top" bgcolor="#FFFFFF" width="100%">
            <table width="100%" role="content-container" class="outer" align="center" cellpadding="0" cellspacing="0"
              border="0">
              <tr>
                <td width="100%">
                  <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td>
                        <!--[if mso]>
    <center>
    <table><tr><td width="600">
  <![endif]-->
                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                          style="width:100%; max-width:600px;" align="center">
                          <tr>
                            <td role="modules-container"
                              style="padding:0px 0px 0px 0px; color:#000000; text-align:left;" bgcolor="#FFFFFF"
                              width="100%" align="left">
                              <table class="module preheader preheader-hide" role="module" data-type="preheader"
                                border="0" cellpadding="0" cellspacing="0" width="100%"
                                style="display: none !important; mso-hide: all; visibility: hidden; opacity: 0; color: transparent; height: 0; width: 0;">
                                <tr>
                                  <td role="module-content">
                                    <p></p>
                                  </td>
                                </tr>
                              </table>
                              <table class="wrapper" role="module" data-type="image" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="a363eca5-627e-46a1-b7d2-259423860ae9">
                                <tbody>
                                  <tr>
                                    <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top"
                                      align="center">
                                      <img class="max-width" border="0"
                                        style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;"
                                        width="600" alt="" data-proportionally-constrained="true" data-responsive="true"
                                        src="https://static.yyjlincoln.com/time2meet/time2meet-logo.jpg">
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="text" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="05b1f275-aea5-4b03-a50b-db5e88696561" data-mc-module-version="2019-10-22">
                                <tbody style="margin-left: 10px; margin-right: 10px;">
                                  <tr>
                                    <td style="padding:18px 0px 0px 0px; line-height:30px; text-align:inherit;"
                                      height="100%" valign="top" bgcolor="" role="module-content">
                                      <div>
                                        <h1 style="text-align: inherit; font-weight: 700; letter-spacing: -0.025em;">Your Account Verification Code</h1>
                                        <div></div>
                                      </div>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="text" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="a6c6c08c-5197-43da-8a59-c63636940820" data-mc-module-version="2019-10-22">
                                <tbody>
                                  <tr>
                                    <td style="padding:0px 0px 18px 0px; line-height:22px; text-align:inherit;"
                                      height="100%" valign="top" bgcolor="" role="module-content">
                                      <div>
                                        <div style="font-family: inherit; text-align: inherit; white-space: pre-line; font-size: 1.17em;">
                                          Hello <div style="font-style: italic; display: inline; font-size: inherit;">{{name}}</div>,

                                          You've just requested for a verification code to be sent to your email. Please use the code below to verify your identity:

                                          <strong style="text-align: center; font-size: 2em; padding-top: 15px; padding-bottom: 15px;">{{code}}</strong>

                                          The code will grant you the permission: {{permission}}

                                          If you didn't request for a verification code, please ignore this email. You account remains secure.

                                          If you have any concerns, please contact us at <a href="mailto:time2meet.support@yyjlincoln.app">time2meet.support@yyjlincoln.app</a>

                                          Thanks again for your continued support.

                                          Regards,
                                          {{sendername}}
                                        </div>
                                        <div></div>
                                      </div>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <table class="module" role="module" data-type="spacer" border="0" cellpadding="0"
                                cellspacing="0" width="100%" style="table-layout: fixed;"
                                data-muid="d6cd2f9f-1c9e-42c1-a39d-4d472f698e62">
                                <tbody>
                                  <tr>
                                    <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe"
                                style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:center;"
                                data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
                                <div class="Unsubscribe--addressLine"></div>
                                <p style="font-size:12px; line-height:20px;"><a class="Unsubscribe--unsubscribeLink"
                                    href="{{$unsubscribe}}" target="_blank" style="">Unsubscribe</a>
                                </p>
                                <p style="font-size:12px; line-height:20px;">
                                  By pressing unsubscribe, you'll unsubscribe to all emails including account verification emails. Contact us if you accidentally unsubscribed.
                                </p>
                                <p style="font-size:12px; line-height:20px;">
                                  Time2Meet
                                </p>
                              </div>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]>
                                  </td>
                                </tr>
                              </table>
                            </center>
                            <![endif]-->
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </center>
</body>

</html>'''
