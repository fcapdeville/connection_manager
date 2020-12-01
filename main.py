#!/usr/bin/env python3.8

# This is the test program for the connection_manager

# Every functions that I will use here are in the connection_manager program.
# I will use their methods and look their signals

#######################################################
# Methods used:
# 1_ NewRouter (string interface, int ip) ==> ()
# Will not be tested over x86.

# 2_ QueryByType (uint32 type) ==> (boolean reachable, string interface, string ip, uint32 port)
# The indication depends on reachable:
#       0 = unknown, 1 = backend, 2 = video, 3 = www
#######################################################

#######################################################
# Signals used:
# 1_ NewReachableServer (uint32, string, string, uint32)
# Indicates the same like QueryByType Method (instead of the boolean, which is omitted).

# 2_ LostReachableServer (uint32)
# Indicates a server loss.
#######################################################

import dbus
import unittest
import datetime
import socket
import time
import json

# The interface, bus and object used in this project
interface_string = "ar.mirgor.Smarthome.ConnectionManager"
bus_name_string = "ar.mirgor.Smarthome.ConnectionManager"
object_string = "/ar/mirgor/Smarthome/ConnectionManager"
# Indicates bus, object and interface
try:
    bus = dbus.SessionBus()  # Bus
    object_path = bus.get_object(bus_name_string, object_string)  # Object
    interface = dbus.Interface(object_path, interface_string)  # Interface
    flag_error = 0
except dbus.DBusException as e1:
    print(e1)
    print("\n&&Fatal error. There is no connection_manager active in this test.")
    flag_error = 1


query_backend = (0, "problem", "problem", 0)         # Define global variables
to_test_1 = 1                                        # Define global variables
server_opened = False                                # Define global variables
backend_info = 2                                     # Define global variables
number_backend = 0                                   # Define global variables
backend_validation = False                           # Define global variables
backend_exceptions = []                              # Define global variable


# Class method 1 to test
class Method1(unittest.TestCase):
    def test_QueryByType_1(self):
        global to_test_1                      # Define global variable
        global query_backend                  # Define global variable
        global server_opened                  # Define global variable
        global backend_info                   # Define global variable
        global number_backend                 # Define global variable
        global backend_validation             # Define global variable
        global backend_exceptions             # Define global variable

# Obtain from config.json the possibles ip and port
        with open("config.json", "r") as read_json:
            json_info = json.load(read_json)                    # Read the file
            if json_info['servers'][0]['type'] == 'backend':
                backend_info = json_info['servers'][0]['ip_port']
            else:
                if json_info['servers'][1]['type'] == 'video':
                    backend_info = json_info['servers'][1]['ip_port']
# In backend_info there is every possible ip & port
        for number_backend in range(0, len(backend_info)):
# Create server in background
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Creates a TCP/IP socket
                server_address = (backend_info[number_backend]['ip'], backend_info[number_backend]['port'])
                sock.bind(server_address)
                sock.listen()
                print("&&Server ip: " + backend_info[number_backend]['ip'] + " port: " +
                      str(backend_info[number_backend]['port']) + " was created.")
                time.sleep(100)                                                      # Delay for the connection_manager
                server_opened = True
            except dbus.DBusException as e2:
                print(e2)
                print("&&Cannot create server " + backend_info[number_backend]['ip'] + ":"
                      + str(backend_info[number_backend]['port']))
                server_opened = False

# ----------------------------------------------------------------------------------------

# Use QueryByType(1)
            print("&&First test: QueryByType(" + str(to_test_1)
                  + ") //backend")
            try:
                query_backend = interface.QueryByType(1)
                print(query_backend)
            # backend
            # True/False
            # interface: 'wlp0s20f3'
            # ip: 192.168.0.52
            # port: 45000 (is the port assigned in the ./tcp_server execution
            except dbus.DBusException as e3:
                print(e3)
                print("\n&&Failure in method 'QueryByType' sending a " + str(to_test_1))

# ----------------------------------------------------------------------------------------

# Kill server in background
            if server_opened:
                try:
                    print("Server killed.\n\n\n")
                    sock.close()
                    backend_validation = True
                except dbus.DBusException as e4:
                    print(e4)
                    print("&&Cannot kill server " + backend_info[number_backend]['ip'] + ":"
                          + str(backend_info[number_backend]['port']))

# Print information in docker screen and log_file
            self.assertEqual(flag_error, 0, "&&There is no connection_manager opened")
            self.assertEqual(query_backend[0], True, "&&The backend services are not reachable")
            try:
                self.assertEqual(server_opened, True, "&&The server " +
                                 backend_info[number_backend]['ip'] + ":" + str(backend_info[number_backend]['port'])
                                 + " was not created.")
            except dbus.DBusException as e5:
                print(e5)
                backend_exceptions.append(number_backend)
    pass


to_test_2 = 2                                         # Define global variables
query_video = (0, "problem", "problem", 0)            # Define global variables
video_opened = False                                  # Define global variables
video_info = 2                                        # Define global variables
number_video = 0                                      # Define global variables
video_validation = False                              # Define global variables
video_exceptions = []                                 # Define global variable


# Class method 2 to test
class Method2(unittest.TestCase):
    def test_QueryByType_2(self):
        global to_test_2                   # Define global variable
        global query_video                 # Define global variable
        global video_opened                # Define global variable
        global video_info                  # Define global variable
        global number_video                # Define global variable
        global video_validation            # Define global variable
        global video_exceptions            # Define global variable

# Obtain from config.json the possibles ip and port
        with open("config.json", "r") as read_json:
            json_info = json.load(read_json)                    # Read the file
            if json_info['servers'][0]['type'] == 'video':
                video_info = json_info['servers'][0]['ip_port']
            else:
                if json_info['servers'][1]['type'] == 'video':
                    video_info = json_info['servers'][1]['ip_port']
# In video_info there is every possible ip & port
        for number_video in range(0, len(video_info)):
# Create server in background
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Creates a TCP/IP socket
                server_address = (video_info[number_video]['ip'], video_info[number_video]['port'])
                sock.bind(server_address)
                sock.listen()
                print("&&Server ip: " + video_info[number_video]['ip'] + " port: " +
                      str(video_info[number_video]['port']) + " was created.")
                time.sleep(100)                                                      # Delay for the connection_manager
                video_opened = True
            except dbus.DBusException as e6:
                print(e6)
                print("&&Cannot create server " + video_info[number_video]['ip'] + ":"
                      + str(video_info[number_video]['port']))
                video_opened = False

# ----------------------------------------------------------------------------------------

# Use QueryByType(2)
            print("&&Second test: QueryByType(" + str(to_test_2)
                  + ") //video")
            try:
                query_video = interface.QueryByType(2)
                print(query_video)
            # video
            # True/False
            # interface: 'wlp0s20f3'
            # ip: 192.168.0.52
            # port: 45000 (is the port assigned in the ./tcp_server execution)
            except dbus.DBusException as e7:
                print(e7)
                print("\n&&Failure in method 'QueryByType' sending a " + str(to_test_2))

# ----------------------------------------------------------------------------------------

# Kill server in background
            if video_opened:
                try:
                    sock.close()
                    video_validation = True
                except dbus.DBusException as e8:
                    print(e8)
                    print("&&Cannot kill server " + video_info[number_video]['ip'] + ":"
                          + str(video_info[number_video]['port']))

# Print information in docker screen and log_file
            self.assertEqual(flag_error, 0, "&&There is no connection_manager opened")
            self.assertEqual(query_video[0], True, "&&The video services are not reachable")
            try:
                self.assertEqual(video_opened, True, "&&The server " +
                                 video_info[number_video]['ip'] + ":" + str(video_info[number_video]['port'])
                                 + " was not created.")
            except dbus.DBusException as e9:
                print(e9)
                video_exceptions.append(number_video)
            pass


query_www = (0, "problem", "problem", 0)         # Define global variables
to_test_3 = 3                                    # Define global variables


# Call method 3 to test
class Method3(unittest.TestCase):
    def test_QueryByType_3(self):
        global to_test_3         # Define global variable
        global query_www         # Define global variable
        print("\n&&Third test: QueryByType(" + str(to_test_3)
              + ") //www")
        try:
            query_www = interface.QueryByType(3)
            print(query_www)
        # www
        # True/False
        # ip: 216.58.202.36
        # port: 80
        # (if there is no modification to the config.json)
        # At logs, this will automatically take the information given by the config.json
        # so, there is no problem if this is modified
        except dbus.DBusException as e10:
            print(e10)
            print("\n&&Failure in method 'QueryByType' sending a " + str(to_test_3))

        # Print information in docker screen and log_file
        self.assertEqual(flag_error, 0, "&&There is no connection_manager opened")
        self.assertEqual(query_www[0], True, "&&The www is not reachable")
        pass


query_double_1 = (0, "problem", "problem", 0)            # Define global variables
query_double_2 = (0, "problem", "problem", 0)            # Define global variables
double_opened_1 = False                                  # Define global variables
double_opened_2 = False                                  # Define global variables
double_info = 2                                          # Define global variables
double_validation_1 = False                              # Define global variables
double_validation_2 = False                              # Define global variables


# Call method 4 to test
class Method4(unittest.TestCase):
    def test_QueryByType_4(self):
        global query_double_1                            # Define global variable
        global query_double_2                            # Define global variable
        global double_opened_1                           # Define global variable
        global double_opened_2                           # Define global variable
        global double_info                               # Define global variable
        global double_validation_1                       # Define global variable
        global double_validation_2                       # Define global variable

# Obtain from config.json the possibles ip and port
        with open("config.json", "r") as read_json:
            json_info = json.load(read_json)  # Read the file
            if json_info['servers'][0]['type'] == 'video':
                double_info = json_info['servers'][0]['ip_port']
            else:
                if json_info['servers'][1]['type'] == 'video':
                    double_info = json_info['servers'][1]['ip_port']
# In video_info there is every possible ip & port
# Create first server in background
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Creates a TCP/IP socket
            server_address = (double_info[0]['ip'], double_info[0]['port'])     # Creates server in the first option
            sock.bind(server_address)
            sock.listen()
            print("&&Server ip: " + double_info[0]['ip'] + " port: " +
                  str(double_info[0]['port']) + " was created.")
            time.sleep(100)  # Delay for the connection_manager
            double_opened_1 = True
        except dbus.DBusException as e11:
            print(e11)
            print("&&Cannot create server " + double_info[0]['ip'] + ":"
                  + str(double_info[0]['port']))
            double_opened_1 = False

# ----------------------------------------------------------------------------------------

# Create second server in background
        try:
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Creates a TCP/IP socket
            server_address = (double_info[1]['ip'], double_info[1]['port'])     # Creates server in the first option
            sock2.bind(server_address)
            sock2.listen()
            print("&&Server ip: " + double_info[1]['ip'] + " port: " +
                  str(double_info[1]['port']) + " was created.")
            time.sleep(1)                                                      # Delay for the connection_manager
            double_opened_2 = True
        except dbus.DBusException as e12:
            print(e12)
            print("&&Cannot create server " + double_info[1]['ip'] + ":"
                  + str(double_info[1]['port']))
            double_opened_2 = False

# ----------------------------------------------------------------------------------------

# Use QueryByType(2)
        print("&&Fifth test: QueryByType(" + str(to_test_2)
              + ") //video")
        try:
            query_double_1 = interface.QueryByType(2)
            print(query_double_1)
        # Information added as an example (could not be this exactly information)
        # video
        # True/False
        # interface: 'wlp0s20f3'
        # ip: 192.168.0.52
        # port: 45000 (is the port assigned in the ./tcp_server execution)
        except dbus.DBusException as e13:
            print(e13)
            print("\n&&Failure in method 'QueryByType' sending a " + str(to_test_2))

# ----------------------------------------------------------------------------------------

# Kill server in background
        if double_opened_1:
            try:
                sock.close()
                double_validation_1 = True
                print("Server killed.")
            except dbus.DBusException as e14:
                print(e14)
                print("&&Cannot kill server " + double_info[0]['ip'] + ":"
                      + str(double_info[0]['port']))

# ----------------------------------------------------------------------------------------

# Print information in docker screen and log_file
        self.assertEqual(flag_error, 0, "&&There is no connection_manager opened")
        self.assertEqual(query_double_1[0], True, "&&The video services are not reachable")
        try:
            self.assertEqual(double_opened_1, True, "&&The server " +
                             double_info[0]['ip'] + ":" + str(double_info[0]['port'])
                             + " was not created.")
        except dbus.DBusException as e15:
            print(e15)
            print("A server was not created. The program continue to the next one.\n")

# ----------------------------------------------------------------------------------------

        # Use QueryByType(2)
        print("&&Fifth test: QueryByType(" + str(to_test_2)
              + ") //video")
        try:
            query_double_2 = interface.QueryByType(2)
            print(query_double_2)
        # Information added as an example (could not be this exactly information)
        # video
        # True/False
        # interface: 'wlp0s20f3'
        # ip: 192.168.0.52
        # port: 45000 (is the port assigned in the ./tcp_server execution)
        except dbus.DBusException as e16:
            print(e16)
            print("\n&&Failure in method 'QueryByType' sending a " + str(to_test_2))

# ----------------------------------------------------------------------------------------

# Kill server in background
        if double_opened_2:
            try:
                sock2.close()
                double_validation_2 = True
                print("Server killed.")
            except dbus.DBusException as e17:
                print(e17)
                print("&&Cannot kill server " + double_info[0]['ip'] + ":"
                      + str(double_info[0]['port']))

# ----------------------------------------------------------------------------------------

# Print information in docker screen and log_file
        self.assertEqual(flag_error, 0, "&&There is no connection_manager opened")
        self.assertEqual(query_double_2[0], True, "&&The video services are not reachable")
        self.assertEqual(double_opened_2, True, "&&The server " +
                         double_info[1]['ip'] + ":" + str(double_info[1]['port'])
                         + " was not created.")
        pass


# Orchestrator for testing
runner_test = unittest.TextTestRunner()
result_test_method1 = 0
result_test_method2 = 0
result_test_method3 = 0
result_test_method4 = 0
result_test_method1 = runner_test.run(unittest.makeSuite(Method1))
result_test_method2 = runner_test.run(unittest.makeSuite(Method2))
result_test_method3 = runner_test.run(unittest.makeSuite(Method3))
result_test_method4 = runner_test.run(unittest.makeSuite(Method4))


with open("Logs:test_app.txt", "a") as fp:
    if result_test_method1:
        fp.write("----------QueryByType(" + str(to_test_1) + ")----------\n")
        fp.write("Date: " + str(datetime.datetime.now()) + "\n\n\n")

        if flag_error == 1:
            fp.write("There is no connection_manager opened\n")
        else:
            if query_backend[0] or not server_opened:
                if not backend_exceptions:
                    fp.write("The backend services are reachable\n")
                else:
                    fp.write("At least one of the backend services is not reachable\n")
                fp.write("\nDone successfully:\n")
                if backend_validation:
                    for counter in range(0, number_backend+1):
                        if counter not in backend_exceptions:
                            fp.write("ip: " + backend_info[counter]['ip'] + "\n")
                            fp.write("port: " + str(backend_info[counter]['port']) + "\n")
                else:
                    fp.write("There is no server validated.\n")

                if backend_exceptions:
                    fp.write("\nServers are not reachable:\n")
                    for counter in range(0, number_backend+1):
                        if counter in backend_exceptions:
                            fp.write("ip: " + backend_info[counter]['ip'] + "\n")
                            fp.write("port: " + str(backend_info[counter]['port']) + "\n")

        if not server_opened:
            try:
                fp.write("\nThe server created in " + backend_info[number_backend]['ip'] + ":" +
                         str(backend_info[number_backend]['port']) + " could not be killed.\n")
            except dbus.DBusException as e18:
                print(e18)
                fp.write("\nThere is no ip_port asigned in the config.json file.\n")

        fp.write("\n----------QueryByType(" + str(to_test_1) + ")----------\n\n\n")

# -----------------------------------------------------------------------------------------

    if result_test_method2:
        fp.write("----------QueryByType(" + str(to_test_2) + ")----------\n")
        fp.write("Date: " + str(datetime.datetime.now()) + "\n\n\n")

        if flag_error == 1:
            fp.write("There is no connection_manager opened\n")
        else:
            if query_video[0] or not video_opened:
                if not video_exceptions:
                    fp.write("The video services are reachable\n")
                else:
                    fp.write("At least one of the video services is not reachable\n")
                fp.write("\nDone successfully:\n")
                if video_validation:
                    for counter in range(0, number_video + 1):
                        if counter not in video_exceptions:
                            fp.write("ip: " + video_info[counter]['ip'] + "\n")
                            fp.write("port: " + str(video_info[counter]['port']) + "\n")
                else:
                    fp.write("There is no server validated.\n")

                if video_exceptions:
                    fp.write("\nServers are not reachable:\n")
                    for counter in range(0, number_video + 1):
                        if counter in video_exceptions:
                            fp.write("ip: " + video_info[counter]['ip'] + "\n")
                            fp.write("port: " + str(video_info[counter]['port']) + "\n")

        if not video_opened:
            try:
                fp.write("\nThe server created in " + video_info[number_video]['ip'] + ":" +
                         str(video_info[number_video]['port']) + " could not be killed.\n")
            except dbus.DBusException as e19:
                print(e19)
                fp.write("\nThere is no ip_port asigned in the config.json file.\n")

        fp.write("\n----------QueryByType(" + str(to_test_2) + ")----------\n\n\n")

# -----------------------------------------------------------------------------------------

    if result_test_method3:
        fp.write("----------QueryByType(" + str(to_test_3) + ")----------\n")
        fp.write("Date: " + str(datetime.datetime.now()) + "\n\n\n")

        if flag_error == 1:
            fp.write("There is no connection_manager opened\n")
        else:
            if query_www[0]:
                fp.write("The www is reachable\n")
            else:
                fp.write("The www is not reachable\n")

            fp.write("Interface:" + query_www[1] + "\n")
            fp.write("ip:" + query_www[2] + "\n")
            fp.write("port:" + str(query_www[3]) + "\n")

        fp.write("\n----------QueryByType(" + str(to_test_3) + ")----------\n\n\n")

# -----------------------------------------------------------------------------------------

    if result_test_method4:
        fp.write("----------QueryByType(" + str(to_test_2) + ")----------\n")
        fp.write("Date: " + str(datetime.datetime.now()) + "\n\n\n")
        fp.write("Two servers connected. Checking priority.\n\n")

        if flag_error == 1:
            fp.write("There is no connection_manager opened\n")
        else:
            if query_double_1[0] or not double_opened_1:
                if double_validation_1:
                    fp.write("First server used:\n")
                    fp.write("ip: " + double_info[0]['ip'] + "\n")
                    fp.write("port: " + str(double_info[0]['port']) + "\n")
                else:
                    fp.write("First server was not killed correctly.\n")

                if double_validation_2:
                    fp.write("Second server used:\n")
                    fp.write("ip: " + double_info[1]['ip'] + "\n")
                    fp.write("port: " + str(double_info[1]['port']) + "\n")
                else:
                    fp.write("Second server was not killed correctly.\n")

                if not double_validation_1 or not double_validation_2:
                    fp.write("A server was not killed correctly.\n")

        fp.write("\n----------QueryByType(" + str(to_test_2) + ")----------\n\n\n")
