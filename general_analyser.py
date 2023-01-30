# getting a basic idea of the data from the different sources

class GeneralAnalyser:
    def __init__(self, data_selectors = {'guardian' : 'guardian_*.csv', 'mirror' : 'mirror_*.csv', 'telegraph': 'telegraph_*.csv', 
    'sun' : 'sun_*.csv', 'mail' : 'mail_*.csv', 'metro' : 'metro_*.csv', 'express' : 'express_*.csv'}):
        self.data_selectors = data_selectors

    def compare_number_of_records(self):
        record_numbers = {}
        for paper in self.data_selectors.keys():
            record_nums = 

    def compare_number_of_records_over_time(self):
        pass 


if __name__ == "__main__":
    pass