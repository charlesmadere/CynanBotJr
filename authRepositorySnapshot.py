from typing import Any, Dict

import CynanBotCommon.utils as utils


class AuthRepositorySnapshot():

    def __init__(
        self,
        jsonContents: Dict[str, Any],
        authRepositoryFile: str
    ):
        if not utils.hasItems(jsonContents):
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')
        elif not utils.isValidStr(authRepositoryFile):
            raise ValueError(f'authRepositoryFile argument is malformed: \"{authRepositoryFile}\"')

        self.__jsonContents: Dict[str, Any] = jsonContents
        self.__authRepositoryFile: str = authRepositoryFile

    def requireNick(self) -> str:
        nick = self.__jsonContents.get('nick')

        if not utils.isValidStr(nick):
            raise ValueError(f'\"nick\" in Auth Repository file (\"{self.__authRepositoryFile}\") is malformed: \"{nick}\"')

        return nick

    def requireTwitchClientId(self) -> str:
        twitchClientId = self.__jsonContents.get('twitchClientId')

        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'\"twitchClientId\" in Auth Repository file (\"{self.__authRepositoryFile}\") is malformed: \"{twitchClientId}\"')

        return twitchClientId

    def requireTwitchClientSecret(self) -> str:
        twitchClientSecret = self.__jsonContents.get('twitchClientSecret')

        if not utils.isValidStr(twitchClientSecret):
            raise ValueError(f'\"twitchClientSecret\" in Auth Repository file (\"{self.__authRepositoryFile}\") is malformed: \"{twitchClientSecret}\"')

        return twitchClientSecret

    def requireTwitchIrcAuthToken(self) -> str:
        twitchIrcAuthToken = self.__jsonContents.get('twitchIrcAuthToken')

        if not utils.isValidStr(twitchIrcAuthToken):
            raise ValueError(f'\"twitchIrcAuthToken\" in Auth Repository file (\"{self.__authRepositoryFile}\") is malformed: \"{twitchIrcAuthToken}\"')

        return twitchIrcAuthToken
