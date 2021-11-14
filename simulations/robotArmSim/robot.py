import simpylc as sp

class Robot(sp.Module):

    def __init__(self):
        sp.Module.__init__(self)

        self.page('eigen robot')

        #self.group('base', True)
        #self.basePWM = sp.Register()
        self._yes = ''
        