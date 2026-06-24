

class DependencyManager:
    def __init__(self, modelInvokeobj):
        self.modelInvokeobj = modelInvokeobj

    def getmodelInvokeobj(self):
        return self.modelInvokeobj

    def setdocparssingobj(self, docparsingobj):
        self.docparsingobj = docparsingobj
    
    def getdocparsingobj(self):
        return self.docparsingobj
    
    def settoolsobj(self, toolsobj):
        self.toolsobj = toolsobj

    def gettoolsobj(self):
        return self.toolsobj
    
    # def gettools(self):
    #     return self.toolsobj.gettools()