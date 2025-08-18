from dataclasses import dataclass
from gatekeeper.dataclasses import BaseEvaluationData, BaseEvaluationDecision


@dataclass
class PostflightEvaluationData(BaseEvaluationData):
    
    msg: str
    
    
@dataclass
class PostflightEvaluationDecision(BaseEvaluationDecision):
    pass