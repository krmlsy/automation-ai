import os,base64

def getProjectRootDir():
    try:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        return ROOT_DIR.replace("/standart.selenium","").replace("/utilities","")
    except Exception as e:
        print(e)

def getPassword():
    base64_message = 'QXNpeWU1NTY2OQ=='
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message