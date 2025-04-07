import time

from types import TracebackType
from typing import Self,Any,Type ,IO

class Timer:
    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> Self:
        self.start_time : float = time.perf_counter()
        print('Timer started')

        return self
    
    def __exit__(self,exc_type: Type[BaseException] | None,
                 exc_vall: Any | None,
                 exc_tb: TracebackType | None) -> None:
        self.end_time: float = time.perf_counter()
        elapsed_time: float = self.end_time - self.start_time
        print(f'Time: {elapsed_time}')

        if exc_type:
            print(exc_type,exc_vall,exc_tb)

        return True
    

class FileManager:
    def __init__(self,filename:str, mode:str) ->None:
        self.filename = filename
        self.mode = mode
    def __enter__(self) -> IO:
        self._file = open(self.filename,self.mode)
        print(f'Custom Open of {self.filename}')

        return self._file
    
    def __exit__(self,exc_type: Type[BaseException] | None,
                 exc_vall: Any | None,
                 exc_tb: TracebackType | None):
        if self._file:
            self._file.close()
            print(f'Close file: {self.filename}')
        if exc_type:
            print(exc_type,exc_vall,exc_tb)

with FileManager('data.txt','r') as file:
    data: str = file.read()
    print(data)

with Timer('name') as timer:
    timer.name
    # raise Exception("stop problem")
    for _ in range(1_000_000_00):
        pass