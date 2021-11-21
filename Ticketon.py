import json

class Ticketon():
    def __init__(self):
        self.cities_dict = self.read_json('cities_dict')
        self.cities_categories_dict = self.read_json('cities_categories_dict')
        self.categories_dict = self.read_json('categories_dict')


    def read_json(self,file_name):
        with open(file_name + '.json', 'r') as json_file:
            data = json.load(json_file)     
        return data


    def get_by_city(self, city_name):
        city_events = {}
        for cities, events in self.cities_dict.items():
            if city_name in cities:
                for event, info in events.items():
                    city_events[event] = info
        return city_events
    
    
    def get_by_date(self, date):
        date_events = {}
        for category, events in self.cities_categories_dict.items():
            for event, info in events.items():
                if info['time'] != None and date in info['time']:
                    date_events[event] = info
        return date_events
    

    def get_by_city_date(self, city_name, date):
        city_date_events = {}
        city_events = self.get_by_city(city_name)
        for city_event, info in city_events.items():
            if info['time'] != None and date in info['time']:
                city_date_events[city_event] = info
        return city_date_events
    
    
    def get_by_category(self, category_name):
        category_events = {}
        for category, events in self.categories_dict.items():
            if category_name in category:
                for event, info in events.items():
                    category_events[event] = info
        return category_events
    
    
    def get_by_city_category(self, city_name, category_name):
        city_category_events = {}
        for city_category, events in self.cities_categories_dict.items():
            if category_name in city_category and city_name in city_category:
                for event, info in events.items():
                    city_category_events[event] = info
        return city_category_events

    
    def get_by_category_date(self, date, category_name):
        category_date_events = {}
        category_events = self.get_by_category(category_name)
        for category_event, info in category_events.items():
            if (info['time'] != None and date in info['time']):
                category_date_events[category_event] = info
                
        return category_date_events
    
    
    def get_by_city_category_date(self, city_name, category_name, date):
        city_category_date_events = {}
        city_categories_dict = self.get_by_city_category(city_name, category_name)
        for category_event, info in city_categories_dict.items():
            if (info['time'] != None and date in info['time']):
                city_category_date_events[category_event] = info
        return city_category_date_events