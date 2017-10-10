# -*- coding: utf-8 -*-

from time import time
start_time = time()

from os import kill
from os import getpid
import signal
def bye(title = ''):
    # input("Press Enter to continue...")
    if title:
        import ctypes
        (a,b,c) = sys.exc_info()
        if b:
            ctypes.windll.user32.MessageBoxW(0, "{0}\n-----\n{1}".format(title,b), title, 0)
            # ctypes.windll.user32.MessageBoxW(0, "{0}\n{1}\n{2}".format(a,b,c), title, 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "{0}\n-----\nExiting".format(title), title, 0)
    kill(getpid(), signal.SIGTERM)

import                        fileinput
import                        requests
import                        sys
from os       import          path
from os       import          chdir
from sys      import          argv
from json     import dumps as dumpsJSON
from json     import load  as loadJSON
from json     import loads as loadsJSON
from sys      import path  as sysPath
from yaml     import load  as loadYAML
from datetime import datetime

if hasattr(sys, "frozen"):
    pass
else:
    import win_unicode_console
    win_unicode_console.enable()

from ShtrihM import ShtrihM
from PSPrint import PSPrint


BASEDIR = path.dirname(sys.executable) if hasattr(sys, "frozen") else path.dirname(__file__)


# Set plp_filename environment variable from passed argument
PLP_FILENAME = argv[1]

with open(PLP_FILENAME, 'r', encoding='utf-8') as plp_data_file:
    PLP_JSON_DATA = loadJSON(plp_data_file)
    # print(PLP_JSON_DATA['salesPointCountry'])


# with open(path.join(BASEDIR, 'package.json'), 'r') as package_json_file:
#     PACKAGE_JSON_DATA = loadJSON(package_json_file)

fbtmpl_fn = path.join(BASEDIR, 'config', 'feedbackTemplate.json')
with open(fbtmpl_fn, 'r', encoding='utf-8') as feedback_template_file:
    FEEDBACK_TEMPLATE = loadJSON(feedback_template_file)
    FEEDBACK_TEMPLATE['feedbackToken'] = PLP_JSON_DATA.get('feedbackToken')
    FEEDBACK_TEMPLATE['operationToken'] = PLP_JSON_DATA.get('operationToken')
    FEEDBACK_TEMPLATE['businessTransactionId'] = PLP_JSON_DATA.get('fiscalData', {'businessTransactionId':''}).get('businessTransactionId', '')
    FEEDBACK_TEMPLATE['operation'] = PLP_JSON_DATA.get('fiscalData').get('operation')


fblog_fn = path.join(BASEDIR, 'feedback.log')
def fb2log(line):
    with open(fblog_fn, 'a', encoding='utf-8') as feedback_log_file:
        feedback_log_file.write(datetime.now().isoformat() + ' ' + str(line) + '\n')


def feedback(feedback, success=True, reverse=None):
    FEEDBACK_TEMPLATE['status'] = success
    FEEDBACK_TEMPLATE['feedBackMessage'] = feedback.get('message')

    _fburl = PLP_JSON_DATA.get('feedbackUrl', PLP_JSON_DATA.get('feedBackurl'))
    # print('Sending "{0}" to "{1}"'.format(dumpsJSON(FEEDBACK_TEMPLATE, indent=4), _fburl))
    fb2log('Sending ' + feedback.get('message'))
    headers = {'Content-type': 'application/json'}
    r = requests.post(_fburl, allow_redirects=True, timeout=30, json=FEEDBACK_TEMPLATE, verify=False)
    fb2log('\\_ sent ok.')

    if r.status_code != requests.codes.ok:
        fb2log('Not Ok - (' + r.status_code + ')')
        if reverse:
            reverse()
        bye('{0}; status_code={1}'.format(r.headers['content-type'], r.status_code))

    try:
        response_json = r.json()
        # print('BO response: {0}'.format(dumpsJSON(response_json, indent=4)))
    except Exception as e:
        fb2log('Not Ok - Feedback failed, reversing operation')
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "Feedback failed", "Reversing operation", 0)
        # print(e)
        # print('BO response: {0}'.format(r.text))
        if reverse:
            reverse()
        bye()

    fb2log('Ok')


def noop():
    pass


def doFiscal():
    _amount = 0
    with ShtrihM(feedback, bye, PLP_JSON_DATA) as cm:
        operations_a = {
        'cut':          {'operation': cm.cut,              },
        'endshift':     {'operation': cm.closeShift,       },
        'feed':         {'operation': cm.feed,             },
        'insertcash':   {'operation': cm.insertCash,       'reverse': cm.withdrawCash},
        'opencashreg':  {'operation': cm.openCashRegister, },
        'refund':       {'operation': cm.cmsale,           'reverse': cm.reverseSale},
        'sale':         {'operation': cm.cmsale,           'reverse': cm.reverseSale},
        'startshift':   {'operation': noop                 },
        'withdrawcash': {'operation': cm.withdrawCash,     'reverse': cm.insertCash},
        'xreport':      {'operation': cm.xReport,          },
        }
        VALID_OPERATIONS = operations_a.keys()
        operation = PLP_JSON_DATA['fiscalData']['operation']
        if operation not in VALID_OPERATIONS:
            raise ValueError('"operation" must be one of {0} in plp file. Got {1} instead.'.format(VALID_OPERATIONS, operation))

        _amount = operations_a[operation]['operation']() or 0

    fiscal_reply_fn = path.join(BASEDIR, 'config', 'fiscal_reply.yaml')
    # fiscal_reply_ofn = path.join(BASEDIR, 'tmp.txt')
    with open(fiscal_reply_fn, 'r', encoding='utf-8') as fiscal_reply_file:
        FISCAL_REPLY = loadYAML(fiscal_reply_file)

    if _amount == 0:
        reply_message = FISCAL_REPLY[operation]['reply']
    else:
        reply_message = FISCAL_REPLY[operation]['exactReply'].format(_amount)

    # print('reply_message: {0}'.format(reply_message))
    feedback({'code': '0', 'message': reply_message}, success=True, reverse=operations_a[operation].get('reverse', None))
    # print('reply_message: {0}'.format(reply_message))


if ( 'fiscalData' in PLP_JSON_DATA
    and 'printerData' in PLP_JSON_DATA['fiscalData']
    and 'type' in PLP_JSON_DATA['fiscalData']['printerData']
    and PLP_JSON_DATA['fiscalData']['printerData']['type'] != '' ):
        try:
            doFiscal()
        except Exception as e:
            # print("Unexpected fiscal error: {0}".format(e), sys.exc_info())
            bye("Unexpected fiscal error: {0}".format(e))


if 'ticketData' in PLP_JSON_DATA:
    try:
        with PSPrint(feedback, bye, PLP_JSON_DATA) as ps:
            ps.printTickets()
    except Exception as e:
        # print("Unexpected printer error: {0}".format(e), sys.exc_info())
        bye("Unexpected printer error: {0}".format(e))

bye()
