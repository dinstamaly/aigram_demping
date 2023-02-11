

"""
В модуле определены фунции для создания файлов
"""

__author__ = 'Dinmukhamed Stamaliev'
import asyncio
import io
import xlsxwriter
from service import get_min_value
from data import gsheet2df


async def get_report_file(data):
    api = gsheet2df('ExcelFormatTemplate', 0)
    new = {}
    new_2 = []
    # print(sheet)

    for i in api:
        print(i)
        if i['price']:
            new[i['SKU'].strip()] = float(i['price'].replace(',', '.'))
            new_2.append(i["SKU"])

    print("---------------------")
    print(len(new_2))
    print("---------------------")

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)

    head_style = workbook.add_format(
        {
            'bold': True, 'border': 2, 'align': 'center',
        }
    )
    head_style2 = workbook.add_format(
        {
            'bold': True, 'bg_color': '#2155CD', 'align': 'left',
            'font_color': 'white'
        }
    )
    content_style = workbook.add_format(
        {
            'bold': False, 'border': 2, 'align': 'center',
        }
    )
    content_style2 = workbook.add_format(
        {
            'bold': False, 'bg_color': '#C4DDFF', 'align': 'left',
        }
    )
    content_style_price1 = workbook.add_format(
        {
            'bold': False, 'bg_color': '#D3D3D3', 'align': 'left',
        }
    )
    content_style_price2 = workbook.add_format(
        {
            'bold': False, 'bg_color': '#00FF00', 'align': 'left',
        }
    )
    content_style3 = workbook.add_format(
        {
            'bold': False, 'align': 'left',
        }
    )
    diff_style = workbook.add_format(
        {
            'bold': False, 'border': 0, 'align': 'center',
            # 'text_wrap': True,
        }
    )
    diff_color_style = workbook.add_format(
        {
            'bold': False, 'border': 0, 'align': 'center',
            'bg_color': 'yellow',
        }
    )
    diff_negative_style = workbook.add_format(
        {
            'bold': False, 'border': 0, 'align': 'center',
            'bg_color': 'green',
        }
    )
    worksheet = workbook.add_worksheet()

    columns = [
        'SKU',
        'model',
        'brand',
        'price',
        'PP1',
        'PP2',
        'PP3',
        'PP4',
        'PP5',
        'preorder',
    ]

    diff_columns = [
        'link',
        'initial price',
        'difference',
        'market name',
        'market price',
        'start price',
        '+ 25%'
    ]

    for index, value in enumerate(columns):
        worksheet.write(0, index, value, head_style)

    for index, value in enumerate(diff_columns):
        worksheet.write(0, index + 11, value, head_style)

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 65)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:J', 17)
    worksheet.set_column('L:L', 15)
    worksheet.set_column('M:M', 20)
    worksheet.set_column('N:P', 17)

    for i, tr in enumerate(data, start=1):

        try:
            data_dict = get_min_value(tr["masterProduct"]["productUrl"],
                                      tr['priceMin'])
        except BaseException as ex:
            print(ex)

        price = tr['priceMin'] if tr['priceMin'] else tr['priceMax']
        price10 = 0
        sum = 0
        if tr['sku'] in new_2:
            print('Yes')
            price10 = float(price / 100 * 25) + float(new[tr['sku']])
            print(price, float(price / 100 * 25), float(new[tr['sku']]))
            sum = float(new[tr['sku']])
        else:
            print('No')
            print(tr['sku'])

        worksheet.write(i, 0, tr['sku'], content_style)
        worksheet.write(i, 1, tr['name'], content_style)
        worksheet.write(i, 2, tr['brand'], content_style)
        worksheet.write(i, 3, price, content_style)
        worksheet.write(i, 4, 'yes', content_style)
        worksheet.write(i, 5, 'no', content_style)
        worksheet.write(i, 6, 'no', content_style)
        worksheet.write(i, 7, 'no', content_style)
        worksheet.write(i, 8, 'no', content_style)
        worksheet.write(i, 9, '', content_style)
        worksheet.write_url(i, 11, tr["masterProduct"]["productUrl"], string='link')
        if data_dict:
            worksheet.write(i, 12, '', diff_style)
            worksheet.write(i, 13, data_dict['difference'], diff_style)
            worksheet.write(i, 14, data_dict['name'], diff_style)
            worksheet.write(i, 15, data_dict['price'], diff_style)

            if data_dict['difference'] > 1:
                worksheet.write(i, 12, price, diff_style)
                worksheet.write(i, 13, data_dict['difference'],
                                diff_color_style)
                worksheet.write(i, 3, data_dict['price'] - 1,
                                content_style)

            if -1 >= data_dict['difference'] >= -10:
                worksheet.write(i, 12, price, diff_style)
                worksheet.write(i, 13, data_dict['difference'],
                                diff_negative_style)
                worksheet.write(i, 3, data_dict['price'] - 1,
                                content_style)
        worksheet.write(i, 16, sum, content_style_price1)
        worksheet.write(i, 17, price10, content_style_price2)
    ################################ worksheet2 ###############################
    worksheet2 = workbook.add_worksheet()
    columns2 = ['Data Item', 'Description']
    columns_data2 = {
        'SKU': 'Merchant specific product identifier. Unique across the merchant.',
        'model': 'Product name.',
        'brand': 'Brandname of the product, e.g. Apple',
        'price': 'Price in KZT, will be set globally across all citiies.',
        'PP1': 'Availability for pick-up point 1 of the merchant. The pick-up points will be defined at merchant onboarding time and communicated to the merchant.',
        'PP2': 'as above',
        'PP3': 'as above',
        'PP4': 'as above',
        'PP5': 'as above',
    }
    worksheet2.set_column('A:A', 15)
    worksheet2.set_column('B:B', 150)
    for index, value in enumerate(columns2):
        worksheet2.write(0, index, value, head_style2)

    for i, tr in enumerate(columns_data2.items(), start=1):
        style = content_style3
        if i % 2 != 0:
            style = content_style2
        worksheet2.write(i, 0, tr[0], style)
        worksheet2.write(i, 1, tr[1], style)

    workbook.close()
    return output.getvalue()