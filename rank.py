import requests
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import random
import validators
from wordcloud import WordCloud
import xlsxwriter


def get_links(starting: str):
    try:
        page = requests.get(starting)
    except requests.ConnectionError:
        return []
    parent = BeautifulSoup(page.text, 'lxml')

    hrefs = set()
    for tag in parent.find_all('a'):
        if tag.has_key('href'):
            link = tag['href']
            if validators.url(link):  # and link not in hrefs and 'instagram' not in link and 'facebook' not in link and 'twitter' not in link and 'linkedin' not in link:
                hrefs.add(link)
    hrefs = list(hrefs)
    random.shuffle(hrefs)
    return hrefs


def domain_cloud(domains):
    """
	Draw the cloud of words
	Args:
		domains (list of str): ['domain1', 'domain2'...]
	"""

    word_string = ' '.join(domains)
    params = dict(background_color="white", width=1200, height=1000, max_words=len(set(domains)))
    wordcloud = WordCloud(**params).generate(word_string)
    plt.imshow(wordcloud)
    plt.show()


def graph(connections, with_labels=True):
    """
	Draw the graph based on a connections
	Args:
		connections (list of tuple): [(A, B), (B, C)...] links from A to B, B to C, etc
		with_labels (bool): plot the labels or not
	"""


    print(connections)
    g = nx.DiGraph()
    #g = nx.Graph()
    #g.add_node(root_url)
    g.add_edges_from(connections)
    nx.draw(g, verticalalignment='bottom', horizontalalignment='center', with_labels=with_labels, node_size=30)
    plt.show()


if __name__ == '__main__':

    #limit = 100
    start = 'https://whataweek.ru'
    g = nx.DiGraph()
    g.add_node(start)

    parent = start
    connections = []
    hrefs = get_links(parent)
    childs = []
    for href in hrefs:
        childs.append(href)
    for child in childs:
        #connections.append(tuple([parent, child]))
        g.add_node(child)
        g.add_edge(parent, child)

        parent2 = child
        hrefs = get_links(parent2)
        childs = []
        for href in hrefs:
            childs.append(href)
        for child in childs:
            #connections.append(tuple([parent2, child]))
            g.add_node(child)
            g.add_edge(parent2, child)
            parent3 = child
            hrefs = get_links(parent3)
            childs = []
            for href in hrefs:
                childs.append(href)
            for child in childs:
                #connections.append(tuple([parent3, child]))
                g.add_node(child)
                g.add_edge(parent3, child)
                parent4 = child
                hrefs = get_links(parent4)
                childs = []
                for href in hrefs:
                    childs.append(href)

                for child in childs:
                    # connections.append(tuple([parent3, child]))
                    g.add_node(child)
                    g.add_edge(parent4, child)

    pagerank = nx.pagerank_numpy(g, alpha=0.85, personalization=None, weight='weight', dangling=None)
    print(g.nodes())
    result = []
    for node in g.nodes():
        print(node, pagerank.get(node))
        result.append([node, pagerank.get(node)])
    #edgeNumber = g.number_of_edges()
    #nodeNumber = g.number_of_nodes()
    nodesize = [g.degree(n) * 5 for n in g]
    pos = nx.spring_layout(g)

    nx.draw(g, with_labels=False, node_size=nodesize)
    #nx.draw_networkx_nodes(g, pos, node_size=nodesize, node_color='r')
    #nx.draw_networkx_edges(g, pos)
    #plt.figure(figsize=(5, 5))
    plt.show()
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    column = 0
    for i in result:
        row += 1
        column = 0
        for j in i:
            worksheet.write(row, column, j)
            column += 1
    workbook.close()
    # nx.draw(g, with_labels=False)
    # plt.show()


    # start = 'https://www.youtube.com'
    # domains = []
    # connections = []
    # q = [start]
    # i = 0
    # while len(domains) < limit:
    #     parent = q[i]
    #     #print(parent)
    #     hrefs = get_links(parent)
    #     childs = []
    #     for href in hrefs:
    #         if href not in q and len(childs) < 5:
    #             childs.append(href)
    #         domains.append(parent.split('//')[1].split('/')[0])
    #     for child in childs:
    #         connections.append(tuple([parent, child]))
    #     q += childs
    #     i += 1


    # print(domains)
    #graph(connections, with_labels=False)
    #domain_cloud(domains)
