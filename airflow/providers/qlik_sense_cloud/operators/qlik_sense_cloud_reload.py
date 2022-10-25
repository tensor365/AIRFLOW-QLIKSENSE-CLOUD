from typing import Any, Callable, Dict, Optional

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook import QlikSenseHook

class QlikSenseCloudReloadOperator(BaseOperator):
    """
    Calls an endpoint on an HTTP system to execute an action.

    :param sample_conn_id: connection to run the operator with
    :type conn_id: str
    :type endpoint: str
    :param data: The data to pass
    :type data: a dictionary of key/value string pairs
    :param headers: The HTTP headers to be added to the request
    :type headers: a dictionary of string key/value pairs
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['appId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, appId: str = None, conn_id: str = 'conn_sample', **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.appId = appId
        self.endpoint = 'api/v1/reloads'
        self.method = 'POST'

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = QlikSenseHook(self.method, conn_id=self.conn_id)

        #Body of request to reload application
        self.data = {"appId":self.appId,"partial": False}

        self.log.info("Call HTTP method to reload app {}".format(self.appId))

        response = hook.run(self.endpoint, self.data)

        return response.text
