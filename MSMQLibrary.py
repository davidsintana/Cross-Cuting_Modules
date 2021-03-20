import pythoncom
import win32com.client
import os

pythoncom.CoInitialize()

class MQMessage:
    def __init__(self, label, body):
        self.label = label
        self.body = body


class MQ:
    def __init__(self, name):
        pythoncom.CoInitialize()
        self.name = name
        self.qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
        self.computer_name = os.getenv('COMPUTERNAME')

    def send_message(self, message):
        # Functionality: sends a message to the MQ Object
        # Input: a MQMessage Object
        self.qinfo.FormatName = "direct=os:" + self.computer_name + "\\PRIVATE$\\" + self.name
        queue = self.qinfo.Open(2, 0)
        com_message = win32com.client.Dispatch("MSMQ.MSMQMessage")
        com_message.Label = message.label
        com_message.Body = message.body
        com_message.Send(queue)
        print("Message " + message.label + " sent")
        queue.Close()

    def get_message(self):
        # Functionality: Gets the latest message from the MQ Object
        # Output: Message Body
        self.qinfo.FormatName = "direct=os:" + self.computer_name + "\\PRIVATE$\\" + self.name
        queue = self.qinfo.Open(1, 0)
        message = queue.Receive()
        print("Get message from " + self.name + " Message Queue")
        # message = MQMessage(com_message.Label, com_message.Body)
        queue.Close()

        return message

