#!/usr/bin/env python3.8

import unittest
import datetime


class Sum(unittest.TestCase):
    def test_sum(self):
        valor = 3

        self.assertEqual(valor, 3, "valor is not 3")
        pass


runner_test1 = unittest.TextTestRunner()
result_test_method1 = runner_test1.run(unittest.makeSuite(Sum))

with open("/media/disk_t/Projects/(220C2003) - (Telecom Smart Home System)/SW/04-ENG7 Software Integration/gitlab-ci/writing_test/Logs:test_app.txt", "w") as fp1:
    fp1.write("Test writing in file:\n")
    fp1.write("Date: " + str(datetime.datetime.now()) + "\n")
    fp1.write("Hello World.\n")
