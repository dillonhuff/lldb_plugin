import lldb
import commands
import optparse
import shlex

def ls(debugger, command, result, internal_dict):
    print >>result, (commands.getoutput('/bin/ls %s' % command))
    
def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f custom_command.ls ls')
    print 'The "ls" python command has been installed and is ready for use.'
    
