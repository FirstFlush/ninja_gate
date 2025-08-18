from street_ninja_common.enums import StreetNinjaEnum


class RequestAction(StreetNinjaEnum):
    PROCEED = "proceed"
    DROP = "drop"
    PROCEED_DROP_JUNK = "proceed_drop_junk"