import lldb

class FindVar:

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
        res = self.thread_plan.GetThread().GetStopReason() == lldb.eStopReasonTrace
        return res

    def should_stop(self, event):

        frame = self.thread_plan.GetThread().GetFrameAtIndex(0)
        a_var = frame.FindVariable("r1")

        if not a_var.IsValid():
            print "Havent found r1 yet"
            return False
        else:
            print "Found r1!"
            self.thread_plan.SetPlanComplete(True)
            return True

    def should_step(self):
        return True
