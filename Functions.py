import json


class Solutions:
    @staticmethod
    def load_geonames_data(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = [line.strip().split('\t') for line in file.readlines()]
        return data

    @staticmethod
    def get_city_subset(page, page_size, geonames_data):
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return geonames_data[start_index:end_index]

    @staticmethod
    def find_city_info(city_name, geonames_data):
        found_cities = [city for city in geonames_data if city[1].lower() == city_name.lower()]
        if found_cities:
            max_population_city = max(found_cities, key=lambda x: int(x[14]))
            return max_population_city
        else:
            return None

    @staticmethod
    def determine_northern_city(city1_info, city2_info):
        latitude_city1 = float(city1_info[4])
        latitude_city2 = float(city2_info[4])
        if latitude_city1 > latitude_city2:
            return city1_info[1], city1_info[4]
        elif latitude_city1 < latitude_city2:
            return city2_info[1], city2_info[4]
        else:
            return "Both cities are located on the same latitude"

    @staticmethod
    def check_same_timezone(city1_info, city2_info):
        timezone_city1 = city1_info[17]
        timezone_city2 = city2_info[17]
        if timezone_city1 == timezone_city2:
            return "Города имеют одинаковый часовой пояс"
        else:
            return "В городах разные часовые пояса"


class Tasks:
    @staticmethod
    def first_task(path):
        geonameid = path.split('/')[-1]
        geonames_data = Solutions.load_geonames_data('RU.txt')
        for city in geonames_data:
            if city[0] == geonameid:
                return json.dumps(city, indent=2)
        return json.dumps({"error": "City not found"})

    @staticmethod
    def second_task(path):
        params = path.split('?')[1].split('&')
        query_params = {}
        for param in params:
            key, value = param.split('=')
            query_params[key] = int(value) if key in ['page', 'page_size'] else value
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        geonames_data = Solutions.load_geonames_data('RU.txt')
        city_subset = Solutions.get_city_subset(page, page_size, geonames_data)
        return json.dumps(city_subset, indent=2)

    @staticmethod
    def third_task(path):
        params = path.split('?')[1].split('&')
        query_params = {}
        for param in params:
            key, value = param.split('=')
            query_params[key] = value
        city1_name = query_params.get('city1')
        city2_name = query_params.get('city2')
        city1_info = Solutions.find_city_info(city1_name, Solutions.load_geonames_data('RU.txt'))
        city2_info = Solutions.find_city_info(city2_name, Solutions.load_geonames_data('RU.txt'))
        if not city1_info:
            return json.dumps({"error": f"City '{city1_name}' not found"})
        if not city2_info:
            return json.dumps({"error": f"City '{city2_name}' not found"})
        northern_city = Solutions.determine_northern_city(city1_info, city2_info)
        timezone_info = Solutions.check_same_timezone(city1_info, city2_info)
        result = {
            "city1": city1_info,
            "city2": city2_info,
            "Северный город": northern_city,
            "Информация о часовом поясе": timezone_info
        }
        return json.dumps(result, indent=2, ensure_ascii=False)



