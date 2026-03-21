import inspect

def prefix_stack(msg, debug):
    # print(f"debug={debug}") 

    if not debug:
        return
    
    stacks = inspect.stack()
    callers = []

    try:
        callerfile1 = stacks[1].filename
    except:
        callerfile1 = ""
    # reverse order, so that outermost caller is first
    for i in range(1, len(stacks)-1):

        try:
            caller = stacks[i]
            callerfile = caller.filename
            callerfunc = caller.function
            callerline = caller.lineno
        except:
            callerfile = ""
            callerfunc = ""
            callerline = ""

        if debug == 1:
            # debug level 1: only print stacks inside immediate caller's file.
            if callerfile != callerfile1:
                break
        callers.append(f"{callerfunc},{callerline}")

    prefix = "/".join(reversed(callers)) +": "

    print(prefix + msg)
