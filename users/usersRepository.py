import json
import os
from datetime import tzinfo
from typing import Any, Dict, List, Optional

import aiofiles
import aiofiles.ospath
import CynanBotCommon.utils as utils
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface

from users.user import User


class UsersRepository(UsersRepositoryInterface):

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        usersFile: str = 'users/usersRepository.json'
    ):
        if timeZoneRepository is None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidStr(usersFile):
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__timeZoneRepository: TimeZoneRepository = timeZoneRepository
        self.__usersFile: str = usersFile

        self.__jsonCache: Optional[Dict[str, Any]] = None
        self.__userCache: Dict[str, User] = dict()

    async def clearCaches(self):
        self.__jsonCache = None
        self.__userCache.clear()

    def __createUser(self, handle: str, userJson: Dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif userJson is None:
            raise ValueError(f'userJson argument is malformed: \"{userJson}\"')

        isChatBandEnabled = utils.getBoolFromDict(userJson, 'chatBandEnabled', False)
        locationId = utils.getStrFromDict(userJson, 'locationId', '')

        timeZones: List[tzinfo] = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        user = User(
            isChatBandEnabled = isChatBandEnabled,
            handle = handle,
            locationId = locationId,
            timeZones = timeZones
        )

        self.__userCache[handle.lower()] = user
        return user

    def __createUsers(self, jsonContents: Dict[str, Any]) -> List[User]:
        if not utils.hasItems(jsonContents):
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        users: List[User] = list()
        for key in jsonContents:
            user = self.__createUser(key, jsonContents[key])
            users.append(user)

        if not utils.hasItems(users):
            raise RuntimeError(f'Unable to read in any users from users repository file: \"{self.__usersFile}\"')

        users.sort(key = lambda user: user.getHandle().lower())
        return users

    def __findAndCreateUser(self, handle: str, jsonContents: Dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif not utils.hasItems(jsonContents):
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        if handle.lower() in self.__userCache:
            return self.__userCache[handle.lower()]

        for key in jsonContents:
            if handle.lower() == key.lower():
                return self.__createUser(handle, jsonContents[key])

        raise RuntimeError(f'Unable to find user with handle \"{handle}\" in users repository file: \"{self.__usersFile}\"')

    def getUser(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()
        return self.__findAndCreateUser(handle, jsonContents)

    async def getUserAsync(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = await self.__readJsonAsync()
        return self.__findAndCreateUser(handle, jsonContents)

    def getUsers(self) -> List[User]:
        jsonContents = self.__readJson()
        return self.__createUsers(jsonContents)

    async def getUsersAsync(self) -> List[User]:
        jsonContents = await self.__readJsonAsync()
        return self.__createUsers(jsonContents)

    def __readJson(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not await aiofiles.ospath.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        async with aiofiles.open(self.__usersFile, mode = 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents
