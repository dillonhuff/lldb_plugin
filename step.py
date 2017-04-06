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

    
