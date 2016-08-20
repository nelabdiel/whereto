#stuff we need.
import os
from flask import Flask, render_template, request, redirect, jsonify
import requests
from bokeh.util.string import encode_utf8
from bs4 import BeautifulSoup
import networkx as nx
from networkx.readwrite import json_graph

app = Flask(__name__)
app.vars = {}

#Index page
@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        url = 'http://nelabdiel.com'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        G = nx.Graph()
        wsite = [url]

        c = 0
        while c < 3:
            try:
                # Request content of site
                r = requests.get(wsite[c])
                soup = BeautifulSoup(r.content)
        
                # Find all links in site.
                rows = soup.find_all('a')
                for row in rows:
                    if ('http' in row.get('href')) or ('www.' in row.get('href')):
                        G.add_node(row.get('href'))
                        G.add_edge(url, row.get('href'))
                        #G.add_edge(wsite[c], row.get('href'))
                        #wsite.append(row.get('href'))
            except:
                pass
    
            # Move on to the next link on the list.
            finally:
                c = c+1
        
        app.vars['data'] = json_graph.node_link_data(G)
        #jsonify(G)
        
        html = render_template('index.html')
        
        return encode_utf8(html)
    
    else:
        url = request.form['url']
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        G = nx.Graph()
        wsite = [url]

        c = 0
        while c < 3:
            try:
                # Request content of site
                r = requests.get(wsite[c])
                soup = BeautifulSoup(r.content)
        
                # Find all links in site.
                rows = soup.find_all('a')
                for row in rows:
                    if ('http' in row.get('href')) or ('www.' in row.get('href')):
                        G.add_node(row.get('href'))
                        G.add_edge(url, row.get('href'))
                        #G.add_edge(wsite[c], row.get('href'))
                        #wsite.append(row.get('href'))
            except:
                pass
    
            # Move on to the next link on the list.
            finally:
                c = c+1
        
        app.vars['data'] = json_graph.node_link_data(G)
        #jsonify(G)
        
        html = render_template('index.html')
        
        return encode_utf8(html)

@app.route("/gdata")
def gdata():
    return jsonify(app.vars['data'])
    
        
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 