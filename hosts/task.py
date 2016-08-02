

class Task(object):
    def __init__(self,request):
        self.request = request
        self.task_type = self.request.POST.get("task_type")

    def handle(self):
        if self.task_type:
            func = getattr(self,self.task_type)
            return func()

    def multi_cmd(self):
        print '------going to run cmd------'

    def multi_file_transfer(self):
        pass