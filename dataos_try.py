from Orange.widgets.widget import OWWidget, Output, Input
from Orange.widgets.settings import Setting
from Orange.widgets import gui
from Orange.data import table

class DataOS(OWWidget):
    # Widget's name as displayed in the canvas
    name = "DataOS Integration"
    # Short widget description
    description = "let's connect with dataos"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "widgets_assets/dataos_logo.svg"

    # Widget's outputs; here, a single output named "Number", of type int
    class Inputs:
        instance_name = Input("Instance Name", str)
        cluster_name = Input("cluster name", str)
        username = Input("username", str)
        api_key = Input("Apikey", str)
        sql_query = Input("sql_query", str)

    class Outputs:
        output_df = Output("Output Dataset", table)

    def __init__(self):
        super().__init__()

        self.instance_name = None
        self.cluster_name = None
        self.username = None
        self.api_key = None
        self.sql_query = None
        self.output_df = None

    