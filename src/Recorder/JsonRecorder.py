import json
import os

from .Recorder import Recorder

class JsonRecorder(Recorder):
    """The device to record data into a :obj:`.json` file.

    Attributes:

    * name (:obj:`str`): The name of the json reocrder.
    * path (:obj:`str`): The path of the record file. It has the format ``tmp/{recorderName}.json``. The direction ``./tmp`` would be created at the initialization if it is not exists.
    * records (:obj:`list`): The dict containing the records.
    * count (:obj:`int`): The number of adding records. It auto increases each time adding a record. Each number would be the key of each record.

    Args:

    * name (:obj:`str`): The name of the json recorder.

    Raise:

    * TypeError: The input name argument is not a string.
    """
    def __init__(self, name):
        """The initial method of a json recorder.
        """
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        self.name = name
        self.path = f'tmp/{self.name}.json'
        self.records = {}
        self.count = 0
        self.save()

    def outputRecord(self):
        """The method of converting the :obj:`dict` of records into a json format string.

        Return:

        * :obj:`str`: The string converted from the :obj:`dict` of records.
        """
        return json.dumps(self.records, ensure_ascii=False, indent=4)

    def addRecord(self, newRecord, autoSave=True):
        """The method of adding a new record. The new record must be a :obj:`dict`.

        Raise:

        * TypeError: The new record is not a :obj:`dict`.
        """
        if not isinstance(newRecord, dict):
            raise TypeError('Record must be a dict')
            
        self.records[str(self.count)] = newRecord
        self.count += 1

        if autoSave:
            self.save()