from typing import Any, Callable, Dict, Optional

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook import QlikSenseHook

class QlikSenseCloudReloadOperator(BaseOperator):
    """
    Trigger a reload of the app id passed in params.

    :conn_id: connection to run the operator with
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['appId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, appId: str = None, conn_id: str = 'qlik_conn_sample', waitUntilFinished: bool = True, **kwargs: Any,) -> None:
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

        if response.status_code == 400: 
            errorDetail = response.json()['errors']['detail']
            raise RuntimeError('Invalid request: {}. Check if appId provided is valid.'.format(errorDetail))
        if response.status_code == 401:
            raise RuntimeError('JWT Token invalid or missing: Check if your API token is still available or valid. Please update connection with the correct one.')

        return response.text
