from typing import Any, Callable, Dict, Optional
import time

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
    def __init__(self, *, appId: str = None, conn_id: str = 'qlik_conn_sample', synchrone: bool = True, **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.appId = appId
        self.synchrone=synchrone

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = QlikSenseHook(self.method, conn_id=self.conn_id)

        #Body of request to reload application
        self.data = {"appId":self.appId,"partial": False}

        self.log.info("Trigger task to reload app {}".format(self.appId))

        response = hook.reload_app(self.appId, False)

        reloadId = response.id
        if self.synchrone:
            self.log.info("Checking status of the application reload: {}".format(self.appId))
            notFinished = True
            while notFinished:
                ans = hook.get_status_reload_app(reloadId)
                if ans.status == 'SUCCEEDED':
                    notFinished = False
                elif ans.status == 'FAILED':
                    raise RuntimeError('Reload of App has failed. \n Log: {}'.format(ans.log))
                elif ans.status == 'EXCEEDED_LIMIT':
                    raise RuntimeError('App reloading has time out.')
                elif ans.status == 'CANCELED':
                    raise RuntimeError('Reload of the app has been cancel')
                time.sleep(15)