from typing import Any, Callable, Dict, Optional
import time

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook import QlikSenseHook

class QlikSenseCloudReportOperator(BaseOperator):
    """
    Trigger a reload of the app id passed in params.

    :qlik_sense_cloud_config_id: connection to run the operator with
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['reportId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, reportId: str = None, qlik_sense_cloud_config_id: str = 'qlik_conn_sample', **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.qlik_sense_cloud_config_id = qlik_sense_cloud_config_id
        self.reportId = reportId

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = QlikSenseHook(qlik_sense_cloud_config_id=self.qlik_sense_cloud_config_id)

        #Body of request to reload application
        
        self.log.info("Trigger task to sending report {}".format(self.reportId))

        response = hook.send_report(self.reportId)

        if response.status_code == 204:
            self.log.info("Report triggered {} successfully".format(self.reportId))
        else:
            self.log.error("Report failed {} to trigger".format(self.reportId))
            raise RuntimeError("Report failed {} to trigger".format(self.reportId))
