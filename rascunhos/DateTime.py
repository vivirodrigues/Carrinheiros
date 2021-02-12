class DateTime:
    def __init__(self, date):
        self.date = date
        self.weekday_pt = ''
        self.weekday_en = ''
        self.number_day = ''
        self.set_weekday()

    def set_weekday(self):
        self.number_day = datetime.datetime.strptime(self.date, '%d %m %Y').weekday()
        self.weekday_pt = get_day_name(self.number_day)
        self.weekday_en = calendar.day_name[self.number_day]

    def get_weekday_en(self):
        return self.weekday_en

    def get_weekday_pt(self):
        return self.weekday_pt

    def get_number_day(self):
        return self.number_day