import matplotlib.pyplot as plt
import io
import base64



def build_graph(x, y):
    img = io.BytesIO()
    plt.pie(x, labels=y, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)






