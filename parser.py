import requests
import lxml
import lxml.html as html
from urllib.parse import urljoin
import json
from requests.exceptions import ConnectionError, Timeout


def get_html_tree(url):
    """
    This method get the response from the url and tries to form a tree.
    :param url: string, url that we want get response from
    :return: lxml.html, tree
    """
    try:
        response = requests.get(url, timeout=2 * 60)
        if not response.ok:
            print('Failed to get response from %s' % url)
            return None
        else:
            tree = html.fromstring(response.text)
            return tree
    except ConnectionError:
        print('Connection error.')
    except Timeout:
        print('Request to %s timed out.' % url)
    return None


def get_city_link(tree):
    base_url = 'https://ticketon.kz'
    all_cities_xpath = './/ul[@id="region-sidebar__dropdown"]//a/@href'
    cities_urls = tree.xpath(all_cities_xpath)
    cities_urls = [urljoin(base_url, url) for url in cities_urls][1:]
    return cities_urls


def get_category_link(tree):
    base_url = 'https://ticketon.kz'
    category_urls = tree.xpath('.//nav[@class="nav"]//a/@href')
    category_urls = [urljoin(base_url, url) for url in category_urls]
    return category_urls


def get_events_links(tree):
    base_url = 'https://ticketon.kz'
    all_events_xpath = './/div[contains(@class, "list-item")]/a/@href'
    events_urls = tree.xpath(all_events_xpath)
    events_urls = [urljoin(base_url, url) for url in events_urls]
    return events_urls


def parse(tree, xpath):
    els = tree.xpath(xpath)
    if len(els):
        return els[0]
    else:
        return None


def get_page_data(tree):
    title_xpath = './/h1'
    time_xpath = './/div[@class="button-buy__wrapper"]//time/@datetime'
    image_xpath = './/div[@class="event__information"]//img/@src'
    description_xpath =  './/div[@class="event__information"]'
    title = tree.xpath(title_xpath)[0].text_content()
    time = parse(tree, time_xpath)
    image = parse(tree, image_xpath)
    description = parse(tree,description_xpath)
    if isinstance(description,lxml.html.HtmlElement):
        description = description.text_content()

    data = {'title': title,
            'time': time,
            'image': image,
            'description': description}
    return data


def cities_categories_parser(cities_categories_urls):
    '''
    This method gets combined urls of cities and categories and creates
    a dict of events in cities called c_dict, where key: city and value: all events;
    Then it puts this dict as a value to another dict called cities_categories_dict,
    where key: category and value c_dict.

    :param cities_categories_urls: list of 180 urls; 20 cities x 9 categories
    :return: cities_categories_dict
    '''
    cities_categories_dict = {}
    for city_category_url in cities_categories_urls:
        cities_events_urls_list = get_events_links(get_html_tree(city_category_url))
        c_dict = {}
        for city_event_url in cities_events_urls_list:
            c_dict[city_event_url] = get_page_data(get_html_tree(city_event_url))
            print(city_event_url + ' is done.')
        cities_categories_dict[city_category_url] = c_dict
        print(city_category_url + ' done.')
    return cities_categories_dict

def cities_parser(cities_urls):
    '''
    This method gets cities' urls and creates a dict of cities and all events in each city;
    Here key: city and value: all events
    :param cities_urls:
    :return: cities_dict
    '''
    cities_dict = {}
    for city_url in cities_urls:
        events_urls_list = get_events_links(get_html_tree(city_url))
        c_dict = {}
        for event_url in events_urls_list:
            c_dict[event_url] = get_page_data(get_html_tree(event_url))
            print(event_url + ' is done.')
        cities_dict[city_url] = c_dict
        print(city_url + ' done.')
    return cities_dict


def categories_parser(categories_urls):
    '''
    This method gets categories' urls and creates a dict of categories and all events in each category;
    Here key: category and value: all events
    :param categories_urls:
    :return: categories_dict
    '''
    categories_dict = {}
    for category_url in categories_urls:
        events_urls_list = get_events_links(get_html_tree(category_url))
        c_dict = {}
        for event_url in events_urls_list:
            c_dict[event_url] = get_page_data(get_html_tree(event_url))
            print(event_url + ' is done.')
        categories_dict[category_url] = c_dict
        print(category_url + ' done.')
    return categories_dict


def parser(cities_urls, categories_urls, cities_categories_urls):
    cities_dict = cities_parser(cities_urls)
    categories_dict = categories_parser(categories_urls)
    cities_categories_dict = cities_categories_parser(cities_categories_urls)
    return cities_dict, categories_dict, cities_categories_dict


def write_json(file_name, data):
    with open(file_name + '.json', 'w') as f:
        json.dump(data, f)


def read_file(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def main():
    cities_urls = read_file('cities.txt')
    categories_urls = read_file('categories.txt')
    cities_categories_urls = read_file('cities_categories.txt')

    cities_dict, categories_dict, cities_categories_dict = parser(cities_urls, categories_urls, cities_categories_urls)
    write_json('cities_categories_dict', cities_categories_dict)
    write_json('cities_dict', cities_dict)
    write_json('categories_dict', categories_dict)


if __name__ == '__main__':
    main()
