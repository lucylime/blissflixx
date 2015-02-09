from chanutils import get_doc, select_one, select_all

_SEARCH_URL = 'http://www.bbc.co.uk/iplayer/search'

_feedlist = [
  {'title':'Most Popular','url':'http://www.bbc.co.uk/iplayer/group/most-popular'},
  {'title':'Arts','url':'http://www.bbc.co.uk/iplayer/categories/arts/all?sort=dateavailable'},
  {'title':'CBBC','url':'http://www.bbc.co.uk/iplayer/categories/cbbc/all?sort=dateavailable'},
  {'title':'CBeebies','url':'http://www.bbc.co.uk/iplayer/categories/cbeebies/all?sort=dateavailable'},
  {'title':'Comedy','url':'http://www.bbc.co.uk/iplayer/categories/comedy/all?sort=dateavailable'},
  {'title':'Documentaries','url':'http://www.bbc.co.uk/iplayer/categories/documentaries/all?sort=dateavailable'},
  {'title':'Drama & Soaps','url':'http://www.bbc.co.uk/iplayer/categories/drama-and-soaps/all?sort=dateavailable'},
  {'title':'Entertainment','url':'http://www.bbc.co.uk/iplayer/categories/entertainment/all?sort=dateavailable'},
  {'title':'Films','url':'http://www.bbc.co.uk/iplayer/categories/films/all?sort=dateavailable'},
  {'title':'Food','url':'http://www.bbc.co.uk/iplayer/categories/food/all?sort=dateavailable'},
  {'title':'History','url':'http://www.bbc.co.uk/iplayer/categories/history/all?sort=dateavailable'},
  {'title':'Lifestyle','url':'http://www.bbc.co.uk/iplayer/categories/lifestyle/all?sort=dateavailable'},
  {'title':'Music','url':'http://www.bbc.co.uk/iplayer/categories/music/all?sort=dateavailable'},
  {'title':'News','url':'http://www.bbc.co.uk/iplayer/categories/news/all?sort=dateavailable'},
  {'title':'Science & Nature','url':'http://www.bbc.co.uk/iplayer/categories/science-and-nature/all?sort=dateavailable'},
  {'title':'Sport','url':'http://www.bbc.co.uk/iplayer/categories/sport/all?sort=dateavailable'},
]

def get_name():
  return 'iPlayer'

def get_image():
  return 'icon.png'

def search(q):
  doc = get_doc(_SEARCH_URL, params={'q':q})
  return _extract(doc)

def showmore(link):
  doc = get_doc(link)
  return _extract(doc)

def get_feedlist():
  return _feedlist

def get_feed(idx):
  doc = get_doc(_feedlist[idx]['url'])
  return _extract(doc)

def _extract(doc):
  rtree = select_all(doc, 'li.list-item')
  results = []
  for l in rtree:
    a = select_one(l, 'a')
    if a is None:
      continue
    url = a.get('href')
    if not url.startswith('/iplayer'):
      continue
    url = "http://www.bbc.co.uk" + url

    pdiv = select_one(l, 'div.primary')
    idiv = select_one(pdiv, 'div.r-image')
    img = idiv.get('data-ip-src')

    sdiv = select_one(l, 'div.secondary')
    title = select_one(sdiv, 'div.title').text.strip()
    el = select_one(sdiv, 'div.subtitle')
    subtitle = None
    if el is not None:
      subtitle = el.text
    synopsis = select_one(sdiv, 'p.synopsis').text
    actions = None
    a = select_one(l, 'a.view-more-container')
    if a is not None:
      link = "http://bbc.co.uk" + a.get('href')
      actions = [{'label':'More Episodes', 'type':'showmore', 'link':link,
                'title': title}]
    results.append({ 'title':title, 'img':img, 'url':url,
                'subtitle':subtitle, 'synopsis':synopsis, 'actions':actions})
  return results