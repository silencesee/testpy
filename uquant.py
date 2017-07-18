# -*- coding: utf-8 -*-
from Done.Uquant.dataapi import Client

if __name__ == "__main__":
    try:
        client = Client()
        client.init('6f959ceaec5993c82be88fffef5c5eb83703a86460b45b5d640f0c2e9a48c954')
        url1 = '/api/equity/getSecST.json?field=&secID=&ticker=000521&beginDate=20020101&endDate=20150828'
        code, result = client.getData(url1)
        if code == 200:
            print result
        else:
            print code
            print result
        url2 = '/api/subject/getThemesContent.csv?field=&themeID=&themeName=&isMain=1&themeSource='
        code, result = client.getData(url2)
        if (code == 200):
            file_object = open('thefile.csv', 'w')
            file_object.write(result)
            file_object.close()
        else:
            print code
            print result
    except Exception, e:
        # traceback.print_exc()
        raise e
