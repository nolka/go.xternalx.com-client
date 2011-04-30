# -*- coding: utf8 -*-

from utils.apimanager import ApiManager
import sys
import options

def CommandExists(cmd):
    if cmdList.has_key(cmd):
        return True
    else:
        return False
    

def SendRequest(params):
    a = ApiManager(options.USER_ID, options.USER_SECRET)
    result = a.Request(params)
    if not result['error']:
        return result
    else:
        print "Request error occurs\nCode:%d\nMessage: %s" % (result['code'], result['message'])
        return
    

def TestConnection(args):
    SendRequest({'act': 'test'})
    

def ShortenUrl(args):
    r = None
    if len(args) == 3:
        r = SendRequest({"act": args[0], 'content': args[1], 'pwd': args[2]})
        
    if len(args) == 2:
        r = SendRequest({"act": args[0], 'content': args[1],})
    
    if r != None and r['error'] == 0:
        for item in r['items']:
            print "source url %s was shorted to %s" % (item['source'], item['url'])
    

def DeleteUrl(args):
    r = None
    if len(args) == 2:
        r = SendRequest({"act": args[0], 'content': args[1],})
        if r != None and r['error'] == 0:
            for item in r['items']:
                print "url %s was deleted" % (item['source'])
    else:
        print "insuffucient args"

def ShortenContent(args):
    pass
    

def ExecuteCommand(cmd, args):
    cmdList[cmd]['func'](args)
    

cmdList = {
            'test':             {
                                    'func': TestConnection, 
                                    'desc': 'Test connection to api',
                                    'usage': sys.argv[0]+' test',
                                },
            'url.shorten':      {
                                    'func': ShortenUrl, 
                                    'desc': 'Create short url',
                                    'usage': sys.argv[0]+' url.shorten url [password]',
                                },
            'url.delete':       {
                                    'func': DeleteUrl, 
                                    'desc': 'Delete url with id specified',
                                    'usage': sys.argv[0]+' url.delete url_id',
                                },
            'content.shorten': 
                                {
                                    'func': ShortenContent, 
                                    'desc': 'Create short url for content',
                                    'usage': sys.argv[0]+' content.shorten content [password]',
                                }
            }
