import os

class Recorder:
    """The device to record data into a file. The records are saved as a plain text file. The name of the record file is the same as the name of the recorder.

    Attributes:

    * name (:obj:`str`): The name of the recorder.
    * path (:obj:`str`): The path of the record file. It has the format ``tmp/{recorderName}.txt``. The direction ``./tmp`` would be created at the initialization if it is not exists.
    * records (:obj:`list`): The list of records.

    Args:

    * name (:obj:`str`): The name of the recorder.

    Raise:

    * TypeError: The input name argument is not a string.
    """
    def __init__(self, name):
        """The initial method of the :obj:`Recorder`.
        """
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        self.name = name
        self.path = f'tmp/{self.name}.txt'
        self.records = []

        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        
        self.save()

    def save(self):
        """The method of saving the records as a file.
        """
        try:
            with open(self.path, 'wt') as fout:
                fout.write(self.outputRecord())                

        except Exception as e:
            print(f'Failed to record on {self.path}\n{e}')

    def outputRecord(self):
        """The method of formatting the records as a string to write into a file. It would convert each record into a string presentation, and join all record with ``'\\n'``.

        Return:

        :obj:`str`: The ``'\\n'`` joined string presentation of all records.
        """
        strings = [str(elem) for elem in self.records]
        return '\n'.join(strings)

    def addRecord(self, newRecord, autoSave=True):
        """The method of adding a new record. A new record would be added into the list ``records``, and auto saving the records if the ``autoSave`` argument is set ``True``.

        Args:

        * newRecord (:obj:`object`): The new record with any data type.
        * autoSave (:obj:`bool`): Handle of auto saving.
        """
        self.records.append(newRecord)

        if autoSave:
            self.save()

    def addRecords(self, newRecords, autoSave=True):
        """The method of adding serveral new records.

        Args:

        * newRecords (:obj:`list`): The :obj:`list` contains new records with any data type.
        * autoSave (:obj:`bool`): Handle of auto saving.
        """
        for r in newRecords:
            self.addRecord(r, False)
        
        if autoSave:
            self.save()

    def recordExists(self):
        """The method of checking whether any record exists or not.

        Return:

        * :obj:`bool`: ``True`` if there exists any record, False otherwise.
        """
        return bool(self.records)

    def recordAmount(self):
        """The method of checking the length of the record list.

        Return:

        * :obj:`int`: The length of the record list.
        """
        return len(self.records)