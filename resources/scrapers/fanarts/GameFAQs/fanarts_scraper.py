﻿# -*- coding: UTF-8 -*-

import os
import re
import urllib2
from xbmcaddon import Addon

# Get Game first page
def _get_game_page_url(system,search):
    platform = _system_conversion(system)
    game = search.replace(' ', '+').lower()
    games = []
    try:
        req = urllib2.Request('http://www.gamefaqs.com/search/index.html?platform='+platform+'&game='+game+'&s=s')
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        search_page = urllib2.urlopen(req)
        for line in search_page.readlines():
            if '>Images</a></td>' in line:
                games.append(re.findall('<td><a class="sevent_(.*?)" href="(.*?)">Images</a></td>', line.replace('\r\n', '')))
        if games:
            return ''.join(games[0][0][1])
    except:
        return ""

# Fanarts list scrapper
def _get_fanarts_list(system,search,imgsize):
    full_fanarts = []
    game_id_url = _get_game_page_url(system,search)
    try:
        req = urllib2.Request('http://www.gamefaqs.com'+game_id_url+'?page=0')
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        game_page = urllib2.urlopen(req)
        if game_page:
            for line in game_page.readlines():
                if 'pod game_imgs' in line:
                    fanarts = re.findall('b"><a href="(.*?)"><img src="(.*?)"', line)
                    for index, item in enumerate(fanarts):
                        full_fanarts.append((item[0],item[1],'Image '+str(index)))
        return full_fanarts
    except:
        return full_fanarts

# Get Fanart scrapper
def _get_fanart(image_url):
    images = []
    try:
        req = urllib2.Request('http://www.gamefaqs.com' + image_url)
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        search_page = urllib2.urlopen(req)
        for line in search_page.readlines():
            if 'pod game_imgs' in line:
                images = re.findall('g"><a href="(.*?)"', line)
                return images[0]
    except:
        return ""

# Game systems DB identification
def _system_conversion(system_id):
    try:
        rootDir = Addon( id="plugin.program.advanced.launcher" ).getAddonInfo('path')
        if rootDir[-1] == ';':rootDir = rootDir[0:-1]
        resDir = os.path.join(rootDir, 'resources')
        scrapDir = os.path.join(resDir, 'scrapers')
        csvfile = open( os.path.join(scrapDir, 'gamesys'), "rb")
        conversion = []
        for line in csvfile.readlines():
            result = line.replace('\n', '').replace('"', '').split(',')
            if result[0].lower() == system_id.lower():
                if result[2]:
                    platform = result[2]
                    return platform
    except:
        return ''

