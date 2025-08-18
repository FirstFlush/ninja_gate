from abc import ABC
from cache.dataclasses import GateActivityData
from django.conf import settings
from gatekeeper.dataclasses import BaseEvaluationData, PostflightEvaluationData
from gatekeeper.models import AbuseEvent, RiskProfile
from gatekeeper.preflight.dataclasses import PreflightEvaluationData


class BaseRiskEvaluationService(ABC):

    ABUSE_EVENTS_MAX = settings.ABUSE_EVENTS_MAX
    
    def __init__(self, data: BaseEvaluationData):
        self.data = data
    
class PreflightEvaluationService(BaseRiskEvaluationService):
    
    def __init__(self, data: PreflightEvaluationData):
        super().__init__(data)

class PostflightEvaluationService(BaseRiskEvaluationService):
    
    def __init__(self, data: PostflightEvaluationData):
        super().__init__(data)