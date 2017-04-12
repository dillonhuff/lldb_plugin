import lldb

class MyStep:

    def __init__(self, thread_plan, dict):
        self.thread_plan = thread_plan
        self.start_address = thread_plan.GetThread().GetFrameAtIndex(0).GetPC()

    def explains_stop(self, event):
        res = self.thread_plan.GetThread().GetStopReason() == lldb.eStopReasonTrace
        return res

    def should_stop(self, event):
        cur_pc = self.thread_plan.GetThread().GetFrameAtIndex(0).GetPC()

        print 'cur_pc        = ', cur_pc
        print 'start address = ', self.start_address

        if cur_pc < self.start_address or cur_pc >= self.start_address + 20:
            self.thread_plan.SetPlanComplete(True)
            return True
        else:
            return False

    def should_step(self):
        return True

    
class StepCheckingCondition:

    def __init__(self, thread_plan, dict):
        self.thread_plan = thread_plan
        self.start_frame = thread_plan.GetThread().GetFrameAtIndex(0)
        self.queue_next_plan()

    def queue_next_plan(self):
        cur_frame = self.thread_plan.GetThread().GetFrameAtIndex(0)
        cur_line_entry = cur_frame.GetLineEntry()
        start_address = cur_line_entry.GetStartAddress()
        end_address = cur_line_entry.GetEndAddress()
        line_range = end_address.GetFileAddress() - start_address.GetFileAddress()
        self.step_thread_plan = self.thread_plan.QueueThreadPlanForStepOverRange(
            start_address, line_range)

    def explains_stop(self, event):
        # We are stepping, so if we stop for any other reason, it isn't
        # because of us.
        return True

    def should_stop(self, event):
        # if not self.step_thread_plan.IsPlanComplete():
        #     return False

        frame = self.thread_plan.GetThread().GetFrameAtIndex(0)
        # if not self.start_frame.IsEqual(frame):
        #     self.thread_plan.SetPlanComplete(True)
        #     return True

        # This part checks the condition.  In this case we are expecting
        # some integer variable called "a", and will stop when it is 20.
        a_var = frame.FindVariable("r1")

        if not a_var.IsValid():
            print "Havent found r1 yet"
            #self.queue_next_plan()
            return False
        else:
            print "Found r1!"
            self.thread_plan.SetPlanComplete(True)
            return True

        # error = lldb.SBError()
        # a_value = a_var.GetValueAsSigned(error)
        # if not error.Success():
        #     print "z value was not good."
        #     return True

        # if a_value == 9:
        #     print 'Found z with correct value'
        #     self.thread_plan.SetPlanComplete(True)
        #     return True
        # else:
        #     self.queue_next_plan()
        #     return False

    def should_step(self):
        return True

# Here's an example that steps out of the current frame, gathers some information
# and then continues.  The information in this case is rax.  Currently the thread
# plans are not a safe place to call lldb command-line commands, so the information
# is gathered through SB API calls.


class FinishPrintAndContinue:

    def __init__(self, thread_plan, dict):
        self.thread_plan = thread_plan
        self.step_out_thread_plan = thread_plan.QueueThreadPlanForStepOut(
            0, True)
        self.thread = self.thread_plan.GetThread()

    def is_stale(self):
        if self.step_out_thread_plan.IsPlanStale():
            self.do_print()
            return True
        else:
            return False

    def explains_stop(self, event):
        return False

    def should_stop(self, event):
        if self.step_out_thread_plan.IsPlanComplete():
            self.do_print()
            self.thread_plan.SetPlanComplete(True)
        return False

    def do_print(self):
        frame_0 = self.thread.frames[0]
        rax_value = frame_0.FindRegister("rax")
        if rax_value.GetError().Success():
            print "RAX on exit: ", rax_value.GetValue()
        else:
            print "Couldn't get rax value:", rax_value.GetError().GetCString()
