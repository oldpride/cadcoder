# tracetools.py
# Drop this file next to your macros or in FreeCAD's Macro folder
# Usage: from tracelines import TraceLines

import sys
import linecache
import os
import re

# tracetools.py
# Fully self-contained, never traces its own lines

import sys
import linecache
import os
from types import FrameType
from typing import Optional

import runpy
import inspect
import time

# Full path to this module file — computed once at import time
_TRACETOOLS_MODULE_PATH = os.path.abspath(__file__)

# get TraceLines start line number
TraceLines_start_lineno = inspect.currentframe().f_lineno
class TraceLines:
    """
    Context manager: prints each executed line from your script only.
    Completely ignores:
      • tracetools.py itself
      • FreeCAD internals
      • any imported module
    """
    def __init__(self, enabled: bool = True, 
                 files_to_trace: Optional[list[str]] = None, 
                 filePattern: Optional[str] = None,
                 funcPattern: Optional[str] = None):
        self.enabled = enabled
        self.caller_path: Optional[str] = None
        self.files_to_trace = files_to_trace
        self.filePattern = filePattern
        self.funcPattern = funcPattern
        self.start_time = time.perf_counter()
        self.last_time = self.start_time

    def __enter__(self):
        # print(f"Tracing lines... (enabled={self.enabled})")
        if not self.enabled:
            return self

        # Get the file that wrote "with TraceLines(...):"
        caller_frame: FrameType = sys._getframe(1)
        caller_file = caller_frame.f_globals.get("__file__")
        if caller_file:
            self.caller_path = os.path.abspath(caller_file)
        else:
            # Rare case: interactive console / Jupyter
            self.caller_path = None

        def traceit(frame: FrameType, event: str, arg):
            if event != "line":
                return traceit

            callee_path = os.path.abspath(frame.f_code.co_filename)
            callee_func = frame.f_code.co_name

            # Skip tracetools.py completely
            # if filename == _TRACETOOLS_MODULE_PATH:
            #     return traceit

            # Skip TraceLines class only, but allow tracing other code in tracetools.py
            if callee_path == _TRACETOOLS_MODULE_PATH:
                lineno = frame.f_lineno
                if TraceLines_start_lineno <= lineno and lineno <= TraceLines_end_lineno:
                    return traceit
            
            # Only trace the original user script
            # if self.script_path and filename == self.script_path:
            if (callee_path == self.caller_path
                or (self.files_to_trace and callee_path in self.files_to_trace)
                or (self.filePattern and re.search(self.filePattern, callee_path, re.IGNORECASE))
                or (self.funcPattern and re.search(self.funcPattern, callee_func, re.IGNORECASE))
            ):
                # print(f"Tracing line in file: {callee_path} vs {self.filePattern}, function: {callee_func} vs {self.funcPattern}")
                lineno = frame.f_lineno
                line = linecache.getline(callee_path, lineno).rstrip()
                # skip blank lines and comment-only lines
                if re.match(r'^\s*#', line):
                    # comment-only line
                    return traceit
                if re.match(r'^\s*$', line):
                    # blank line
                    return traceit

                # only record actual code line's elapsed time
                now = time.perf_counter()
                elapsed = now - self.last_time
                total_elapsed = now - self.start_time
                self.last_time = now
                if elapsed > 1:
                    print() # print a blank line to signal a gap

                # Actual code line
                print(f"{total_elapsed:.2f}s {elapsed:.2f}s {os.path.basename(callee_path)}:{lineno} {line.lstrip()}")
                sys.stdout.flush()

            return traceit

        sys.settrace(traceit)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        elapsed = time.perf_counter() - self.start_time
        print(f"Total elapsed time: {elapsed:.2f}s")
        if self.enabled:
            sys.settrace(None)
        # Returning False = let exceptions propagate normally
        return False
TraceLines_end_lineno = inspect.currentframe().f_lineno
    
def trace_file(script_path: str, 
               enabled: bool = True, 
               filePattern: Optional[str] = None,
               funcPattern: Optional[str] = None
               ):
    """
    Runs a FreeCAD macro with TraceLines automatically enabled.
    You don't need to modify the macro at all!
    """
    script_path = os.path.abspath(script_path)
    
    try:
        tracer = TraceLines(enabled=enabled, 
                            files_to_trace=[script_path], 
                            filePattern=filePattern,
                            funcPattern=funcPattern)
        # print(f"trace_enabled={enabled} for script: {script_path}")
        tracer.caller_path = script_path
        tracer.__enter__()

        runpy.run_path(script_path, run_name="__main__")
    finally:
        tracer.__exit__(None, None, None)

def test_function():
    a = 5
    print(f"a + 1 = {a} + 1 = {a + 1}")

def main():
    print("with TraceLines enabled:")
    with TraceLines(enabled=True):
        test_function()
    print("with TraceLines disabled:")
    with TraceLines(enabled=False):
        test_function()

 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_script_path = os.path.join(script_dir, "tracetools_test.py")
    print("Running tracetools_test.py with tracing:")
    trace_file(test_script_path, enabled=True)

if __name__ == "__main__":
    main()
