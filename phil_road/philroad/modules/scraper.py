from lxml.html import fromstring, tostring
import re
import urllib2


TEXT_XPATH = '//div[@id="mw-content-text"]/*[not(self::div or self::table or self::dl or self::h or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6)]'
INVALID_LINKS_XPATH = '//*/a[ancestor::i or ancestor::sub or ancestor::sup]'
LINK_XPATH = TEXT_XPATH + '[{0}]/descendant::a[{1}]'

PAREN1 = '\('
PAREN2 = '\)'
LINK_START_TAG = '<a '
LINK_END_TAG = '</a>'
HREF = 'href'

MATCH = 'match'
LOOP = 'loop'
DEAD_END = 'dead_end'
UNEXPECTED_ERROR = 'error'

RESULT_KEY = 'result'
ARTICLES_KEY = 'articles'
REPEATED_ARTICLE_KEY = 'repeated_article'

WIKIPEDIA_URL = 'http://en.wikipedia.org'
PHILOSOPHY = 'http://en.wikipedia.org/wiki/Philosophy'

OPENER = urllib2.build_opener()
OPENER.addheaders = [('User-agent', 'Mozilla/5.0')]


def get_to_phil(init_article):
    articles = [init_article]
    next_article = first_link(init_article)

    # Safe guard of 50, while it's possible that some paths could be more
    # than 50, it seems rather unlikely
    for _ in range(50):
        if next_article == PHILOSOPHY:
            articles.append(next_article)
            return {RESULT_KEY: MATCH, ARTICLES_KEY: articles}
        elif next_article in articles:
            articles.append(next_article)
            return {RESULT_KEY: LOOP, ARTICLES_KEY: articles, REPEATED_ARTICLE_KEY: next_article}
        elif next_article is None:
            return {RESULT_KEY: DEAD_END, ARTICLES_KEY: articles}

        articles.append(next_article)
        next_article = first_link(next_article)
    return {RESULT_KEY: UNEXPECTED_ERROR, ARTICLES_KEY: articles}


def first_link(article):
    text_num = 1
    link_num = 1
    found_match = False

    # Using urllib2 to handle redirects, because lxml can't
    response = OPENER.open(article)
    html = response.read()

    tree = fromstring(html)
    for text in tree.xpath(TEXT_XPATH):

        # Remove all links from the tree that are invalid
        for inv_links in text.xpath(INVALID_LINKS_XPATH):
            inv_links.drop_tree()

        text_marked = tostring(text)

        '''
        We've removed all the bogus links, but now we have to account for links
        in parenthesis. To handle this, we're going to count all the open and
        close braces before a link. If the two numbers aren't the same, then we
        know that the link will actually be inside a set of parenthesis.
        We're also keeping track of the parent text element and the link number
        so that we can easily jump to the link via XPATH and extract what we need.
        '''
        end_link_loc, paren1_count, paren2_count = 0, 0, 0
        beg_link_loc = text_marked.find(LINK_START_TAG)
        while beg_link_loc != -1:
            prelink = text_marked[end_link_loc:beg_link_loc]
            paren1_count += len(re.findall(PAREN1, prelink))
            paren2_count += len(re.findall(PAREN2, prelink))
            if paren1_count == paren2_count:
                found_match = True
                break

            end_link_loc = text_marked.find(LINK_END_TAG, beg_link_loc)
            beg_link_loc = text_marked.find(LINK_START_TAG, end_link_loc)
            link_num += 1

        if found_match:
            break

        link_num = 1
        text_num += 1

    if not found_match:
        return None
    else:
        link_xpath = str.format(LINK_XPATH, str(text_num), str(link_num))
        links = tree.xpath(link_xpath)

        # Should really only ever get one link unless something bad happened
        if len(links) != 1:
            return None
        else:
            # Links are not absolute, so add the base URL
            return WIKIPEDIA_URL + links[0].get(HREF)
