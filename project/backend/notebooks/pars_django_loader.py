from dotenv import dotenv_values
from pathlib import Path
import django
import os
import sys


config = dotenv_values(".env")
BACKEND_DIR_FOR_NOTEBOOK = config.get('BACKEND_DIR_FOR_NOTEBOOK')
BACKEND_DIR_FOR_NOTEBOOK_RESOLVED = Path(BACKEND_DIR_FOR_NOTEBOOK).resolve()

class DjangoLoader:
    def __init__(self, *args, **kwargs):
        self.backend_dir: Path = kwargs.get(
            "backend_dir",
            Path(BACKEND_DIR_FOR_NOTEBOOK).resolve()
        )
        self.pathers: list[callable] = kwargs.get(
            "pathers",
            [
                os.chdir,
                sys.path.append
            ]
        )
        self.django_settings_module: str = kwargs.get(
            "django_settings_module",
            "config.settings.develop"
        )
        self.allow_async: bool = kwargs.get(
            "allow_django_async",
            True
        ) 

        self.__has_error: bool | None = None 
    
    def __set_django_dir(self):
        for pather in self.pathers:
            pather(str(self.backend_dir))

    def __set_django_settings_module(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.develop'

    def __set_async_for_django(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

    def load_django_settings(self):
        try:
            if self.allow_async:
                self.__set_async_for_django()
    
            self.__set_django_dir()
            self.__set_django_settings_module()

            self.__has_error = False
        except Exception as e:
            self.__has_error = True
            raise e

    def start_django(self):
        django.setup()

    def __bool__(self):
        if self.__has_error is None:
            raise "Status check cannot give response 'cause before run load_django() function"
        return not self.__has_error

    @classmethod
    def auto(cls):
        cls = cls()
        cls.load_django_settings()
        if cls.__has_error:
            raise "Auto setup was stop 'cause loader has error"
        else:
            cls.start_django()
            print("Django has started...")