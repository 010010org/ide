import tkinter as tk


class TemplateWindow():
    def __init__(self, x, y, parent = None):
        self._debugMode = False
        self._previousX = x
        self._previousY = y
        self._windowX = x
        self._windowY = y

        self._icon = None
        
        if parent == None:
            self._window = tk.Tk()
        else:
            self._window = tk.Toplevel(parent)
        


        self._window.geometry(f"{x}x{y}")
    
    def update(self):
        """resizes the image to the current size of the window"""
        self._window.update()
        
        pass
    
    def run(self):
        self._window.mainloop()


class testWindow(TemplateWindow):
    def __init__(self):
        super().__init__(300, 300)
        self.run()

window = testWindow()
        