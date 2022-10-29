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
    def __init__(self, *, automationId: str = None, conn_id: str = 'qlik_conn_sample', inputs:Dict[str, Any] = {}, waitUntilFinished: bool = True ,**kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.automationId = automationId
        self.inputs = inputs
        self.endpoint = 'api/v1/automations/{}/runs'.format(self.automationId)
        self.method = 'POST'
        self.waitUntilFinshed = waitUntilFinished

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = QlikSenseHook(self.method, conn_id=self.conn_id)
        
        self.guid = str(uuid.uuid4())
        #Body of request to reload application
        self.data = {"guid": self.guid ,"inputs":self.inputs,"context":"editor"}

        self.log.info("Call HTTP method to reload automation {} with guiid {}".format(self.automationId, self.guid))

        response = hook.run(self.endpoint, self.data)

        if response.status_code == 404: 
            errorDetail = response.json()['errors']['detail']
            raise RuntimeError('Invalid request: {}. Check if automationId provided is valid.'.format(errorDetail))
        if response.status_code == 401:
            raise RuntimeError('JWT Token invalid or missing: Check if your API token is still available or valid. Please update connection with the correct one.')

        #If activated, wait the end of the automation to give an answer
        if self.waitUntilFinshed:
            endpointTracker = '/api/v1/automations/{}/runs/{}'.format(self.automationId, self.guid) 
            hookListenner = QlikSenseHook('GET', conn_id=self.conn_id)

            timeout = 60*60*5
            timeoutCounter = 0           
            statusRunning = ['starting', 'running']
            flagAutomationNotFinished = True
            while flagAutomationNotFinished:
                response = hookListenner.run(endpointTracker)
                if response.json()['status'] not in statusRunning:
                    flagAutomationNotFinished = False
                timeoutCounter+=10           
                time.sleep(10)
                if timeoutCounter > timeout: 
                    raise RuntimeError('Timeout: the reloading of automation has timeout')
            return response.text
    
        return response.text