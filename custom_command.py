import lldb
import commands
import optparse
import shlex

def my_cmd(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()

    for frame in thread:

        print str(frame)

        function = frame.GetFunction()
        print 'FUNCTION = ', function

        if frame.IsInlined():
            print 'INLINED'
        else:
            args = frame.get_arguments()

            print '# of arguments = ', len(args)

            for arg in args:
                print arg

            vars = frame.get_all_variables()

            print '# of vars =', len(args)

            for var in vars:
                print var

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f custom_command.my_cmd my_cmd')
    print 'The "my_cmd" python command has been installed and is ready for use.'
