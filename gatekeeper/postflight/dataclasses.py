from dataclasses import dataclass
from gatekeeper.dataclasses import BaseEvaluationData, BaseDecision


@dataclass
class PostflightEvaluationData(BaseEvaluationData):
    
    msg: str
    
    
@dataclass
class PostflightDecision(BaseDecision):
    pass