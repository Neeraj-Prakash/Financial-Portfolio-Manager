import datetime
from dateutil import relativedelta

class Asset:
    inv_amt = 0
    int_rate = 0
    
    def __init__(self, a_name, a_type, a_inv, a_units, a_date, sip, a_val):
        self.a_name = a_name
        self.a_type = a_type
        self.a_inv = a_inv
        self.a_units = a_units
        self.a_date = a_date
        self.sip = sip
        self.a_val = a_val
        self.set_time_inv()
        self.set_inv_amt()
    
    def set_inv_amt(self):
        if self.sip in ['y', 'Y']:
            months = self.time_inv[2] * 12 + self.time_inv[1]
            self.inv_amt = self.a_inv * months
        else:
            self.inv_amt = self.a_inv
    
    def set_time_inv(self):
        '''date = self.a_date.split(sep='-')
        date = list(map(int, date))
        st_date = datetime.datetime(date[2], date[1], date[0])'''
        st_date = self.a_date
        end_date = datetime.datetime.now()
        relative = relativedelta.relativedelta(end_date, st_date)
        self.time_inv = [relative.days, relative.months, relative.years]

    def set_int_rate(self, rate):
        self.int_rate = rate

    def get_int_amt(self):
        return self.a_val - self.inv_amt

class Portfolio:
    m_sip = 0
    def __init__(self, asset_list):
        self.asset_list = asset_list
        self.set_t_val()
        self.set_t_inv()
        self.set_t_int()
        self.set_allo()
        self.set_m_sip()


    def set_t_val(self):
        tval = 0
        for asset in self.asset_list:
            tval += asset.a_val
        self.t_val = tval
    
    def set_t_inv(self):
        tinv = 0
        for asset in self.asset_list:
            tinv += asset.inv_amt
        self.t_inv = tinv

    def set_t_int(self):
        self.t_int = self.t_val - self.t_inv
    
    def set_allo(self):
        self.allo = dict()
        for asset in self.asset_list:
            if asset.a_type in self.allo:
                self.allo[asset.a_type] += asset.a_val
            else:
                self.allo[asset.a_type] = asset.a_val    

    def set_m_sip(self):
        for asset in self.asset_list:
            if asset.sip in ['Y', 'y']:
                self.m_sip += asset.a_inv