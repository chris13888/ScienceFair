import wikipedia
import re
import spacy
from collections import Counter
import requests
from bs4 import BeautifulSoup, SoupStrainer
import random

strip = re.compile('<.*?>')
nlp = spacy.load('en_core_web_lg')

form_html = '''<form>
  <table>
    <tr>
      <td class="author-name">
        Author Name<br>
        <span style="font-size: 0.7em;">(Lastname, Firstname)</span>
      </td>
      <td class="article-name">
        Article Name<br>
        <span style="font-size: 0.7em;">(Name of the Article)</span>
      </td>
      <td class="site-name">
        Site Name<br>
        <span style="font-size: 0.7em;">(Name of the Website)</span>
      </td>
      <td class="url">
        URL<br>
        <span style="font-size: 0.7em;">(Uniform Resource Locator)</span>
      </td>
    </tr>
    <tr>
      <td><input class="input author-field" value="{}"/></td>
      <td><input class="input article-field" value="{}"/></td>
      <td><input class="input site-field" value="{}"/></td>
      <td><input class="input url-field" value="{}"/></td>
    </tr>
  </table>
  <div></div>
  <button type="button" onclick="add(this);" class="button cbutton">Add Author</button>
  <button type="button" onclick="delet(this);" class="button cbutton">Remove Author</button>
  <button type="button" onclick="cite(this);" class="button cbutton">Generate Citation</button>
</form>'''

def modify_stop(nlp, word_list):
    for word in word_list:
        nlp.vocab[word].is_stop = True

modify_stop(nlp, ['the', 'a', 'an'])

def get_article(topic):
    try:
        return wikipedia.page(wikipedia.search(topic)[0])
    except wikipedia.DisambiguationError as e:
        try:
            return wikipedia.page(e.options[0])
        except:
            return wikipedia.page(random.choice(e.options))

def clean(text):
    text = re.sub(r'\[.+?\]', r' ', text)
    text = re.sub(r'\(listen\)', r' ', text)
    text = re.sub(r'(\s)\s+?', '\g<1>', text)
    return text

def summarize(text, top=2):
    doc = nlp(text)
    words = Counter([i.text for i in doc if i.is_alpha and not i.is_stop]) # Find the count of each word.

    try: highest_freq = words.most_common(1)[0][1] # Get the frequency of the most commonly appearing word.
    except: return 'no summary available.'
    scores = [] # The array of scores for each phrase.
    for sent in doc.sents:
        if len(sent) > 25:
            continue
        score = 0
        for tok in sent:
            score += words.get(tok.text, 0)/highest_freq
        scores.append((sent.text, score))

    scores = sorted(scores, key = lambda x: -x[1]) # Sort descending.
    return ('\n'.join([i[0] for i in scores[:top]])) # Return the top few sentences joined with a newline.

def chunks(text, top=4):
    doc = nlp(text)
    words = Counter([i.text for i in doc if i.is_alpha and not i.is_stop]) # Find the count of each word.

    try: highest_freq = words.most_common(1)[0][1] # Get the frequency of the most commonly appearing word.
    except: return ['no noun chunks available']
    scores = [] # The array of scores for each phrase.
    for chunk in doc.noun_chunks:
        score = 0
        for tok in chunk:
            score += words.get(tok.text, 0)/highest_freq
        scores.append((chunk.text, score))
    scores = sorted(scores, key = lambda x: x[1]) # Sort descending.
    return [i[0] for i in scores[:top]] # Return the top few noun chunks.

def get_article_soup(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def get_article_text(soup):
    text = ''
    for i in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h4', 'h5', 'h6', 'p']):
        text += re.sub(strip, '', str(''.join([str(z) for z in i.contents])).replace('<br>', '\n')) +'\n'
    return text

def get_article_title(soup):
    try: return soup.find_all(['h1'])[0].get_text().strip()
    except: return 'unknown title'

def get_website(soup, url):
    try:
        return soup.find("meta",  property="og:site_name")['content']
    except:
        thing = re.sub(r'/{2,}', r'/', url).split('/')
        if thing[0].startswith('http'):
            thing = thing[1]
        else:
            thing = thing[0]
        thing = thing.replace('www.', '')
        thing = re.sub(r'[\-_]', r' ', thing)
        thing = ' '.join(thing.split('.')[:-1]).title()
        return thing

def get_article_author(html, text=None):
    if text == None:
        text = get_article_text(BeautifulSoup(html, 'html.parser'))

    free = re.sub(strip, '', html)
    # print(free)
    try:
        match = re.search(r'[Bb][Yy] +(.+)\n', free)
        if len(match.group(1)) > 50:
            raise Exception('No way the name could be *that* long.')
        return [match.group(1)]
    except:
        pass

    a = []
    for entity in nlp(text).ents:
        if entity.label_ == 'PERSON':
            a.append(entity.text)
    z = Counter(a).most_common()
    try: smol = z[-1][1]
    except: return ['no_names_found']
    a = []
    for thing in z:
        if smol == thing[1]:
            if ' ' in thing[0]:
                a.append(thing)
    return a

def return_html(topic):
    html = ''
    article = get_article(topic)
    text = clean(article.summary)
    html += f'<h2>Wikipedia Page: <a href="{article.url}">{article.title}</a></h2>'
    html += f'<h2>Summary of Wikipedia article: </h2><p>{summarize(text, 3)}</p>'
    html += f'<h2>Useful search phrases: </h2><p>{", ".join(chunks(text, 6))}</p>'
    references = article.references
    html += f'<h2>Useful References: </h2>'
    for i in range(min(len(references), 5)):
        try:
            url = references[i]
            thing = get_article_soup(url)
            cleaned = get_article_text(thing)
            website_name = get_website(thing, url)
            article_title = get_article_title(thing)
            html += f'<p>{website_name}\'s article, <a href="{url}">{article_title}</a><br>'
            try: author = get_article_author[0]
            except: author = 'no_names_found'
            if author == 'no_names_found':
                author = ''
            html += f'{form_html.format(", ".join(author.split(" ")[::-1]), article_title, website_name, url)}</p>'
        except:
            continue
    return html


# Sample Program: Uncomment to test out!
# article = get_article('Apollo 8')
#
# text = clean(article.summary)
#
# print(summarize(text, 3))
# print(chunks(text, 5))

# Sample Program: Uncomment to test out!
# url = 'https://www.nj.com/rutgersfootball/index.ssf/2008/11/big_east_bowl_picture_and_rutg.html'
# a = get_article_soup(url)
# t = get_article_text(a)
# print(get_article_title(a))
# print(get_website(a, url))
# print(get_article_author(t))
