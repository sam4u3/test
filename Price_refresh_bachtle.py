import html
import os.path
import pandas
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def request_get(url):
    data = requests.get(url, verify=False)
    if data.status_code == 200:
        return data.content
    raise Exception('failed to get data')


def read_products(excel_path):
    print('Reading Excel file')
    product_data = pandas.read_excel(excel_path)
    print(f'Found Products : {len(product_data)}')
    return product_data['Product name']


def main(excel_path):
    base_url = 'https://www.bechtle.com/de-en/finder?query='
    product_names = read_products(excel_path)

    final_data = []

    for product_name in product_names:
        print(f'Searching product : {product_name}')
        product_name_encode = requests.utils.quote(product_name.strip())
        search_url = base_url + product_name_encode
        search_content = request_get(search_url)

        soup = BeautifulSoup(search_content, 'html.parser')
        p_items = soup.find_all('div', class_='product-list-item')

        for item in p_items:
            product_name_tag = item.find('div', class_='product-name')
            product_name_txt = product_name_tag.text.strip()
            if product_name_txt == product_name:
                print(f'Found product : {product_name_txt}')
                product_url = 'https://www.bechtle.com/' + item.find('a')['href']
                price = item.find('p', {'class': 'bechtle-price'}).text.strip()

                temp = {'Product Name': product_name,
                        'product url': product_url,
                        'product price': price}
                final_data.append(temp)
                print(f'Added price successfully, Price : {price}')
                break
        else:
            print('search query :', product_name, 'not found any products')
        return final_data


if __name__ == '__main__':
    excel_path = os.path.abspath(r"C:\PythonProjects\product_name.xlsx")
    data = main(excel_path=excel_path)
    df = pandas.DataFrame(data)
    df.to_excel('report.xlsx')