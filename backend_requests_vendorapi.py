
import os, sys, requests
import io

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../_elements/'))
from xos import *
from xpd import *

from __utils import *

''' UPDATES EXISTING DATA WITH NEW API DATA '''

def update_state_values(states):

    states['requests']['tokens'] = {
        'vendor': os.environ['IEX_KEY'],
    }

    states['requests']['queues']['sector'] = [

        {
            'source': 'vendor',
            'label': 'attribute',
            'url': 'https://cloud.vendor.com/stable/sector/{}/chart/1m?token={}&format=csv',
            'cols_original': ['date', 'attA', 'attB', 'attC', 'attD', 'attE'],
            'cols_renamed': ['datetimes', 'attA', 'attB', 'attC', 'attD', 'attE'],
            # type (before update - loop over times, loop over dates)
        },
    ]

    vendorToken = states['requests']['tokens']['vendor']

    _urlFormated = states['requests']['queues']['profile'][1]['url'].format('{}', vendorToken)
    states['requests']['queues']['profile'][1]['url'] = _urlFormated

    return states

def request_context_data(div, context, subject):

    ''' organize request '''
    url = div['url'].format(subject, )
    cols_original = div['cols_original']
    cols_renamed = div['cols_renamed']
    headers = {
        'Content-Type': 'application/csv'
    }

    ''' execute request '''
    print('\n\t. executing request')
    df_new = None
    if (context == 'sector'):

        try:

            # get response
            response = requests.request('GET', url, headers=headers)

            # decode response
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

            # handle missing columns
            for _c in cols_original:
                if not _c in df.columns:
                    print('column `{}` not found, will be set as empty'.format(_c))
                    df[_c] = np.nan

            # rename columns
            df_new = pd.DataFrame(df[cols_original].values, columns=cols_renamed).copy()

        except:
            print('\n\t\t. ERROR OCCURRED')

    return df_new

def x(states, p, context):

    ''' load '''
    states = update_state_values(states)
    df_exist = load_div_data(states, 'source', context=context)
    outline = states['requests']['queues'][context]

    ''' request data '''
    print('\n# `{}` ({}):`'.format(p, context))
    print('\n. executing request for {}...'.format(p))

    ''' request from multiple sources '''
    df_updated = None
    for context_requestBlock in outline:

        df_new = None
        df_received = request_context_data(context_requestBlock, context, p)

        if ((context == 'sector')
            or (context == 'timeEvents')):
            df_updated = update_existing_df(df_exist, df_received)

    ''' save '''
    save_div_data(states, 'source', df_updated, context=context)

    print('... requests complete.')
    return


