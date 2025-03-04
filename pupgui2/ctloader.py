import pkgutil
import importlib

from pupgui2.resources import ctmods


class CtLoader:
    
    ctmods = []
    ctobjs = []

    def __init__(self, main_window = None):
        self.main_window = main_window
        self.load_ctmods()

    def load_ctmods(self) -> bool:
        """
        Load ctmods
        Return Type: bool
        """
        for _, mod, _ in pkgutil.iter_modules(ctmods.__path__):
            if mod.startswith('ctmod_'):
                try:
                    ctmod = importlib.import_module(f'pupgui2.resources.ctmods.{mod}')
                    if ctmod is None:
                        print('Could not load ctmod', mod)
                        continue
                    self.ctmods.append(ctmod)
                    self.ctobjs.append({
                        'name': ctmod.CT_NAME,
                        'launchers': ctmod.CT_LAUNCHERS,
                        'description': ctmod.CT_DESCRIPTION,
                        'installer': ctmod.CtInstaller(main_window=self.main_window)
                    })
                    print('Loaded ctmod', ctmod.CT_NAME)
                except Exception as e:
                    print('Could not load ctmod', mod, ':', e)
        return True

    def get_ctmods(self, launcher=None, advanced_mode=True):
        """
        Get loaded ctmods, optionally sort by launcher
        Return Type: []
        """
        if launcher is None:
            return self.ctmods

        ctmods = [ctmod for ctmod in self.ctmods if launcher in ctmod.CT_LAUNCHERS and ('advmode' not in ctmod.CT_LAUNCHERS or advanced_mode)]

        return ctmods

    def get_ctobjs(self, launcher=None, advanced_mode=True):
        """
        Get loaded compatibility tools, optionally sort by launcher
        Return Type: List[dict]
        Content(s):
            'name', 'launchers', 'installer'
        """
        if launcher is None:
            return self.ctobjs

        ctobjs = []
        for ctobj in self.ctobjs:
            if launcher.get('launcher') in ctobj['launchers']:
                if 'advmode' in ctobj['launchers'] and not advanced_mode:
                    continue
                if 'native-only' in ctobj['launchers'] and launcher.get('type') != 'native':
                    continue
                ctobjs.append(ctobj)
        return ctobjs
