# -*- coding: utf-8 -*-
"""
.. module:: Extractor
   :synopsis: This module contains the Extractor.

.. moduleauthor:: Su, Yeh-Tarn

"""

from Recorder import JsonRecorder


class Extractor:
    """The web page data extracting device for the :obj:`Crawler`. User has to create a new extractor inheriting this class, and define the extracting method. Please read the example below.

    Attributes:

    * JesonRecorder (:obj:`JsonRecorder`): The json recorder recording the data into a json file.

    Args:

    * name (:obj:`str`): The name of the extractor.

    Example::

        class myExtractor(Extractor):

            def get_url(self, url, bs):     # The input arguments of an extracting method must include the url and bs.
                data = url                  # User can defined the method of extracting specific data.
                msg  = ''                   # User can defined the additional returning information or remained as an empty string.
                return data, msg            # User can ignore to control the possible exceptions, the ``Extractor.get`` decorator would pass and inform if an exception occurs.

            def get_title(self, url, bs):
                data = bs.head
                data = data.title.get_text()      # The method could be multiple lines
                msg  = ''
                return data, msg
    """
    def __init__(self, name):
        """The initial method of an Extractor.
        """
        self.name = name
        self.JsonRecorder = JsonRecorder(name)

    def get(self, extractFunc):
        """The decorator to decorate user-defined extracting method. It would wrap the input method with a ``try...except`` structure, and return the attempted data and message. If no exception raised, the return message would combine the returned message of the input method and the default message, which has a format ``Get {attribute name}: {data}``, with a ``'\\n'``.

        Args:

        * extractFunc (:obj:`method`): The user-defined extracting method.

        Return:

        * :obj:`method`: The decorated method if the argument is a method.
        * :obj:`None`: None if the argument is not a method.
        """

        if not callable(extractFunc):
            return None
            
        def get_attr(*args, **kwargs):
        
            attrName  = extractFunc.__name__[4:]
            data, msg = '', ''
            
            try:
                data, msg = extractFunc(*args, **kwargs)
                msg = f'{msg}\nGet {attrName}: {data}' if msg else f'Get {attrName}: {data}'
        
            except Exception as e:
                msg = f'Failed to get {attrName}: {e}'

            return data, msg
            
        return get_attr

    def extract(self, url, bs):
        """The method of running all the extractor's extracting method, which has a name starting with ``get_``. After extracting all attempted data, each attribute name and extracted data would become a key-value pair and consist a dict. The dict would be added as a record into the json recorder and be written into the record file.

        Args:

        * url (:obj:`str`): The url string of the web page.
        * bs (:obj:`BeautifulSoup`): The :obj:`BeautifulSoup` object of the web page.

        Return:

        * :obj:`str`: The messages returned from each data extracting method joined with ``'\\n'``.
        """

        jsonSerializablTypes = [dict, list, tuple, str, int, float, bool, type(None)]
        dataset, msgs = {}, []

        for func in (getattr(self, funcName) for funcName in dir(self) if funcName.startswith('get_')):
            attr = func.__name__[4:]

            try:
                data, msg = self.get(func)(url, bs)

                if type(data) not in jsonSerializablTypes:
                    data = str(data)        # If the returned data is not json serializable, convert it into a string.

                dataset[attr] = data
                msgs.append(msg)

            except Exception as e:
                msgs.append(f'Failed to run the extracting method {attr} of extractor {self.name}: {e}')
        
        self.JsonRecorder.addRecord(dataset)

        return '\n'.join(msgs)