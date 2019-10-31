
class PayLoad:
    def __init__(self, identifier=None, last_updated=None, cpu_count=None, cpu_freq=None, cpu_perc=None, mem_total=None,
                 mem_available=None, mem_used=None, mem_free=None, mem_used_perc=None, swap_total=None, swap_used=None,
                 swap_free=None, swap_used_perc=None, data=None):
        if data is None:
            data = dict()
        self.IDENTIFIER = data.get('IDENTIFIER', identifier)
        self.LAST_UPDATED = data.get('LAST_UPDATED', last_updated)
        self.CPU_COUNT = data.get('CPU_COUNT', cpu_count)
        self.CPU_FREQ = data.get('CPU_FREQ', cpu_freq)
        self.CPU_PERC = data.get('CPU_PERC', cpu_perc)
        self.MEM_TOTAL = data.get('MEM_TOTAL', mem_total)
        self.MEM_AVAILABLE = data.get('MEM_AVAILABLE', mem_available)
        self.MEM_USED = data.get('MEM_USED', mem_used)
        self.MEM_FREE = data.get('MEM_FREE', mem_free)
        self.MEM_USED_PERC = data.get('MEM_USED_PERC', mem_used_perc)
        self.SWAP_TOTAL = data.get('SWAP_TOTAL', swap_total)
        self.SWAP_USED = data.get('SWAP_USED', swap_used)
        self.SWAP_FREE = data.get('SWAP_FREE', swap_free)
        self.SWAP_USED_PERC = data.get('SWAP_USED_PERC', swap_used_perc)

    def to_dict(self):
        return self.__dict__

    def to_tuple(self):
        return (self.IDENTIFIER, self.LAST_UPDATED, self.CPU_COUNT, self.CPU_FREQ, self.CPU_PERC, self.MEM_TOTAL,
                self.MEM_AVAILABLE, self.MEM_USED, self.MEM_FREE, self.MEM_USED_PERC, self.SWAP_TOTAL, self.SWAP_USED,
                self.SWAP_FREE, self.SWAP_USED_PERC)
