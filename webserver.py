from flask import Flask
import data
import threading
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/get_data")
def get_data():
    data.get_data()
    return "%s" % data.prices


@app.route("/table")
def table():
    table_html = ""
    for e in reversed(data.prices):
        table_html += '''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
        ''' % e
    tabela = '''
<html>
<head>
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <TABLE  BORDER="5"; WIDTH=50%%>
    <TR>
        <TH COLSPAN="3">
            <H3><BR>Podatci s burza</H3>
        </TH>
    </TR>
        <TH>Date</TH>
        <TH>Symbol</TH>
        <TH>Price</TH>
    <TR>
    % s
    </TR>
</TABLE>
</body>
</html>
    '''

    return tabela % table_html


@app.route("/data")
def returndata():
    s = '''
    <html>
    <head>
    <meta http-equiv="refresh" content="5">
    </head>
    <body>
    %r
    </body>
    </html>
    '''
    return s % data.prices


@app.route("/graph")
def graph():
    import matplotlib
    import matplotlib.pyplot as plt
    #plt = matplotlib.pyplot
    import StringIO
    import urllib, base64

    plt.plot(range(10, 20))
    fig = plt.gcf()

    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
    return '<img src = "%s"/>' % uri

    


def puller():
    while True:
        print "polling"
        data.get_data()
        time.sleep(10)


t = threading.Thread(target=puller)
t.setDaemon(True)
t.start()

if __name__ == "__main__":
    app.run(debug=True)
