# -*- coding: utf-8 -*-

from os import kill
from os import getpid
import signal

import requests
import sys
from os import path
from sys import argv
from json import load as loadJSON
from datetime import datetime
# from yaml import load as loadYAML
# from time import time
# import fileinput
# from os import chdir
# from json import dumps as dumpsJSON
# from json import loads as loadsJSON
# from sys import path as sysPath

# start_time = time()


def bye(title=''):
    # input("Press Enter to continue...")
    if title:
        import ctypes
        (a, b, c) = sys.exc_info()
        if b:
            ctypes.windll.user32.MessageBoxW(
                0, "{0}\n-----\n{1}".format(title, b), title, 0)
            # ctypes.windll.user32.MessageBoxW(
            #     0, "{0}\n{1}\n{2}".format(a,b,c), title, 0)
        else:
            ctypes.windll.user32.MessageBoxW(
                0, "{0}\n-----\nExiting".format(title), title, 0)
    kill(getpid(), signal.SIGTERM)


BASEDIR = ''
PLP_JSON_DATA = {}
FEEDBACK_TEMPLATE = {}


def init():
    if hasattr(sys, "frozen"):
        pass
    else:
        import win_unicode_console
        win_unicode_console.enable()

    global BASEDIR
    global PLP_JSON_DATA
    global FEEDBACK_TEMPLATE

    BASEDIR = path.dirname(sys.executable) if hasattr(sys, "frozen")\
        else path.dirname(__file__)

    PLP_FILENAME = argv[1]
    with open(PLP_FILENAME, 'r', encoding='utf-8') as plp_data_file:
        PLP_JSON_DATA = loadJSON(plp_data_file)

# with open(path.join(BASEDIR, 'package.json'), 'r') as package_json_file:
#     global PACKAGE_JSON_DATA
#     PACKAGE_JSON_DATA = loadJSON(package_json_file)

    fbtmpl_fn = path.join(BASEDIR, 'config', 'feedbackTemplate.json')
    with open(fbtmpl_fn, 'r', encoding='utf-8') as feedback_template_file:
        FEEDBACK_TEMPLATE = loadJSON(feedback_template_file)
        FEEDBACK_TEMPLATE['feedbackToken'] = PLP_JSON_DATA.get('feedbackToken')
        FEEDBACK_TEMPLATE['operationToken'] = PLP_JSON_DATA\
            .get('operationToken')
        FEEDBACK_TEMPLATE['businessTransactionId'] = PLP_JSON_DATA\
            .get('fiscalData', {'businessTransactionId': ''})\
            .get('businessTransactionId', '')
        FEEDBACK_TEMPLATE['operation'] = PLP_JSON_DATA\
            .get('fiscalData').get('operation')

    print('Initialized')


def fb2log(line):
    fblog_fn = path.join(BASEDIR, 'feedback.log')
    with open(fblog_fn, 'a', encoding='utf-8') as feedback_log_file:
        feedback_log_file\
            .write(datetime.now().isoformat() + ' ' + str(line) + '\n')


def feedback(feedback, success=True, reverse=None):
    FEEDBACK_TEMPLATE['status'] = success
    FEEDBACK_TEMPLATE['feedBackMessage'] = feedback.get('message')

    _fburl = PLP_JSON_DATA.get('feedbackUrl', PLP_JSON_DATA.get('feedBackurl'))
    fb2log('Sending ' + feedback.get('message'))
    # headers = {'Content-type': 'application/json'}
    r = requests.post(
        _fburl,
        allow_redirects=True,
        timeout=30,
        json=FEEDBACK_TEMPLATE,
        verify=False)
    fb2log('\\_ sent ok.')

    if r.status_code != requests.codes.ok:
        fb2log('Not Ok - (' + r.status_code + ')')
        if reverse:
            reverse()
        bye('{0}; status_code={1}'
            .format(r.headers['content-type'], r.status_code))

    try:
        response_json = r.json()
        # print('BO response: {0}'.format(dumpsJSON(response_json, indent=4)))
    except Exception as e:
        fb2log('Not Ok - Feedback failed, reversing operation')
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "Feedback failed",
                                         "Reversing operation", 0)
        # print(e)
        # print('BO response: {0}'.format(r.text))
        if reverse:
            reverse()
        bye()

    fb2log(response_json)


def noop():
    pass


def cmsale():
    card_payment_amount = 0
    for payment in PLP_JSON_DATA['fiscalData']['payments']:
        if payment['type'] == '4':
            card_payment_amount += payment['cost']

    if card_payment_amount == 0:
        return 0

    cpuSettings = \
        PLP_JSON_DATA.get('fiscalData', {}).get('cardPaymentUnitSettings', {})

    if not cpuSettings['cardPaymentUnitXml'] == 'PosXML 7.2.0':
        return 0

    from PosXML import PosXML
    posxmlIP = cpuSettings['cardPaymentUnitIp']
    posxmlPort = cpuSettings['cardPaymentUnitPort']
    with PosXML(
        feedback, bye,
        {'url': 'http://{0}:{1}'.format(posxmlIP, posxmlPort)}
    ) as posxml:
        posxml.post('CancelAllOperationsRequest', '')
        if PLP_JSON_DATA['fiscalData']['operation'] == 'sale':
            _transactionRequest = 'TransactionRequest'
        else:
            _transactionRequest = 'ReverseTransactionRequest'

        if PLP_JSON_DATA['fiscalData']['operation'] == 'sale':
            _transactionIdField = 'businessTransactionId'
        else:
            _transactionIdField = 'saleTransactionId'

        _transactionId = PLP_JSON_DATA['fiscalData'][_transactionIdField]
        response = posxml.post(
            _transactionRequest,
            {
                'TransactionID': _transactionId,
                'Amount': int(round(card_payment_amount * 100)),
                'CurrencyName': 'EUR',
                'PrintReceipt': 1,
                'ReturnReceipts': 64,
                'Timeout': 100,
            }
        )
        # print('response', response)
        if response['ReturnCode'] != '0':
            feedback({
                'code': response['ReturnCode'],
                'message': 'Card payment: {0}'.format(response['Reason'])
            }, False)
            bye()


init()

# if PLP_JSON_DATA.get('fiscalData', {}).get('payments', []):
#     try:
#         cmsale()
#     except Exception as e:
#         bye("Unexpected fiscal error: {0}".format(e))
#     print('Sold')

if PLP_JSON_DATA.get('ticketData', {}):
    print('Printing')
    try:
        from PSPrint import PSPrint
        with PSPrint(feedback, bye, PLP_JSON_DATA) as ps:
            ps.printTickets()
    except Exception as e:
        bye("Unexpected printer error: {0}".format(e))
    print('Printed')

bye()
