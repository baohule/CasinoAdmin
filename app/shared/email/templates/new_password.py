def get_template(name, password):
    return f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office"
      style="width:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>New email template 2023-04-13</title><!--[if (mso 16)]>
    <style type="text/css">
        a {{
            text-decoration: none;
        }}
    </style>
    <![endif]--><!--[if gte mso 9]>
    <style>sup {{
        font-size: 100% !important;
    }}</style><![endif]--><!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG></o:AllowPNG>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]--><!--[if !mso]><!-- -->
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet"><!--<![endif]-->
    <style type="text/css">
        .jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, #bit-notification-bar-iframe, ::-webkit-calendar-picker-indicator, div[role="dialog"] div[role="document"], div[role="dialog"] div[role="document"] {{
            filter: invert(100%) hue-rotate(180deg) contrast(80%) sepia(10%) !important;
        }}

        [data-darkreader-inline-bgcolor] {{
            background-color: var(--darkreader-inline-bgcolor) !important;
        }}

        [data-darkreader-inline-bgimage] {{
            background-image: var(--darkreader-inline-bgimage) !important;
        }}

        [data-darkreader-inline-border] {{
            border-color: var(--darkreader-inline-border) !important;
        }}

        [data-darkreader-inline-border-bottom] {{
            border-bottom-color: var(--darkreader-inline-border-bottom) !important;
        }}

        [data-darkreader-inline-border-left] {{
            border-left-color: var(--darkreader-inline-border-left) !important;
        }}

        [data-darkreader-inline-border-right] {{
            border-right-color: var(--darkreader-inline-border-right) !important;
        }}

        [data-darkreader-inline-border-top] {{
            border-top-color: var(--darkreader-inline-border-top) !important;
        }}

        [data-darkreader-inline-boxshadow] {{
            box-shadow: var(--darkreader-inline-boxshadow) !important;
        }}

        [data-darkreader-inline-color] {{
            color: var(--darkreader-inline-color) !important;
        }}

        [data-darkreader-inline-fill] {{
            fill: var(--darkreader-inline-fill) !important;
        }}

        [data-darkreader-inline-stroke] {{
            stroke: var(--darkreader-inline-stroke) !important;
        }}

        [data-darkreader-inline-outline] {{
            outline-color: var(--darkreader-inline-outline) !important;
        }}

        [data-darkreader-inline-stopcolor] {{
            stop-color: var(--darkreader-inline-stopcolor) !important;
        }}

        :root {{
            --darkreader-neutral-background: #1f2020;
            --darkreader-neutral-text: #d6d0c6;
            --darkreader-selection-background: #15539c;
            --darkreader-selection-text: #e5e0d8;
        }}

        html {{
            color-scheme: dark !important;
        }}

        input, textarea, select, button, dialog {{
            background-color: #242525;
        }}

        html, body, input, textarea, select, button {{
            border-color: #776f62;
            color: #e5e0d8;
        }}

        a {{
            color: #4791e6;
        }}

        table {{
            border-color: #5c6060;
        }}

        ::placeholder {{
            color: #b2aa9e;
        }}

        input:-webkit-autofill,
        textarea:-webkit-autofill,
        select:-webkit-autofill {{
            background-color: #484a12 !important;
            color: #e5e0d8 !important;
        }}

        ::-webkit-scrollbar {{
            background-color: #2b2d2d;
            color: #aca496;
        }}

        ::-webkit-scrollbar-thumb {{
            background-color: #4e5151;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background-color: #5f6364;
        }}

        ::-webkit-scrollbar-thumb:active {{
            background-color: #515455;
        }}

        ::-webkit-scrollbar-corner {{
            background-color: #242525;
        }}

        ::selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        ::-moz-selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        .jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, #bit-notification-bar-iframe, ::-webkit-calendar-picker-indicator {{
            filter: invert(100%) hue-rotate(180deg) contrast(80%) sepia(10%) !important;
        }}

        [data-darkreader-inline-bgcolor] {{
            background-color: var(--darkreader-inline-bgcolor) !important;
        }}

        [data-darkreader-inline-bgimage] {{
            background-image: var(--darkreader-inline-bgimage) !important;
        }}

        [data-darkreader-inline-border] {{
            border-color: var(--darkreader-inline-border) !important;
        }}

        [data-darkreader-inline-border-bottom] {{
            border-bottom-color: var(--darkreader-inline-border-bottom) !important;
        }}

        [data-darkreader-inline-border-left] {{
            border-left-color: var(--darkreader-inline-border-left) !important;
        }}

        [data-darkreader-inline-border-right] {{
            border-right-color: var(--darkreader-inline-border-right) !important;
        }}

        [data-darkreader-inline-border-top] {{
            border-top-color: var(--darkreader-inline-border-top) !important;
        }}

        [data-darkreader-inline-boxshadow] {{
            box-shadow: var(--darkreader-inline-boxshadow) !important;
        }}

        [data-darkreader-inline-color] {{
            color: var(--darkreader-inline-color) !important;
        }}

        [data-darkreader-inline-fill] {{
            fill: var(--darkreader-inline-fill) !important;
        }}

        [data-darkreader-inline-stroke] {{
            stroke: var(--darkreader-inline-stroke) !important;
        }}

        [data-darkreader-inline-outline] {{
            outline-color: var(--darkreader-inline-outline) !important;
        }}

        [data-darkreader-inline-stopcolor] {{
            stop-color: var(--darkreader-inline-stopcolor) !important;
        }}

        :root {{
            --darkreader-neutral-background: #1f2020;
            --darkreader-neutral-text: #d6d0c6;
            --darkreader-selection-background: #15539c;
            --darkreader-selection-text: #e5e0d8;
        }}

        html {{
            color-scheme: dark !important;
        }}

        input, textarea, select, button, dialog {{
            background-color: #242525;
        }}

        html, body, input, textarea, select, button {{
            border-color: #776f62;
            color: #e5e0d8;
        }}

        a {{
            color: #4791e6;
        }}

        table {{
            border-color: #5c6060;
        }}

        ::placeholder {{
            color: #b2aa9e;
        }}

        input:-webkit-autofill,
        textarea:-webkit-autofill,
        select:-webkit-autofill {{
            background-color: #484a12 !important;
            color: #e5e0d8 !important;
        }}

        ::-webkit-scrollbar {{
            background-color: #2b2d2d;
            color: #aca496;
        }}

        ::-webkit-scrollbar-thumb {{
            background-color: #4e5151;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background-color: #5f6364;
        }}

        ::-webkit-scrollbar-thumb:active {{
            background-color: #515455;
        }}

        ::-webkit-scrollbar-corner {{
            background-color: #242525;
        }}

        ::selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        ::-moz-selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        .jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, #bit-notification-bar-iframe, ::-webkit-calendar-picker-indicator {{
            filter: invert(100%) hue-rotate(180deg) contrast(80%) sepia(10%) !important;
        }}

        [data-darkreader-inline-bgcolor] {{
            background-color: var(--darkreader-inline-bgcolor) !important;
        }}

        [data-darkreader-inline-bgimage] {{
            background-image: var(--darkreader-inline-bgimage) !important;
        }}

        [data-darkreader-inline-border] {{
            border-color: var(--darkreader-inline-border) !important;
        }}

        [data-darkreader-inline-border-bottom] {{
            border-bottom-color: var(--darkreader-inline-border-bottom) !important;
        }}

        [data-darkreader-inline-border-left] {{
            border-left-color: var(--darkreader-inline-border-left) !important;
        }}

        [data-darkreader-inline-border-right] {{
            border-right-color: var(--darkreader-inline-border-right) !important;
        }}

        [data-darkreader-inline-border-top] {{
            border-top-color: var(--darkreader-inline-border-top) !important;
        }}

        [data-darkreader-inline-boxshadow] {{
            box-shadow: var(--darkreader-inline-boxshadow) !important;
        }}

        [data-darkreader-inline-color] {{
            color: var(--darkreader-inline-color) !important;
        }}

        [data-darkreader-inline-fill] {{
            fill: var(--darkreader-inline-fill) !important;
        }}

        [data-darkreader-inline-stroke] {{
            stroke: var(--darkreader-inline-stroke) !important;
        }}

        [data-darkreader-inline-outline] {{
            outline-color: var(--darkreader-inline-outline) !important;
        }}

        [data-darkreader-inline-stopcolor] {{
            stop-color: var(--darkreader-inline-stopcolor) !important;
        }}

        :root {{
            --darkreader-neutral-background: #1f2020;
            --darkreader-neutral-text: #d6d0c6;
            --darkreader-selection-background: #15539c;
            --darkreader-selection-text: #e5e0d8;
        }}

        html {{
            color-scheme: dark !important;
        }}

        input, textarea, select, button, dialog {{
            background-color: #242525;
        }}

        html, body, input, textarea, select, button {{
            border-color: #776f62;
            color: #e5e0d8;
        }}

        a {{
            color: #4791e6;
        }}

        table {{
            border-color: #5c6060;
        }}

        ::placeholder {{
            color: #b2aa9e;
        }}

        input:-webkit-autofill,
        textarea:-webkit-autofill,
        select:-webkit-autofill {{
            background-color: #484a12 !important;
            color: #e5e0d8 !important;
        }}

        ::-webkit-scrollbar {{
            background-color: #2b2d2d;
            color: #aca496;
        }}

        ::-webkit-scrollbar-thumb {{
            background-color: #4e5151;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background-color: #5f6364;
        }}

        ::-webkit-scrollbar-thumb:active {{
            background-color: #515455;
        }}

        ::-webkit-scrollbar-corner {{
            background-color: #242525;
        }}

        ::selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        ::-moz-selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        .jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, #bit-notification-bar-iframe, ::-webkit-calendar-picker-indicator {{
            filter: invert(100%) hue-rotate(180deg) contrast(80%) sepia(10%) !important;
        }}

        [data-darkreader-inline-bgcolor] {{
            background-color: var(--darkreader-inline-bgcolor) !important;
        }}

        [data-darkreader-inline-bgimage] {{
            background-image: var(--darkreader-inline-bgimage) !important;
        }}

        [data-darkreader-inline-border] {{
            border-color: var(--darkreader-inline-border) !important;
        }}

        [data-darkreader-inline-border-bottom] {{
            border-bottom-color: var(--darkreader-inline-border-bottom) !important;
        }}

        [data-darkreader-inline-border-left] {{
            border-left-color: var(--darkreader-inline-border-left) !important;
        }}

        [data-darkreader-inline-border-right] {{
            border-right-color: var(--darkreader-inline-border-right) !important;
        }}

        [data-darkreader-inline-border-top] {{
            border-top-color: var(--darkreader-inline-border-top) !important;
        }}

        [data-darkreader-inline-boxshadow] {{
            box-shadow: var(--darkreader-inline-boxshadow) !important;
        }}

        [data-darkreader-inline-color] {{
            color: var(--darkreader-inline-color) !important;
        }}

        [data-darkreader-inline-fill] {{
            fill: var(--darkreader-inline-fill) !important;
        }}

        [data-darkreader-inline-stroke] {{
            stroke: var(--darkreader-inline-stroke) !important;
        }}

        [data-darkreader-inline-outline] {{
            outline-color: var(--darkreader-inline-outline) !important;
        }}

        [data-darkreader-inline-stopcolor] {{
            stop-color: var(--darkreader-inline-stopcolor) !important;
        }}

        :root {{
            --darkreader-neutral-background: #1f2020;
            --darkreader-neutral-text: #d6d0c6;
            --darkreader-selection-background: #15539c;
            --darkreader-selection-text: #e5e0d8;
        }}

        html {{
            color-scheme: dark !important;
        }}

        input, textarea, select, button, dialog {{
            background-color: #242525;
        }}

        html, body, input, textarea, select, button {{
            border-color: #776f62;
            color: #e5e0d8;
        }}

        a {{
            color: #4791e6;
        }}

        table {{
            border-color: #5c6060;
        }}

        ::placeholder {{
            color: #b2aa9e;
        }}

        input:-webkit-autofill,
        textarea:-webkit-autofill,
        select:-webkit-autofill {{
            background-color: #484a12 !important;
            color: #e5e0d8 !important;
        }}

        ::-webkit-scrollbar {{
            background-color: #2b2d2d;
            color: #aca496;
        }}

        ::-webkit-scrollbar-thumb {{
            background-color: #4e5151;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background-color: #5f6364;
        }}

        ::-webkit-scrollbar-thumb:active {{
            background-color: #515455;
        }}

        ::-webkit-scrollbar-corner {{
            background-color: #242525;
        }}

        ::selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        ::-moz-selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        .jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, #bit-notification-bar-iframe, ::-webkit-calendar-picker-indicator {{
            filter: invert(100%) hue-rotate(180deg) contrast(80%) sepia(10%) !important;
        }}

        [data-darkreader-inline-bgcolor] {{
            background-color: var(--darkreader-inline-bgcolor) !important;
        }}

        [data-darkreader-inline-bgimage] {{
            background-image: var(--darkreader-inline-bgimage) !important;
        }}

        [data-darkreader-inline-border] {{
            border-color: var(--darkreader-inline-border) !important;
        }}

        [data-darkreader-inline-border-bottom] {{
            border-bottom-color: var(--darkreader-inline-border-bottom) !important;
        }}

        [data-darkreader-inline-border-left] {{
            border-left-color: var(--darkreader-inline-border-left) !important;
        }}

        [data-darkreader-inline-border-right] {{
            border-right-color: var(--darkreader-inline-border-right) !important;
        }}

        [data-darkreader-inline-border-top] {{
            border-top-color: var(--darkreader-inline-border-top) !important;
        }}

        [data-darkreader-inline-boxshadow] {{
            box-shadow: var(--darkreader-inline-boxshadow) !important;
        }}

        [data-darkreader-inline-color] {{
            color: var(--darkreader-inline-color) !important;
        }}

        [data-darkreader-inline-fill] {{
            fill: var(--darkreader-inline-fill) !important;
        }}

        [data-darkreader-inline-stroke] {{
            stroke: var(--darkreader-inline-stroke) !important;
        }}

        [data-darkreader-inline-outline] {{
            outline-color: var(--darkreader-inline-outline) !important;
        }}

        [data-darkreader-inline-stopcolor] {{
            stop-color: var(--darkreader-inline-stopcolor) !important;
        }}

        :root {{
            --darkreader-neutral-background: #1f2020;
            --darkreader-neutral-text: #d6d0c6;
            --darkreader-selection-background: #15539c;
            --darkreader-selection-text: #e5e0d8;
        }}

        html {{
            color-scheme: dark !important;
        }}

        input, textarea, select, button, dialog {{
            background-color: #242525;
        }}

        html, body, input, textarea, select, button {{
            border-color: #776f62;
            color: #e5e0d8;
        }}

        a {{
            color: #4791e6;
        }}

        table {{
            border-color: #5c6060;
        }}

        ::placeholder {{
            color: #b2aa9e;
        }}

        input:-webkit-autofill,
        textarea:-webkit-autofill,
        select:-webkit-autofill {{
            background-color: #484a12 !important;
            color: #e5e0d8 !important;
        }}

        ::-webkit-scrollbar {{
            background-color: #2b2d2d;
            color: #aca496;
        }}

        ::-webkit-scrollbar-thumb {{
            background-color: #4e5151;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background-color: #5f6364;
        }}

        ::-webkit-scrollbar-thumb:active {{
            background-color: #515455;
        }}

        ::-webkit-scrollbar-corner {{
            background-color: #242525;
        }}

        ::selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        ::-moz-selection {{
            background-color: #15539c !important;
            color: #e5e0d8 !important;
        }}

        #outlook a {{
            padding: 0;
        }}

        .ExternalClass {{
            width: 100%;
        }}

        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {{
            line-height: 100%;
        }}

        .es-button {{
            mso-style-priority: 100 !important;
            text-decoration: none !important;
        }}

        a[x-apple-data-detectors] {{
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }}

        .es-desk-hidden {{
            display: none;
            float: left;
            overflow: hidden;
            width: 0;
            max-height: 0;
            line-height: 0;
            mso-hide: all;
        }}

        .es-button-border:hover a.es-button, .es-button-border:hover button.es-button {{
            background: #ffffff !important;
        }}

        .es-button-border:hover {{
            background: #ffffff !important;
            border-style: solid solid solid solid !important;
            border-color: #3d5ca3 #3d5ca3 #3d5ca3 #3d5ca3 !important;
        }}

        @media only screen and (max-width: 600px) {{
            p, ul li, ol li, a {{
                line-height: 150% !important
            }}

            h1, h2, h3, h1 a, h2 a, h3 a {{
                line-height: 120% !important
            }}

            h1 {{
                font-size: 20px !important;
                text-align: center
            }}

            h2 {{
                font-size: 16px !important;
                text-align: left
            }}

            h3 {{
                font-size: 20px !important;
                text-align: center
            }}

            .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a {{
                font-size: 20px !important
            }}

            h2 a {{
                text-align: left
            }}

            .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a {{
                font-size: 16px !important
            }}

            .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a {{
                font-size: 20px !important
            }}

            .es-menu td a {{
                font-size: 14px !important
            }}

            .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a {{
                font-size: 10px !important
            }}

            .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a {{
                font-size: 16px !important
            }}

            .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a {{
                font-size: 12px !important
            }}

            .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a {{
                font-size: 12px !important
            }}

            *[class="gmail-fix"] {{
                display: none !important
            }}

            .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 {{
                text-align: center !important
            }}

            .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 {{
                text-align: right !important
            }}

            .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 {{
                text-align: left !important
            }}

            .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img {{
                display: inline !important
            }}

            .es-button-border {{
                display: block !important
            }}

            a.es-button, button.es-button {{
                font-size: 14px !important;
                display: block !important;
                border-left-width: 0px !important;
                border-right-width: 0px !important
            }}

            .es-btn-fw {{
                border-width: 10px 0px !important;
                text-align: center !important
            }}

            .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right {{
                width: 100% !important
            }}

            .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header {{
                width: 100% !important;
                max-width: 600px !important
            }}

            .es-adapt-td {{
                display: block !important;
                width: 100% !important
            }}

            .adapt-img {{
                width: 100% !important;
                height: auto !important
            }}

            .es-m-p0 {{
                padding: 0px !important
            }}

            .es-m-p0r {{
                padding-right: 0px !important
            }}

            .es-m-p0l {{
                padding-left: 0px !important
            }}

            .es-m-p0t {{
                padding-top: 0px !important
            }}

            .es-m-p0b {{
                padding-bottom: 0 !important
            }}

            .es-m-p20b {{
                padding-bottom: 20px !important
            }}

            .es-mobile-hidden, .es-hidden {{
                display: none !important
            }}

            tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden {{
                width: auto !important;
                overflow: visible !important;
                float: none !important;
                max-height: inherit !important;
                line-height: inherit !important
            }}

            tr.es-desk-hidden {{
                display: table-row !important
            }}

            table.es-desk-hidden {{
                display: table !important
            }}

            td.es-desk-menu-hidden {{
                display: table-cell !important
            }}

            .es-menu td {{
                width: 1% !important
            }}

            table.es-table-not-adapt, .esd-block-html table {{
                width: auto !important
            }}

            table.es-social {{
                display: inline-block !important
            }}

            table.es-social td {{
                display: inline-block !important
            }}

            .es-desk-hidden {{
                display: table-row !important;
                width: auto !important;
                overflow: visible !important;
                max-height: inherit !important
            }}
        }}
    </style>
</head>
<body style="width:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;padding:0;Margin:0">
<div class="es-wrapper-color" style="background-color:#FAFAFA"><!--[if gte mso 9]>
    <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
        <v:fill type="tile" color="#fafafa"></v:fill>
    </v:background>
    <![endif]-->
    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FAFAFA">
        <tr style="border-collapse:collapse">
            <td valign="top" style="padding:0;Margin:0">
                <table cellpadding="0" cellspacing="0" class="es-content" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                    <tr style="border-collapse:collapse">
                        <td class="es-adaptive" align="center" style="padding:0;Margin:0">
                            <table class="es-content-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td align="left" style="padding:10px;Margin:0">
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:580px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" class="es-infoblock" style="padding:0;Margin:0;line-height:14px;font-size:12px;color:#CCCCCC"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:14px;color:#CCCCCC;font-size:12px">
                                                                New Password Generated<br></p></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table cellpadding="0" cellspacing="0" class="es-header" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                    <tr style="border-collapse:collapse">
                        <td class="es-adaptive" align="center" style="padding:0;Margin:0">
                            <table class="es-header-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#3d5ca3;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="#3d5ca3" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px;background-color:#3d5ca3" bgcolor="#3d5ca3"
                                        align="left" data-darkreader-inline-bgcolor><!--[if mso]>
                                        <table style="width:560px" cellpadding="0"
                                               cellspacing="0">
                                            <tr>
                                                <td style="width:270px" valign="top"><![endif]-->
                                        <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                            <tr style="border-collapse:collapse">
                                                <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:270px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img"
                                                                                                                             src="https://gtsjso.stripocdn.email/content/guids/4e075778-246a-460a-8d8e-bf59fdb8e130/images/4236327659696_cb82d378cf545070c08c_132_1.png"
                                                                                                                             alt
                                                                                                                             style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                                                                             width="132"></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!--[if mso]></td>
                                                     <td style="width:20px"></td>
                                                     <td style="width:270px" valign="top"><![endif]-->
                                        <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                            <tr style="border-collapse:collapse">
                                                <td align="left" style="padding:0;Margin:0;width:270px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="left" style="padding:0;Margin:0"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:39px;color:#333333;font-size:26px">
                                                                <br></p>
                                                                <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:57px;color:#333333;font-size:38px">
                                                                    <strong>Baohule Casino</strong></p></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!--[if mso]></td></tr></table><![endif]--></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                    <tr style="border-collapse:collapse">
                        <td style="padding:0;Margin:0;background-color:#fafafa" bgcolor="#fafafa" align="center" data-darkreader-inline-bgcolor>
                            <table class="es-content-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#ffffff;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td style="padding:0;Margin:0;padding-left:20px;padding-right:20px;padding-top:40px;background-color:transparent;background-position:left top"
                                        bgcolor="transparent" align="left" data-darkreader-inline-bgcolor>
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                                                    <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:left top"
                                                           width="100%" cellspacing="0" cellpadding="0">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px;font-size:0"><img
                                                                    src="https://gtsjso.stripocdn.email/content/guids/CABINET_dd354a98a803b60e2f0411e893c82f56/images/23891556799905703.png"
                                                                    alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="175">
                                                            </td>
                                                        </tr>
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;padding-top:15px;padding-bottom:15px"><h1
                                                                    style="Margin:0;line-height:24px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:20px;font-style:normal;font-weight:normal;color:#333333"
                                                                    data-darkreader-inline-color><b>New Password</b></h1></td>
                                                        </tr>
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;padding-left:40px;padding-right:40px"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                HI, {name} </p></td>
                                                        </tr>
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;padding-right:35px;padding-left:40px"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                There was a&nbsp;change your password!</p></td>
                                                        </tr>
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="Margin:0;padding-left:10px;padding-right:10px;padding-top:40px;padding-bottom:40px"><span
                                                                    class="es-button-border"
                                                                    style="border-style:solid;border-color:#3D5CA3;background:#FFFFFF;border-width:2px;display:inline-block;border-radius:10px;width:auto;mso-border-alt:10px"><a
                                                                    href="" class="es-button" target="_blank"
                                                                    style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#3D5CA3;font-size:14px;display:inline-block;background:#FFFFFF;border-radius:10px;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-weight:bold;font-style:normal;line-height:17px;width:auto;text-align:center;padding:15px 20px 15px 20px">
                                                                    
                                                                    {password}
                                                                    
                                                                    </a></span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr style="border-collapse:collapse">
                                    <td style="padding:0;Margin:0;padding-left:10px;padding-right:10px;padding-top:20px;background-position:center center" align="left">
                                        <!--[if mso]>
                                        <table style="width:580px" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="width:199px" valign="top"><![endif]-->
                                        <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                            <tr style="border-collapse:collapse">
                                                <td align="left" style="padding:0;Margin:0;width:199px">
                                                    <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center center"
                                                           width="100%" cellspacing="0" cellpadding="0">
                                                        <tr style="border-collapse:collapse">
                                                            <td class="es-m-txt-c" align="right" style="padding:0;Margin:0;padding-top:15px"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:24px;color:#666666;font-size:16px"
                                                                    data-darkreader-inline-color><strong>Follow us:</strong></p></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!--[if mso]></td>
                                                     <td style="width:20px"></td>
                                                     <td style="width:361px" valign="top"><![endif]-->
                                        <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                            <tr style="border-collapse:collapse">
                                                <td align="left" style="padding:0;Margin:0;width:361px">
                                                    <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center center"
                                                           width="100%" cellspacing="0" cellpadding="0">
                                                        <tr style="border-collapse:collapse">
                                                            <td class="es-m-txt-c" align="left" style="padding:0;Margin:0;padding-bottom:5px;padding-top:10px;font-size:0">
                                                                <table class="es-table-not-adapt es-social" cellspacing="0" cellpadding="0"
                                                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                    <tr style="border-collapse:collapse">
                                                                        <td valign="top" align="center" style="padding:0;Margin:0;padding-right:10px"><img
                                                                                src="https://gtsjso.stripocdn.email/content/assets/img/social-icons/rounded-gray/facebook-rounded-gray.png"
                                                                                alt="Fb" title="Facebook" width="32"
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                        </td>
                                                                        <td valign="top" align="center" style="padding:0;Margin:0;padding-right:10px"><img
                                                                                src="https://gtsjso.stripocdn.email/content/assets/img/social-icons/rounded-gray/twitter-rounded-gray.png"
                                                                                alt="Tw" title="Twitter" width="32"
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                        </td>
                                                                        <td valign="top" align="center" style="padding:0;Margin:0;padding-right:10px"><img
                                                                                src="https://gtsjso.stripocdn.email/content/assets/img/social-icons/rounded-gray/instagram-rounded-gray.png"
                                                                                alt="Ig" title="Instagram" width="32"
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                        </td>
                                                                        <td valign="top" align="center" style="padding:0;Margin:0;padding-right:10px"><img
                                                                                src="https://gtsjso.stripocdn.email/content/assets/img/social-icons/rounded-gray/youtube-rounded-gray.png"
                                                                                alt="Yt" title="Youtube" width="32"
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                        </td>
                                                                        <td valign="top" align="center" style="padding:0;Margin:0;padding-right:10px"><img
                                                                                src="https://gtsjso.stripocdn.email/content/assets/img/social-icons/rounded-gray/linkedin-rounded-gray.png"
                                                                                alt="In" title="Linkedin" width="32"
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic">
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!--[if mso]></td></tr></table><![endif]--></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table class="es-footer" cellspacing="0" cellpadding="0" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                    <tr style="border-collapse:collapse">
                        <td style="padding:0;Margin:0;background-color:#fafafa" bgcolor="#fafafa" align="center" data-darkreader-inline-bgcolor>
                            <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" data-darkreader-inline-bgcolor
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                                <tr style="border-collapse:collapse">
                                    <td style="Margin:0;padding-top:10px;padding-left:20px;padding-right:20px;padding-bottom:30px;background-color:#0b5394;background-position:left top"
                                        bgcolor="#0b5394" align="left" data-darkreader-inline-bgcolor>
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="left" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><h2
                                                                    style="Margin:0;line-height:19px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:16px;font-style:normal;font-weight:normal;color:#ffffff"
                                                                    data-darkreader-inline-color><strong>Have quastions?</strong></h2></td>
                                                        </tr>
                                                        <tr style="border-collapse:collapse">
                                                            <td align="left" style="padding:0;Margin:0;padding-bottom:5px"><p
                                                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:21px;color:#ffffff;font-size:14px"
                                                                    data-darkreader-inline-color>We are here to help, learn more about us <a target="_blank"
                                                                                                                                             style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;color:#ffffff;font-size:14px"
                                                                                                                                             data-darkreader-inline-color href="">here</a>
                                                            </p>
                                                                <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:21px;color:#ffffff;font-size:14px"
                                                                   data-darkreader-inline-color>or <a target="_blank"
                                                                                                      style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;color:#ffffff;font-size:14px"
                                                                                                      data-darkreader-inline-color href="">contact us</a></p></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                    <tr style="border-collapse:collapse">
                        <td style="padding:0;Margin:0;background-color:#fafafa" bgcolor="#fafafa" align="center" data-darkreader-inline-bgcolor>
                            <table class="es-content-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="transparent" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td style="padding:0;Margin:0;padding-top:15px;background-position:left top" align="left">
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:600px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;padding-bottom:20px;padding-left:20px;padding-right:20px;font-size:0">
                                                                <table width="100%" height="100%" cellspacing="0" cellpadding="0" border="0"
                                                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                    <tr style="border-collapse:collapse">
                                                                        <td style="padding:0;Margin:0;border-bottom:1px solid #fafafa;background:none;height:1px;width:100%;margin:0px"
                                                                            data-darkreader-inline-border-bottom data-darkreader-inline-bgimage data-darkreader-inline-bgcolor></td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table class="es-footer" cellspacing="0" cellpadding="0" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                    <tr style="border-collapse:collapse">
                        <td style="padding:0;Margin:0;background-color:#fafafa" bgcolor="#fafafa" align="center" data-darkreader-inline-bgcolor>
                            <table class="es-footer-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="transparent" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td align="left" style="Margin:0;padding-bottom:5px;padding-top:15px;padding-left:20px;padding-right:20px">
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;display:none"></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                    <tr style="border-collapse:collapse">
                        <td align="center" style="padding:0;Margin:0">
                            <table class="es-content-body"
                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                                   cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" data-darkreader-inline-bgcolor>
                                <tr style="border-collapse:collapse">
                                    <td align="left" style="Margin:0;padding-left:20px;padding-right:20px;padding-top:30px;padding-bottom:30px">
                                        <table width="100%" cellspacing="0" cellpadding="0"
                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                            <tr style="border-collapse:collapse">
                                                <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                                                    <table width="100%" cellspacing="0" cellpadding="0"
                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                        <tr style="border-collapse:collapse">
                                                            <td align="center" style="padding:0;Margin:0;display:none"></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
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
</body>
</html>
"""
