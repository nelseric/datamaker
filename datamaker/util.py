""" Utility functions """

import numpy.lib
import numpy as np
import pandas as pd
import cPickle as pickle

#pylint: disable=maybe-no-member

def save_pandas(fname, data):
    '''Save DataFrame or Series

    Parameters
    ----------
    fname : str
        filename to use
    data: Pandas DataFrame or Series
    '''
    np.save(open(fname, 'w'), data)
    if len(data.shape) == 2:
        meta = data.index, data.columns
    elif len(data.shape) == 1:
        meta = (data.index,)
    else:
        raise ValueError('save_pandas: Cannot save this type')
    encoded_meta = pickle.dumps(meta)
    encoded_meta = encoded_meta.encode('string_escape')
    with open(fname, 'a') as df_file:
        df_file.seek(0, 2)
        df_file.write(encoded_meta)


def load_pandas(fname, mmap_mode='r'):
    '''Load DataFrame or Series

    Parameters
    ----------
    fname : str
        filename
    mmap_mode : str, optional
        Same as numpy.load option
    '''
    values = np.load(fname, mmap_mode=mmap_mode)
    with open(fname) as df_file:
        numpy.lib.format.read_magic(df_file)
        numpy.lib.format.read_array_header_1_0(df_file)
        df_file.seek(values.dtype.alignment * values.size, 1)
        meta = pickle.loads(df_file.readline().decode('string_escape'))
    if len(meta) == 2:
        return pd.DataFrame(values, index=meta[0], columns=meta[1])
    elif len(meta) == 1:
        return pd.Series(values, index=meta[0])
