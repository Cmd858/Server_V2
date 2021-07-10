import ctypes
from infi.systray import SysTrayIcon


class ConsoleManager:
    def __init__(self, exitCallback):
        self.exitCallback = exitCallback
        options = (("Activate Console", None, lambda x: self.ConsoleVisible(True)),
                   ("Deactivate Console", None, lambda x: self.ConsoleVisible(False)))
        self.trayIcon = SysTrayIcon(None, 'Server_V2 Options', options, self.CallKillServer)

    def ConsoleVisible(self, visBool):
        if visBool is False:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        else:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

    def CallKillServer(self, systray):
        try:
            SysTrayIcon.shutdown
        except Exception as e:
            print(e)
        self.exitCallback()

    def StartTrayIcon(self):
        self.trayIcon.start()
