from abc import ABC, abstractmethod
from cache.dataclasses import GateActivityData
from django.conf import settings
from gatekeeper.dataclasses import BaseEvaluationData, BaseDecision
from gatekeeper.models import AbuseEvent, RiskProfile
from gatekeeper.preflight.dataclasses import PreflightEvaluationData, PreflightDecision
from gatekeeper.postflight.dataclasses import PostflightEvaluationData, PostflightDecision


class BaseRiskEvaluationService(ABC):

    ABUSE_EVENTS_MAX = settings.ABUSE_EVENTS_MAX
    
    def __init__(self, data: BaseEvaluationData):
        self.data = data
    
    @abstractmethod
    def evaluate(self, **kwargs) -> BaseDecision:
        pass
    
class PreflightEvaluationService(BaseRiskEvaluationService):
    
    def __init__(self, data: PreflightEvaluationData):
        super().__init__(data)

    def evaluate(self) -> PreflightDecision:
        ...        



class PostflightEvaluationService(BaseRiskEvaluationService):
    
    def __init__(self, data: PostflightEvaluationData):
        super().__init__(data)
        
    def evaluate(self) -> PostflightDecision:
        ...