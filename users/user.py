from datetime import tzinfo
from typing import List

import CynanBotCommon.utils as utils


class User():

    def __init__(
        self,
        isChatBandEnabled: bool,
        handle: str,
        locationId: str,
        timeZones: List[tzinfo]
    ):
        if not utils.isValidBool(isChatBandEnabled):
            raise ValueError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        elif not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        self.__isChatBandEnabled: bool = isChatBandEnabled
        self.__handle: str = handle
        self.__locationId: str = locationId
        self.__timeZones: List[tzinfo] = timeZones

    def getHandle(self) -> str:
        return self.__handle

    def getLocationId(self) -> str:
        return self.__locationId

    def getTimeZones(self) -> List[tzinfo]:
        return self.__timeZones

    def getTwitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    def hasLocationId(self) -> bool:
        return utils.isValidStr(self.__locationId)

    def hasTimeZones(self) -> bool:
        return utils.hasItems(self.__timeZones)

    def isChatBandEnabled(self) -> bool:
        return self.__isChatBandEnabled
