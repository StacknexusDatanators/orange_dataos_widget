from Orange.widgets.widget import OWWidget, Output, Input
from Orange.widgets.settings import Setting
from Orange.widgets import gui
from Orange.data import Table, table
from trino.dbapi import connect
from trino.auth import BasicAuthentication
import pandas as pd
import sys
from Orange.data.pandas_compat import table_from_frame

class orange_dataos(OWWidget):
    # Widget's name as displayed in the canvas
    name = "DataOS Integration"
    # Short widget description
    description = "let's connect with dataos"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "icons/dataos_logo.svg"

    # Widget's outputs; here, a single output named "Number", of type int
    class Inputs:
        instance_name = Input("instance_name", str)
        cluster_name = Input("cluster_name", str)
        username = Input("username", str)
        api_key = Input("apikey", str)
        sql_query = Input("sql_query", str)

    class Outputs:
        output_df = Output("Output Dataset", Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        self.instance_name = ""
        self.cluster_name = ""
        self.username = ""
        self.api_key = ""
        self.sql_query = ""
        self.output_df = ""
        box = gui.vBox(self.controlArea, "TrinoDB Settings")

        gui.lineEdit(box, self, "instance_name", label="DataOS domain:")
        gui.lineEdit(box, self, "cluster_name", label="Catalog:")
        gui.lineEdit(box, self, "username", label="Username:")
        gui.lineEdit(box, self, "api_key", label="Apikey:")
        gui.lineEdit(box, self, "sql_query", label="SQL Query:")
        gui.button(self.controlArea, self, "Read Data", callback=self.read_data)
    
    def read_data(self):
        conn = connect(
            host="tcp.{0}".format(self.instance_name),
            port="7432",
            auth=BasicAuthentication(self.username,self.api_key),
            http_scheme="https",
            http_headers={"cluster-name": self.cluster_name}
        )
        data = pd.read_sql(self.sql_query, conn)
        for c in data.columns:
            print(c, type(data[c][0]))
        print(data)
        data.drop(columns = ["__metadata"], inplace = True)
        self.Outputs.output_df.send(table_from_frame(data))

    @Inputs.instance_name
    def set_instance_name(self, instance_name):
        self.instance_name = instance_name
    @Inputs.cluster_name
    def set_cluster_name(self, cluster_name):
        self.cluster_name = cluster_name
    @Inputs.username
    def set_username(self, username):
        self.username = username
    @Inputs.api_key
    def set_apikey(self, api_key):
        self.api_key = api_key
    @Inputs.sql_query
    def set_sql_query(self, sql_query):
        self.sql_query = sql_query

def main(argv=sys.argv):
    from AnyQt.QtWidgets import QApplication
    app = QApplication(list(argv))
    args = app.arguments()

    ow = orange_dataos()
    ow.show()
    ow.raise_()
    app.exec_()
    return 0


if __name__ == "__main__":
    sys.exit(main())
