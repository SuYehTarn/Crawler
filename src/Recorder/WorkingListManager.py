from collections import deque

from .Recorder import Recorder

class WorkingListManager(Recorder):
    """The device to manage the adding and getting of works and to make a record.

    Attributes:

    * name (:obj:`str`): The name of the working list manager. The default name is ``wokingList``.
    * path (:obj:`str`): The file path of the working list.
    * records (:obj:`list`): The list of works.
    * done (:obj:`list`): The list of processed works.
    * donePath (:obj:`str`): The file path of the processed work list.

    Args:

    * workingList (:obj:`list`): A list of url string.

    Raise:

    * TypeError: The input argument is not a list or a deque of strings.
    """
    def __init__(self, workingList=None):
        self.donePath = 'tmp/done.txt'
        self.done = []
        
        super().__init__('workingList')        

        if workingList is None:
            workingList = deque()

        elif isinstance(workingList, deque):
            for elem in workingList:
                if not isinstance(elem, str):
                    raise TypeError('The elements in the working list must be strings.')

        elif isinstance(workingList, list):
            for elem in workingList:
                if not isinstance(elem, str):
                    raise TypeError('The elements in the working list must be strings.')
            else:
                workingList = deque(workingList)

        else:
            raise TypeError('Input working list must be a list or deque.')

        self.records = workingList
        self.save()

    def save(self):
        """The method of saving the working list and done list.
        """
        super().save()

        try:
            with open(self.donePath, 'wt') as fout:
                fout.write('\n'.join(self.done))

        except Exception as e:
            print(f'Failed to record on done.txt: {e}')

    def addRecord(self, newRecord, autoSave=True):
        """The method of adding a work as a new record. A record would not be added into the working list again if it has been added before.

        Args:

        * newRecord (:obj:`str`): A url string as a new work.
        * autoSave (:obj:`bool`): A boolean value handling auto saving. The default value is ``True``.
        """
        if newRecord in self.records:
            return
        
        if newRecord in self.done:
            return

        super().addRecord(newRecord)

    def addWork(self, work):
        """The method of adding a work into the working list.

        Args:

        * work (:obj:`str`): A url string as a new work.
        """
        self.addRecord(work)

    def addWorks(self, works):
        """The method of adding serveral works into the working list.

        Args:

        * works (:obj:`list`): A list of url strings as new works.
        """
        self.addRecords(works)

    def getWork(self):
        """The method of getting a work from the work list.

        Return:

        * work (:obj:`str`): The first element of the working list.
        """
        try:
            work = self.records.popleft()
            self.done.append(work)
            
        except IndexError:
            return None        
        
        self.save()
        
        return work

    def workExists(self):
        """The method of checking the existence of work in working list.

        Return:

        * :obj:`bool`: ``True`` if work exists in the working list, ``False`` otherwise.
        """
        return self.recordExists()

    def remainedAmount(self):
        """The method of getting the remained work amount.

        Return:

        * :obj:`int`: The amount of works in the working list.
        """
        return self.recordAmount()