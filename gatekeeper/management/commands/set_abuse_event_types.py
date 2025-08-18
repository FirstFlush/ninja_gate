from django.core.management.base import BaseCommand
from django.db import transaction
import logging
from typing import Any
from ...enums import AbuseEventTypeEnum
from ...models import AbuseEventType
from ._event_type_data import EVENT_TYPE_DATA


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Pre-populate the AbuseEventType table with initial data.

    Creates all required AbuseEventType records in a single transaction.
    If any error occurs, all changes are rolled back.
    """
    help = "Populate the AbuseEventType table"

    DATA = EVENT_TYPE_DATA

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

    def _handle(self):
        self._preflight()
        with transaction.atomic():
            for event_type in self.DATA:
                self._save(event_type)

    def _preflight(self):
        if len(AbuseEventTypeEnum.__members__) != len(self.DATA):
            enum_members = set(AbuseEventTypeEnum.values)
            event_data = set([event_type["name"].value for event_type in self.DATA])
            missing = ", ".join(enum_members.difference(event_data))
            msg = f"Preflight check failed. Missing AbuseEventTypeEnums: `{missing}`"
            logger.error(msg)
            raise RuntimeError(msg)

    def _save(self, event_type: dict[str, Any]):
        try:
            _, created = AbuseEventType.objects.get_or_create(
                name=event_type["name"].value,
                category=event_type["category"].value,
                description=event_type["description"],
            )
        except Exception as e:
            msg = f"Could not populate AbuseEventType table due to an unexpected error: {e}"
            logger.error(msg, exc_info=True)
            raise
        
        else:
            if created:
                logger.info(f"AbuseEventType `{event_type['name'].value}` created")
            else:
                logger.info(f"AbuseEventType `{event_type['name'].value} already exists. Skipping...`")