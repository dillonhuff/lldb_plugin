import lldb
import commands
import optparse
import shlex

def my_cmd(debugger, command, result, internal_dict):
    print 'My command executed!'
    
def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f custom_command.my_cmd my_cmd')
    print 'The "my_cmd" python command has been installed and is ready for use.'
    
