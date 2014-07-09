import os
class getEnv:
    def __init__(self, envParam):
        super().__init__()
        self.env = ''
        cmdLine = 'env | grep ' + envParam
        try:
            fd = os.popen(cmdLine)
            for env in fd:
                self.env=env.split("=")[1].strip()
        except Exception as e:
                print("Error: get Env error!\n")
        finally:
                fd.close()
    def getEnv(self,):
        return self.env

