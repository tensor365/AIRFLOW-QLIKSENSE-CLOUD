from typing import Any, Callable, Dict, Optional

import time 
import uuid

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.qlik_sense_cloud.hooks.qlik_sense_hook import QlikSenseHook

class QlikSenseCloudAutomationOperator(BaseOperator):
    """
    Trigger a reload of an automation from automation id passed in params.

    :conn_id: connection to run the operator with
    :automationId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['automationId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, automationId: str = None, conn_id: str = 'qlik_conn_sample', inputs:Dict[str, Any] = {}, synchrone: bool = True ,**kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.automationId = automationId
        self.inputs = inputs
        self.synchrone = synchrone

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = QlikSenseHook(self.method, conn_id=self.conn_id)
        
        #Body of request to reload application
        
        self.log.info("Trigger the reload automation {}".format(self.automationId))

        response = hook.reload_automation(self.automationId)

        runId = response.id
        #If activated, wait the end of the automation to give an answer
        if self.synchrone:
            self.log.info("Checking status of the automation reload {}".format(self.automationId))
            notFinished = True
            while notFinished:
                ans = hook.get_status_reload_automation(self.automationId, runId)
                if ans.status == 'finished':
                    notFinished=False
                    self.log.info("Automation {} reload ended successfully".format(self.automationId))
                elif ans.status == 'finished with warnings':
                    notFinished=False
                    self.log.info("Automation {} reload ended successfully with warnings".format(self.automationId))
                elif ans.status == 'failed':             
                    raise RuntimeError('Automation reload {} failed.'.format(self.automationId))
                elif ans.status == 'stopped':
                    raise RuntimeError('Automation reload {} has been stopped.'.format(self.automationId))
                time.sleep(15)