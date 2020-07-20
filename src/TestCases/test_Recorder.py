from collections import deque
import unittest
import os
import io
import sys
import json

from Recorder import Recorder
from Recorder import WorkingListManager
from Recorder import JsonRecorder

class TestRecorder(unittest.TestCase):
    """The test case of the module `Recorder.Reocrder`.
    """
    def setUp(self):
        self.assertFalse(os.path.exists('tmp/testRecorder.txt')) # Record file not exists at the start of each test

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it.

        * Remove the record file after each test
        """
        # Remove the record file after each test
        if os.path.exists('tmp/testRecorder.txt'):
            os.remove('tmp/testRecorder.txt')

    def test_attributes(self):
        """Testing the attribute setting after initialization.
        """
        r = Recorder('testRecorder')
        self.assertEqual(r.name, 'testRecorder') # Recorder name variable correctness
        self.assertEqual(r.path, 'tmp/testRecorder.txt') # Recorder path variable correctness
        self.assertTrue(isinstance(r.records, list)) # Record list variable datatype correctness
        self.assertTrue(os.path.exists(r.path) and os.path.isfile(r.path)) # Record file existence
        with self.assertRaises(TypeError):
            Recorder([]) # Raising error if not initialize with a string

    def test_save(self):
        """Testing the saving method.
        """
        r = Recorder('testRecorder')
        r.save()
        self.assertTrue(os.path.exists(r.path) and os.path.isfile(r.path)) # Record file existence
        with open(r.path, 'r') as fin:
            self.assertFalse(fin.read()) # Record file content emptiness

    def test_recordWithoutAutoSave(self):
        """Testing the record adding method without auto saving.
        """
        newRecord = 'abc'
        r = Recorder('testRecorder')
        r.addRecord(newRecord, False)
        self.assertEqual(r.records, [newRecord]) # Record list correctness
        with open(r.path, 'r') as fin:
            self.assertFalse(fin.read()) # Record file content correctness

    def test_record(self):
        """Testing the record adding method.
        """
        newRecord = 'abc'
        r = Recorder('testRecorder')
        r.addRecord(newRecord)
        self.assertEqual(r.records, [newRecord]) # Record list correctness
        with open(r.path, 'r') as fin:
            self.assertEqual(fin.read(), 'abc') # Record file of correct data

    def test_recordsWithoutAutoSave(self):
        """Testing the mutiple records adding method without auto saving.
        """
        newRecords = ['abc', 'klm']
        r = Recorder('testRecorder')
        r.addRecords(newRecords, False)
        self.assertEqual(r.records, newRecords) # New records were added
        with open(r.path, 'r') as fin:
            self.assertFalse(fin.read()) # Record file content correctness

    def test_records(self):
        """Testing the mutiple record adding method.
        """
        newRecords = ['abc', 'klm']
        r = Recorder('testRecorder')
        r.addRecords(newRecords)

        self.assertEqual(r.records, newRecords) # Record list correctness
        self.assertTrue(os.path.exists(r.path) and os.path.isfile(r.path)) # Record file existence
        with open(r.path, 'r') as fin:
            self.assertEqual(fin.read(), 'abc\nklm') # Record file content correctness

    def test_recordWithoutAutoSaveAfterRecordAutoSave(self):
        """Testing the record adding method without auto saving after exercising an adding method with auto saving.
        """
        newRecord = 'abc'
        r = Recorder('testRecorder')
        r.addRecord(newRecord)
        self.assertEqual(r.records, ['abc']) # Record list correctness
        with open(r.path, 'r') as fin:
            self.assertEqual(fin.read(), 'abc') # Record file content correctness

        newRecord = 'klm'
        r.addRecord(newRecord, False)
        self.assertEqual(r.records, ['abc', 'klm']) # Record list correctness
        with open(r.path, 'r') as fin:
            txt = fin.read()
            self.assertEqual(txt, 'abc') # Record file remained unchanged
            self.assertNotEqual(txt, 'abc\nklm')

    def test_recordAutoSaveAfterRecordWithoutAutoSave(self):
        """Testing the record adding method after exercising an adding method without auto saving.
        """
        newRecord = 'abc'
        r = Recorder('testRecorder')
        r.addRecord(newRecord, False)
        self.assertEqual(r.records, [newRecord])
        with open(r.path, 'r') as fin:
            self.assertFalse(fin.read()) # Record file content correctness

        newRecord = 'klm'
        r.addRecord(newRecord)
        with open(r.path, 'r') as fin:
            txt = fin.read()
            self.assertNotEqual(txt, 'abc')
            self.assertEqual(txt, 'abc\nklm') # Newest record was saved together with the previous unsaved record

    def test_outputRecord(self):
        """Testing the method of converting the records into an output string.
        """
        newRecords = ['abc', 'klm']
        r = Recorder('testRecorder')
        r.addRecords(newRecords, False)
        self.assertEqual(r.outputRecord(), 'abc\nklm') # Output format correctness

    def test_recordExists(self):
        """Testing the method of checking the existence of record.
        """
        r = Recorder('testRecorder')
        self.assertFalse(r.recordExists()) # Record not exists at initial state

        newRecord = ['abc']
        r.addRecord(newRecord, False)
        self.assertTrue(r.recordExists()) # Record exists after adding a record

    def test_recordAmount(self):
        """Testing the method of checking the amount of record.
        """
        r = Recorder('testRecorder')
        self.assertEqual(r.recordAmount(), 0) # Record amount correctness of initial state

        newRecord = 'abc'
        r.addRecord(newRecord, False)
        self.assertEqual(r.recordAmount(), 1) # Record amount correctness after adding a record

        for i in range(10):
            r.addRecord(str(i), False)
        self.assertEqual(r.recordAmount(), 11) # Record amount correctness after adding a record for serveral times

        newRecords = ['aaa', 'bbb', 'ccc']
        r.addRecords(newRecords)
        self.assertEqual(r.recordAmount(), 14) # Record amount correctness after adding records

class TestWorkingListManager(unittest.TestCase):
    """The test case of the module `Recorder.WorkinListManager`.
    """
    def setUp(self):
        """Hook method for setting up the test fixture before exercising it.

        * Direct the standard output to a :obj:`stringIO` object.
        * Checking record files not exists before testing.
        """
        sys.stdout = self.strIO = io.StringIO() # Redirect the stdout

        # Checking record files not exists before testing
        self.assertFalse(os.path.exists('tmp/workingList.txt'))
        self.assertFalse(os.path.exists('tmp/done.txt'))

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it.

        * Redirecting the stdout.
        * Removing files created during testing
        """
        sys.stdout = sys.__stdout__ # Redirecting the stdout

        # Removing files created during testing
        if os.path.exists('tmp/workingList.txt'):
            os.remove('tmp/workingList.txt')        
        if os.path.exists('tmp/done.txt'):
            os.remove('tmp/done.txt')

    def test_attributes(self):
        """Testing the attribute setting after initialization.

        * Case 1: Default attributes.
        * Case 2: Initializing with a list.
        * Case 3: Initializing with a deque.
        * Case 4: Raising a TypeError if not initializing with a list or a deque.
        """
        # Test default attributes
        WLM = WorkingListManager()
        self.assertEqual(WLM.name, 'workingList')
        self.assertEqual(WLM.path, 'tmp/workingList.txt')
        self.assertEqual(WLM.donePath, 'tmp/done.txt')
        self.assertTrue(isinstance(WLM.records, deque))
        self.assertFalse(WLM.records) # Records deque is empty
        self.assertTrue(isinstance(WLM.done, list))

        # Test attributes of initializing with a list
        WLM = WorkingListManager(['aaa'])
        self.assertTrue(isinstance(WLM.records, deque) and WLM.records)
        self.assertEqual(WLM.records.pop(), 'aaa')

        # Test attributes of initializing with a deque
        WLM = WorkingListManager(deque(['bbb']))
        self.assertTrue(isinstance(WLM.records, deque) and WLM.records)
        self.assertEqual(WLM.records, deque(['bbb']))

        # Test raising a TypeError if not initializing with a list or a deque
        with self.assertRaises(TypeError):
            WorkingListManager('')

    def test_save(self):
        """Testing saving method.
        """
        # Testing auto saving after initialization
        WLM = WorkingListManager(['first work', 'second work'])
        self.assertTrue(os.path.exists(WLM.path) and os.path.isfile(WLM.path)) # Working list records exists
        with open(WLM.path) as fin:
            self.assertEqual(fin.read(), 'first work\nsecond work') # File correctness
        self.assertTrue(os.path.exists(WLM.donePath) and os.path.isfile(WLM.donePath)) # Done list exists
        with open(WLM.donePath) as fin:
            self.assertEqual(fin.read(), '') # File correctness

        # Testing auto saving after getting a work
        WLM.getWork()
        with open(WLM.path) as fin:
            self.assertEqual(fin.read(), 'second work')
        with open(WLM.donePath) as fin:
            self.assertEqual(fin.read(), 'first work')

        # Testing auto saving after getting a work
        WLM.getWork()
        with open(WLM.path) as fin:
            self.assertEqual(fin.read(), '')
        with open(WLM.donePath) as fin:
            self.assertEqual(fin.read(), 'first work\nsecond work')

    def test_addWork(self):
        """Testing method of adding a work.
        """
        newWork = 'abc'
        WLM = WorkingListManager()
        WLM.addWork(newWork)
        self.assertEqual(WLM.records, deque([newWork])) # Record list correctness 
        with open(WLM.path, 'r') as fin:
            self.assertEqual(fin.read(), 'abc') # File correctness of auto saving after adding a work
    
    def test_addWorks(self):
        """Testing method of adding multiple works.
        """
        newWorks = ['abc', 'klm']
        expectedRecords = deque(newWorks)
        expectedData = 'abc\nklm'

        WLM = WorkingListManager()
        WLM.addWorks(newWorks)

        self.assertEqual(WLM.records, expectedRecords) # Record list correctness 
        with open(WLM.path, 'r') as fin:
            self.assertEqual(fin.read(), expectedData) # File correctness of auto saving after adding a work
            
    def test_getWork(self):
        """Testing method of getting a work.
        """
        newWorks = ['abc', 'klm', 'rts']
        expectedWork = 'abc'
        expectedRecords = deque(['klm', 'rts'])
        expectedData = 'klm\nrts'

        WLM = WorkingListManager()
        WLM.addWorks(newWorks)
        work = WLM.getWork()

        self.assertEqual(work, expectedWork) # Returning data correctness
        self.assertEqual(WLM.records, expectedRecords) # Record list correctness
        with open(WLM.path, 'r') as fin:
            self.assertEqual(fin.read(), expectedData) # File correctness of auto saving after getting a work
            
    def test_workExists(self):
        """Testing method of checking the existence of work.
        """
        WLM = WorkingListManager()
        self.assertFalse(WLM.workExists()) # No record exists if initialize without working list
        newWork = 'abc'
        WLM.addWork(newWork)
        self.assertTrue(WLM.workExists()) # Record exists after append a recorder to the record list

    def test_remainedAmount(self):
        """Testing method of checking the amount of works.
        """
        WLM = WorkingListManager()
        self.assertEqual(WLM.remainedAmount(), 0) # Work amount correctness of initial state
        
        newWork = 'abc'        
        WLM.addWork(newWork)
        self.assertEqual(WLM.remainedAmount(), 1) # Work amount correctness after adding a work
        
        for i in range(10):
            WLM.addWork(str(i))
        self.assertEqual(WLM.remainedAmount(), 11) # Work amount correctness after adding a work for serveral times

        newRecords = ['aaa', 'bbb', 'ccc']
        WLM.addWorks(newRecords)
        self.assertEqual(WLM.remainedAmount(), 14) # Work amount correctness after adding works    

class TestJsonRecorder(unittest.TestCase):
    """The test case of the module `Recorder.JsonRecorder`.

    Attributes:

    * testName (:obj:`str`): The name used to build a ``JsonRecorder`` during the test.
    * testPath (:obj:`str`): The path assumed the record file created on.
    """
    
    testName = 'testRecorder'
    testPath = f'tmp/{testName}.json'

    def setUp(self):
        self.assertFalse(os.path.exists(self.testPath))# Checking record files not exists before testing


    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it.

        * Removing files created during testing
        """
        if os.path.exists(self.testPath):
            os.remove(self.testPath)

    def test_attributes(self):
        """Testing the attribute setting after initialization.        
        """
        jr = JsonRecorder('testRecorder')
        self.assertEqual(jr.name, 'testRecorder') # Json recorder name correctness
        self.assertEqual(jr.path, self.testPath) # Record file path correctness
        self.assertTrue(isinstance(jr.records, dict)) # Record variable datatype correctness
        self.assertFalse(jr.records) # Record is empty at initial state
        self.assertEqual(jr.count, 0) # Record counting variable is 0 at initial state
        self.assertTrue(os.path.exists(jr.path) and os.path.isfile(jr.path)) # Record file existence
        with open(jr.path, 'r') as fin:
            self.assertFalse(json.loads(fin.read())) # Record file content correctness

    def test_addRecord(self):
        """Testing the method of adding a record.
        """
        newRecord = {'a': '1', 'b': 3}
        expectedRecords = {'0': {'a': '1', 'b': 3}}
        
        jr = JsonRecorder('testRecorder')
        jr.addRecord(newRecord)

        self.assertEqual(jr.records, expectedRecords) # Record variable correctness after adding a record
        self.assertTrue(os.path.exists(jr.path) and os.path.isfile(jr.path)) # Record file existence        
        with open(jr.path, 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectedRecords) # Record file content correctness
        
        # Raising Type error if new record is not a dict
        with self.assertRaises(TypeError):
            jr.addRecord('')

    def test_outputRecord(self):
        """Testing the method of converting the records into an output string.
        """
        newRecords = [{'a': '1', 'b': 3}, {'a': '1', 'b': 3}]
        expectedData = ('{\n'
                        '    "0": {\n'
                        '        "a": "1",\n'
                        '        "b": 3\n'
                        '    },\n'
                        '    "1": {\n'
                        '        "a": "1",\n'
                        '        "b": 3\n'
                        '    }\n'
                        '}')
        expectedDict = {'0':{'a': '1', 'b': 3}, '1':{'a': '1', 'b': 3}}

        jr = JsonRecorder('testRecorder')
        jr.addRecords(newRecords, False)
        self.assertEqual(jr.outputRecord(), expectedData) # Record list output format correctness
        self.assertEqual(json.loads(jr.outputRecord()), expectedDict) # Record file content correctness

    def test_save(self):
        """Testing the method of saving the records.
        """
        newRecords = [{'a': '1', 'b': 3}, {'a': '1', 'b': 3}]
        expectedDict = {'0':{'a': '1', 'b': 3}, '1':{'a': '1', 'b': 3}}
        
        jr = JsonRecorder('testRecorder')
        jr.addRecords(newRecords)        
        self.assertTrue(os.path.exists(jr.path) and os.path.isfile(jr.path)) # Record file existence
        with open(jr.path, 'r') as fin:
            self.assertEqual(json.loads(fin.read()), expectedDict) # Record file content correctness

if __name__ == "__main__":
    unittest.main()