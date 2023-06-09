# Standard Library
import socket
from typing import Optional

# Slack
from slack_sdk.http_retry.interval_calculator import RetryIntervalCalculator
from slack_sdk.http_retry.state import RetryState
from slack_sdk.http_retry.request import HttpRequest
from slack_sdk.http_retry.response import HttpResponse
from slack_sdk.http_retry.handler import RetryHandler, default_interval_calculator


class MyRetryHandler(RetryHandler):
    ''' Handles retries for slack webhook 
    Ensures that slackTools does not crash your program if internet connection is lost.
    '''
    def __init__(
        self,
        max_retry_count: int = 3,
        interval_calculator: RetryIntervalCalculator = default_interval_calculator,
    ):
        super().__init__(max_retry_count, interval_calculator)
        self.call_count = 0

    def _can_retry(
        self,
        *,
        state: RetryState,
        request: HttpRequest,
        response: Optional[HttpResponse],
        error: Optional[Exception],
    ) -> bool:
        self.call_count += 1
        if response is not None and \
            ( response.status_code != 200 or \
             response.body.get("error") == "fatal_error"):
            return True
        
        if error is not None \
            and isinstance(error, socket.error) \
                and error.errno == 104:
            # [Errno 104] Connection reset by peer
            return True

        return False
