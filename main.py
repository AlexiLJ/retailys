import requests
import zipfile
import io
import xml.etree.ElementTree as ET

def products(path:str) -> list[dict]:
    tree = ET.parse(path)
    root = tree.getroot().find("items")
    top_level = root.findall("./item")
    product_list = []
    for item in top_level:
        product = {'spare_parts': []}
        product['name'] = item.get("name")
        parts = item.findall('.//part[@categoryId="1"]//item')
        if parts:
            for part in parts:
                part_name = part.get("name")
                product['spare_parts'].append(part_name)
        product_list.append(product)
    return product_list
#
if __name__ == '__main__':
    url = 'https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip'

    response = requests.get(url)
    assert response.status_code == 200, 'Wrong status code'

    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        thezip.extractall('data')
        filename = thezip.namelist()[0]
    path = f'./data/{filename}'
    products = products(path)

    while True:
        choice = input('\nIf you want to see quantity of products press 1 \n'
                       'If you want to print ALL products press 2 \n'
                       'If you want to print ALL products + SPARE parts press 3 \n>>> ' )

        if choice == '1':
            print(f'There are {len(products)} products')
        elif choice == '2':
            for product in products:
                print(product['name'])
        elif choice == '3':
            for product in products:
                string_to_print = f"Product: {product['name']} "
                if product['spare_parts']:
                    string_to_print += "\nSpare parts: \n"
                    for part in product['spare_parts']:
                        string_to_print += f"\t {part} \n"
                print(string_to_print)
        else:
            print('Wrong input')
            continue
