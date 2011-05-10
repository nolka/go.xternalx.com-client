# -*- coding: utf8 -*-

import urllib, httplib
import md5
import xml.etree.cElementTree as ET

##
# Класс, который будет отправлять запросы к API, и обрабатывать его ответы
class ApiManager:
    
    UserId      = ""
    UserSecret  = ""
    
    __headers = {"Accept": "text/plain"}
    
    def __init__(self, userId, userHash):
        self.UserId     = userId
        self.UserSecret = userHash

    ##
    # функция, отправляющая запрос к api
    # @param params словарь с параметрами запроса
    # @return словарь с результатами запроса
    def Request(self, params):
        params['user'] = self.UserId
        params['hash'] = self.__getMd5(params)
        
        # преобразуем  словарь в строку запроса
        params = urllib.urlencode(params)
        conn = httplib.HTTPConnection('go.xternalx.com')
        conn.request('GET', '/api/?%s' % params, "", self.__headers)
        response = conn.getresponse()
        # если запрос успешен, будем парсить его
        if response.status == 200:
            return self.__parseResponse(response.read())
        else:
            print "Could not send request, server return error %d" % request.status
            
    
    ##
    # функция, генерирующая md5 хэш по значениям словаря, упорядоченного по ключам
    #   в алфавитном порядке по возрастанию
    # @param params словарь значений
    # @return строка, содержащая m5 хэш
    def __getMd5(self, params):
        sortedKeys = params.keys()
        sortedKeys.sort()
        toSign = ""
        
        for key in sortedKeys:
            toSign += params[key]
        
        toSign += self.UserSecret
        
        m = md5.new()
        m.update(toSign)
        return m.hexdigest()
    
    ##
    # функция - парсер xml ответа в словарь
    # @param xmkString xmk ответ от api
    # @return словарь, представляюший из себя представление ответа api
    def __parseResponse(self, xmlString):
        xml = ET.fromstring(xmlString)
        # если ошибка, создаем словарь с информацией о ней, и отдаем
        if int(xml.attrib['iserror']) == 1:
            result =    {
                            'error': True,
                            'message': xml.findtext('message'),
                            'code': int(xml.findtext('code'))
                        }
            return result
        # иначе преобраем ответ в словарь
        else:
            result =    {
                            'error': False,
                            # список результатов запроса к api
                            'items': []
                        }
            # проходим по каждому элементу в xml (/reply/item)
            for itemNode in xml.iter('item'):
                itemData = {}
                """
                тип элемента
                при создании ссылок это linkData,
                при уалении ссылок это deleted
                """
                itemData['type'] = itemNode.attrib['type']
                for param in itemNode.iter('param'):
                    itemData[param.attrib['key']] = param.text
                    
                """
                если возвращенный запросом item является типом linkData,
                добавляем к словарю поле url,  в котором хранится короткая ссылка на оригинал
                """
                if itemData['type'] == 'linkData': 
                    itemData['url'] = "http://go.xternalx.com/%s/" % itemData['id']
                    
                result['items'].append(itemData)
            return result

