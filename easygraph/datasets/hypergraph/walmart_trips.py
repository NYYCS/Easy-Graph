import requests

from easygraph.utils.exception import EasyGraphError


def request_text_from_url(url):
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        raise EasyGraphError("Connection Error!")

    if r.ok:
        return r.text
    else:
        raise EasyGraphError(f"Error: HTTP response {r.status_code}")


class walmart_trips:
    def __init__(self, data_root=None):
        self.data_root = "https://" if data_root is not None else data_root
        self.hyperedges_path = "https://gitlab.com/easy-graph/easygraph-data-walmart-trips/-/raw/main/hyperedges-walmart-trips.txt?inline=false"
        self.node_labels_path = "https://gitlab.com/easy-graph/easygraph-data-walmart-trips/-/raw/main/node-labels-walmart-trips.txt?ref_type=heads&inline=false"
        #self.node_names_path = "https://gitlab.com/easy-graph/easygraph-data-walmart-trips/-/raw/main/node-names-house-committees.txt?ref_type=heads&inline=false"
        self.label_names_path = "https://gitlab.com/easy-graph/easygraph-data-walmart-trips/-/raw/main/label-names-walmart-trips.txt?ref_type=heads&inline=false"
        self._hyperedges = []
        self._node_labels = []
        self._label_names = []
        self._node_names = []
        self.generate_hypergraph(
            hyperedges_path=self.hyperedges_path,
            node_labels_path=self.node_labels_path,
            #node_names_path=self.node_names_path,
            label_names_path=self.label_names_path,
        )

    def process_label_txt(self, data_str, delimiter="\n", transform_fun=str):
        data_str = data_str.strip()
        data_lst = data_str.split(delimiter)
        final_lst = []
        for data in data_lst:
            data = data.strip()
            data = transform_fun(data)
            final_lst.append(data)
        return final_lst

    @property
    def node_labels(self):
        return self._node_labels

    """
    @property
    def node_names(self):
        return self._node_names
    """
    @property
    def label_names(self):
        return self._label_names

    @property
    def hyperedges(self):
        return self._hyperedges

    def generate_hypergraph(
        self,
        hyperedges_path=None,
        node_labels_path=None,
        #node_names_path=None,
        label_names_path=None,
    ):
        def fun(data):
            data = int(data) - 1
            return data

        hyperedges_info = request_text_from_url(hyperedges_path)
        hyperedges_info = hyperedges_info.strip()
        hyperedges_lst = hyperedges_info.split("\n")
        for hyperedge in hyperedges_lst:
            hyperedge = hyperedge.strip()
            hyperedge = [int(i) - 1 for i in hyperedge.split(",")]
            self._hyperedges.append(tuple(hyperedge))
        # print(self.hyperedges)

        node_labels_info = request_text_from_url(node_labels_path)

        process_node_labels_info = self.process_label_txt(
            node_labels_info, transform_fun=fun
        )
        self._node_labels = process_node_labels_info
        # print("process_node_labels_info:", process_node_labels_info)
        # print("process_node_names_info:", process_node_names_info)
        label_names_info = request_text_from_url(label_names_path)
        process_label_names_info = self.process_label_txt(label_names_info)
        self._label_names = process_label_names_info
        # print("process_label_names_info:", process_label_names_info)
