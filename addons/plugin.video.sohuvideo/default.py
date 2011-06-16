﻿# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, httplib, re, string, sys, os, gzip, StringIO

# 搜狐视频(SoHu) by taxigps, 2011
#Modified by wow1122/wht9000@gmail.com
# Plugin constants 
__addonname__ = "搜狐视频(SoHu)"
__addonid__ = "plugin.video.sohuvideo"
__addon__ = xbmcaddon.Addon(id=__addonid__)

RATE_LIST = [['超清','3'], ['高清','2'], ['普通','1'], ]
CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['综艺','7'], ['纪录片','8'], ['动漫','16'], ['音乐','24'], ['教育','21'], ['播客','9001'], ['视频新闻','13']]
ORDER_LIST = [['0','相关程度'], ['3','最新发布'], ['4','评分最高'], ['1','总播放最多'],['5','日播放最多'], ['7','周播放最多']]
ORDER_LIST1 = [['0','相关程度'], ['3','最新发布'], ['1','总播放最多']]
ORDER_LIST2 = [['0','相关程度'], ['3','最新发布'], ['1','总播放最多'],['5','日播放最多'], ['7','周播放最多']]
def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
        httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    response.close()
    match = re.compile('<meta http-equiv="[Cc]ontent-[Tt]ype" content="text/html; charset=(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata=httpdata.decode('gbk', 'ignore').encode('utf8')
            #httpdata = unicode(httpdata, charset).encode('utf8')
    return httpdata
   
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def rootList():
    for name, id in CHANNEL_LIST:
        li=xbmcgui.ListItem(name)
        u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus("")+"&area="+urllib.quote_plus("")+"&year="+urllib.quote_plus("-1")+"&order="+urllib.quote_plus("0")+"&page="+urllib.quote_plus("1")+"&p5="+urllib.quote_plus("")+"&p6="+urllib.quote_plus("")+"&p11="+urllib.quote_plus("")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def getcatList(listpage):
    match = re.compile('<li><span>类型：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    catlist = re.compile('p2(.+?)_p3.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(catlist)>0: catlist.insert(0,['0','全部'])
    return catlist

def getareaList(listpage):
    match = re.compile('<li><span>产地：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    arealist = re.compile('p3(_.+?)_p4.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(arealist)>0: arealist.insert(0,['0','全部'])
    return arealist

def getyearList(listpage):    
    match = re.compile('<li><span>年份：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    yearlist = re.compile('p4(.+?)_p5.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(yearlist)>0: yearlist.insert(0,['0','全部'])
    return yearlist

def getList16(listpage):    
    match = re.compile('<li><span>篇幅：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    pflist = re.compile('p5(.+?)_p6.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(pflist)>0: pflist.insert(0,['0','全部'])
    match = re.compile(' <li><span>年龄：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    nllist = re.compile('p6(.+?)_p7.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(nllist)>0: nllist.insert(0,['0','全部'])
    return pflist,nllist
           
def getList24(listpage):
    match = re.compile('<li><span>类型：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    lxlist = re.compile('p5(.+?)_p6.+?html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(lxlist)>0: lxlist.insert(0,['0','全部'])
    match = re.compile('<li><span>歌手：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    gslist = re.compile('p6(.+?)_p7.+?html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(gslist)>0: gslist.insert(0,['0','全部'])
    match = re.compile('<li><span>语言：.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    yylist = re.compile('p11(.+?).html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(yylist)>0: yylist.insert(0,['0','全部'])
    match = re.compile('<li><span>地区：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    arealist = re.compile('p3(_.+?)_p4.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(arealist)>0: arealist.insert(0,['0','全部'])
    return lxlist,gslist,yylist,arealist
    
def progList(name,id,page,cat,area,year,p5,p6,p11,order):
    url = 'http://so.tv.sohu.com/list_p1'+id+'_p2'+cat+'_p3'+area+'_p4'+year+'_p5'+p5+'_p6'+p6+'_p7'+order+'_p82_p9_2d1_p10'+page+'_p11'+p11+'.html'
    print url
    currpage = int(page)
    link = GetHttpData(url)
    match = re.compile('共有 <span>(.+?)</span> 个符合条件', re.DOTALL).findall(link)
    if match[0]=='0':
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '没有符合此条件的视频！')
    else:
        if currpage==1:match = re.compile('<div class="jumpA clear">\s*<div class="r">上一页(.+?)<a href=').findall(link)
        else:match = re.compile('<div class="jumpA clear">\s*<div class="r">.+?</a>(.+?)<a href=').findall(link)
        if len(match):
            totalpages = int(match[0].split('/')[1])
        else:
            totalpages = 1
        match = re.compile('<div class="seaKey bord clear" id="seaKey">(.+?)<div class="jumpA clear">', re.DOTALL).findall(link)
        if len(match):
            listpage = match[0]
        else:
            listpage = ''
        match = re.compile('<div class="vInfo">(.+?)</em></p>', re.DOTALL).findall(link)
        totalItems = len(match) + 1
        if currpage > 1: totalItems = totalItems + 1
        if currpage < totalpages: totalItems = totalItems + 1
        lxstr=''
        if id!='13':
            catlist= getcatList(listpage)
            if cat:
                lxstr = lxstr+searchDict(catlist,cat)
            elif id=='24':
                lxstr = lxstr+'全部风格'
            else:    
                lxstr = lxstr+'全部类型'
            if id in ('1','2','7'):          
                arealist= getareaList(listpage)
                if area:
                    lxstr = lxstr+'/'+searchDict(arealist,area)
                else:
                    lxstr = lxstr+'/全部地区'
            if id in ('1','2','16','24'):
                yearlist = getyearList(listpage)
                if year=='-1':
                    lxstr = lxstr+'/全部年份'
                elif year in ('80','90'):
                    lxstr = lxstr+'/'+year+'年代'
                elif year == '100':
                    lxstr = lxstr+'/更早年代'
                else:
                    lxstr = lxstr+'/'+year+'年'
            if id=='16':
                pflist,nllist=getList16(listpage)
                if p5:
                    lxstr = lxstr+'/'+searchDict(pflist,p5)
                else:
                    lxstr = lxstr+'/全部篇幅'        
                if p6:
                    lxstr = lxstr+'/'+searchDict(nllist,p6)
                else:
                    lxstr = lxstr+'/全部年龄'
            if id=='24': 
                lxlist,gslist,yylist,arealist=getList24(listpage)
                if p5:
                    lxstr = lxstr+'/'+searchDict(lxlist,p5)
                else:
                    lxstr = lxstr+'/全部类型'            
                if p6:
                    lxstr = lxstr+'/'+searchDict(gslist,p6)
                else:
                    lxstr = lxstr+'/全部歌手'
                if p11:
                    lxstr = lxstr+'/'+searchDict(yylist,p11)
                else:
                    lxstr = lxstr+'/全部语言'
                if area:
                    lxstr = lxstr+'/'+searchDict(arealist,area)
                else:
                    lxstr = lxstr+'/全部地区'
            li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + lxstr + '/' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
            u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&listpage="+urllib.quote_plus(listpage)+"&p5="+urllib.quote_plus(p5)+"&p6="+urllib.quote_plus(p6)+"&p11="+urllib.quote_plus(p11)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
        for i in range(0,len(match)):
            match1 = re.compile('<a href="(.+?)" target="_blank">\s*<img src="(.+?)".+? target="_blank">(.+?)</a>', re.DOTALL).search(match[i])
            p_url = match1.group(1)
            p_thumb = match1.group(2)
            p_name = match1.group(3)
            match1 = re.compile('<span class="commet">\(([0-9]+)人评价\)</span><span class="grade"><font>([0-9]*)</font>([\.0-9]*).*?</span>').search(match[i])
            if match1:
                p_rating = float(match1.group(2) + match1.group(3))
                p_votes = match1.group(1)
            else:
                p_rating = 0
                p_votes = ''
            match1 = re.compile('导演：.+?</font>(.+?)</a>').search(match[i])
            if match1:
                p_director = match1.group(1)
            else:
                p_director = ''
            print p_director
            match1 = re.compile('<span class="show">类型：(.+?</span>)').search(match[i])
            if match1:
                match0 = re.compile('<font class="highlight"></font>([^<]+)').findall(match1.group(1))
                p_genre = ' / '.join(match0)
            else:
                p_genre = ''
            match1 = re.compile('<p class="detail">(.+?)(</p>|</b>)').search(match[i])
            if match1:
                p_plot = re.sub('<b id=.*?>','',match1.group(1))
            else:
                p_plot = ''
            match1 = re.compile('<font>年份：<a href="\?c=1&year=([0-9]+)">').search(match[i])
            if match1:
                p_year = int(match1.group(1))
            else:
                p_year = 0
            #if match[i].find('.shtml')>0:
            if id in ('2','16'):
                p_dir = True
                mode = 2
            else:
                p_dir = False
                mode = 3
            if id=='9001':mode=5
            if match[i].find('<span class="cq_ico">')>0:
                p_name1 = p_name + '[超清]'
                p_res = 2
            elif match[i].find('<span class="gq_ico">')>0:
                p_name1 = p_name + '[高清]'
                p_res = 1
            else:
                p_name1 = p_name
                p_res = 0
            li = xbmcgui.ListItem(str(i + 1) + '.' + p_name1, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&id="+urllib.quote_plus(str(i))
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, p_dir, totalItems)
    
        if currpage > 1:
            li = xbmcgui.ListItem('上一页')
            u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
        if currpage < totalpages:
            li = xbmcgui.ListItem('下一页')
            u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,id,url,thumb):
    print url
    link = GetHttpData(url)
    if url.find('.shtml')>0:
        match0 = re.compile('var vrs_playlist_id="(.+?)";', re.DOTALL).findall(link)
        link = GetHttpData('http://hot.vrs.sohu.com/vrs_videolist.action?playlist_id='+match0[0])
        match = re.compile('"videoImage":"(.+?)",.+?"videoUrl":"(.+?)".+?"videoOrder":"(.+?)",', re.DOTALL).findall(link)
        totalItems = len(match)
        for p_thumb,p_url,p_name in match:
            li = xbmcgui.ListItem('第'+p_name+'集', iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus('第'+p_name+'集') + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)       
    else:    
        match0 = re.compile('var pid=(.+?);', re.DOTALL).findall(link)
        if match0:
            pid=match0[0].replace('"','')
            match0 = re.compile('var vid=(.+?);', re.DOTALL).findall(link)
            vid=match0[0].replace('"','')
            match0 = re.compile('var obType = (.+?);', re.DOTALL).findall(link)
            obtype= match0[0].replace('"','')  
            #match0 = re.compile('var ps = (.+?);', re.DOTALL).findall(link)
            #ps= match0[0]     
            link = GetHttpData("http://search.vrs.sohu.com/avs_i"+vid+"_pr"+pid+"_o"+obtype+"_n_p1000_chltv.sohu.com.json")
            match = re.compile('"videoName":"(.+?)",.+?"videoUrl":"(.+?)",.+?"videoBigPic":"(.+?)",', re.DOTALL).findall(link)
            totalItems = len(match)
            for p_name,p_url, p_thumb  in match:
                li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
                u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
                #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        else:
            match = re.compile('<a href="(http://tv.sohu.com/\d{8}/n\d{9}.shtml)".+?><img.+?src="(.+?)".+?(第\d+集)', re.I).findall(link)
            totalItems = len(match)
            for p_url,p_thumb,p_name  in match:
                li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
                u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
                #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb):
    print url
    link = GetHttpData(url)
    print 'PlayVideo'+url
    match1 = re.compile('var vid="(.+?)";').search(link)
    if not match1:
        match1 = re.compile('<a href="(http://[^/]+/[0-9]+/[^\.]+.shtml)" target="?_blank"?><img').search(link)
        if match1:
            PlayVideo(name,match1.group(1),thumb)
        return
    p_vid = int(match1.group(1))
    link = GetHttpData('http://search.vrs.sohu.com/mv_i'+str(p_vid)+'.json')
    match = re.compile('"playlistId":(.+?),"').findall(link)
    link = GetHttpData('http://hot.vrs.sohu.com/vrs_videolist.action?playlist_id='+match[0])
    match = re.compile('"videoId":(.+?),"').findall(link)
    p_vid = match1.group(1)
    link = GetHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+p_vid)
    match = re.compile('"norVid":(.+?),"highVid":(.+?),"superVid":(.+?),').search(link)
    ratelist=[]
    if match.group(3)!='0':ratelist.append(['超清','3'])
    if match.group(2)!='0':ratelist.append(['高清','2'])
    if match.group(1)!='0':ratelist.append(['流畅','1'])
    dialog = xbmcgui.Dialog()
    list = [x[0] for x in ratelist]
    if len(ratelist)==1:
        rate=ratelist[0][1]
    else:
        sel = dialog.select('类型', list)
        if sel == -1:
            return
        else:
            rate=ratelist[sel][1]
    if match.group(int(rate))<>str(p_vid):link = GetHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+match.group(int(rate)))
    match = re.compile('"tvName":"(.+?)"').findall(link)
    name = match[0]
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    paths = match[0].split('","')
    match = re.compile('"su"\:\["(.+?)"\]').findall(link)
    newpaths = match[0].split('","')
    playlist = xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(paths)):
        link = GetHttpData('http://220.181.61.229/?prot=2&file='+paths[i].replace('http://data.vod.itc.cn','')+'&new='+newpaths[i])
        key=link.split('|')[3]
        req = httplib.HTTPConnection("new.sohuv.dnion.com")
        req.request("GET", newpaths[i]+'?key='+key)
        r1 = req.getresponse()
        #print r1.getheader('Location')
        listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(paths))+" 节"})
        playlist.add(r1.getheader('Location'), listitem)
    xbmc.Player().play(playlist)

def PlayBoKe(name,url,thumb):
    link = GetHttpData(url)
    print 'PlayVideo:'+url
    match = re.compile('var _videoId = (.+?);', re.DOTALL).findall(link)
    print match[0]
    link = GetHttpData('http://my.tv.sohu.com/videinfo.jhtml?m=viewtv&vid='+match[0])
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    paths=match[0].split('","')
    print link
    match = re.compile('"su"\:\["(.+?)"\]').findall(link)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    if len(match)>3:
        for i in range(0,len(paths)):
            newpaths = match[0].split('","')
            link = GetHttpData('http://data.vod.itc.cn/?prot=2&file='+paths[i]+'&new='+newpaths[i])
            key=link.split('|')[3]
            req = httplib.HTTPConnection("new.sohuv.dnion.com")
            req.request("GET", newpaths[i]+'?key='+key)
            r1 = req.getresponse()
            listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(paths))+" 节"})
            playlist.add(r1.getheader('Location'), listitem)
        xbmc.Player().play(playlist)
    else:
        for i in range(0,len(paths)):
            listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(paths))+" 节"})
            playlist.add('http://'+paths[i], listitem)
            print paths[i]
        xbmc.Player().play(playlist)    
    #print r1.getheader('Location')
    #listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
    #listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(paths))+" 节"})
    #playlist.add(r1.getheader('Location'), listitem)
    
    
def performChanges(name,id,listpage,cat,area,year,order,p5,p6,p11):
    change = False
    catlist= getcatList(listpage)
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            if sel == 0:
                cat = ''
            else:
                cat = catlist[sel][0]
            change = True
    if id in ('1','2','7'):
        arealist=getareaList(listpage)
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                if sel == 0:
                    area = ''
                else:
                    area = arealist[sel][0]
                change = True       
    if id in ('1','2','16','24'):
        yearlist=getyearList(listpage)
        if len(yearlist)>0:
            list = [x[1] for x in yearlist]
            sel = dialog.select('年份', list)
            if sel != -1:
                if sel == 0:
                    year = '-1'
                else:
                    year = yearlist[sel][0]
                change = True
    if id=='16':
        pflist,nllist=getList16(listpage)
        if len(pflist)>0:
            list = [x[1] for x in pflist]
            sel = dialog.select('篇幅', list)
            if sel != -1:
                if sel == 0:
                    p5 = ''
                else:
                    p5 = pflist[sel][0]
                change = True 
        if len(nllist)>0:
            list = [x[1] for x in nllist]
            sel = dialog.select('年龄', list)
            if sel != -1:
                if sel == 0:
                    p6 = ''
                else:
                    p6 = nllist[sel][0]
                change = True
    if id=='24': 
        lxlist,gslist,yylist,arealist=getList24(listpage)
        if len(lxlist)>0:
            list = [x[1] for x in lxlist]
            sel = dialog.select('类型', list)
            if sel != -1:
                if sel == 0:
                    p5 = ''
                else:
                    p5 = lxlist[sel][0]
                change = True         
        if len(gslist)>0:
            list = [x[1] for x in gslist]
            sel = dialog.select('歌手', list)
            if sel != -1:
                if sel == 0:
                    p6 = ''
                else:
                    p6 = gslist[sel][0]
                change = True 
        if len(yylist)>0:
            list = [x[1] for x in yylist]
            sel = dialog.select('语言', list)
            if sel != -1:
                if sel == 0:
                    p11 = ''
                else:
                    p11 = yylist[sel][0]
                change = True 
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                if sel == 0:
                    area = ''
                else:
                    area = arealist[sel][0]
                change = True 
    if id=='9001':
        list = [x[1] for x in ORDER_LIST1]
    elif id=='13':
        list = [x[1] for x in ORDER_LIST2]
    else:
        list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        if id=='9001':order = ORDER_LIST1[sel][0]
        elif id=='13':order = ORDER_LIST2[sel][0]
        else:order = ORDER_LIST[sel][0]
        change = True
    if change:
        progList(name,id,'1',cat,area,year,p5,p6,p11,order)

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

params = get_params()
mode = None
name = None
id = None
cat = ''
area = ''
year = ''
order = ''
page = ''
p5 = ''
p6 = ''
p11 = ''
listpage = ''
url = None
thumb = None

try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    listpage = urllib.unquote_plus(params["listpage"])
except:
    pass
try:
    p5 = urllib.unquote_plus(params["p5"])
except:
    pass
try:
    p6 = urllib.unquote_plus(params["p6"])
except:
    pass
try:
    p11 = urllib.unquote_plus(params["p11"])
except:
    pass
try:
    order = urllib.unquote_plus(params["order"])
except:
    pass
try:
    year = urllib.unquote_plus(params["year"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
except:
    pass
try:
    cat = urllib.unquote_plus(params["cat"])
except:
    pass
try:
    id = urllib.unquote_plus(params["id"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode == None:
    rootList()
elif mode == 1:
    progList(name,id,page,cat,area,year,p5,p6,p11,order)
elif mode == 2:
    seriesList(name,id,url,thumb)
elif mode == 3:
    PlayVideo(name,url,thumb)
elif mode == 4:
    performChanges(name,id,listpage,cat,area,year,order,p5,p6,p11)
elif mode == 5:
    PlayBoKe(name,url,thumb)
