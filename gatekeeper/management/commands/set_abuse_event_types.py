
from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from ...enums import AbuseEventTypeEnum, AbuseCategoryEnum
from ...models import AbuseEventType


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Populate the AbuseEventType table"
    
    DATA = [
        
        {
            "name": AbuseEventTypeEnum.INTERNATIONAL_NUMBER,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
            "severity_weight": 100,
        },
        
        {
            "name": AbuseEventTypeEnum.USA_NUMBER,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
            "severity_weight": 100,
        },
        
        {
            "name": AbuseEventTypeEnum.MALICIOUS,
            "category": AbuseCategoryEnum.SECURITY,
            "description": "",
            "severity_weight": 100,
        },
        
        {
            "name": AbuseEventTypeEnum.VOIP_NUMBER,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
            "severity_weight": 100,
        },
        
    ]


    def handle(self, *args, **kwargs):
        logger.info("Populating AbuseEventType table...")
        try:
            self._handle()
        except Exception as e:
            msg = f"Failure to populate AbuseEventType table due to the following error: {e}"
            logger.error(msg, exc_info=True)
            raise
        else:
            logger.info("AbuseEventType table populated")
        
    def _handle(self): ...
        # AbuseEventType