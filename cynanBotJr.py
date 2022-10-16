from asyncio import AbstractEventLoop
from typing import Optional

from twitchio.ext import commands

from authRepository import AuthRepository
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from users.usersRepository import UsersRepository


class CynanBotJr(commands.Bot):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        authRepository: AuthRepository,
        chatBandManager: Optional[ChatBandManager],
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        websocketConnectionServer: Optional[WebsocketConnectionServer]
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = [ user.getHandle().lower() for user in usersRepository.getUsers() ],
            loop = eventLoop,
            nick = authRepository.getAll().requireNick(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken()
        )

        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif authRepository is None:
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
