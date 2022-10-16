import asyncio
import locale

from authRepository import AuthRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.networkClientProvider import NetworkClientProvider
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from cynanBotJr import CynanBotJr
from users.usersRepository import UsersRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Misc initialization section ##
#################################

authRepository = AuthRepository()
backingDatabase = BackingDatabase()
eventLoop = asyncio.get_event_loop()
timber = Timber(
    eventLoop = eventLoop
)
networkClientProvider = NetworkClientProvider(
    eventLoop = eventLoop
)
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase,
    networkClientProvider = networkClientProvider,
    timber = timber
)
websocketConnectionServer = WebsocketConnectionServer(
    eventLoop = eventLoop,
    timber = timber
)


#######################################
## CynanBotJr initialization section ##
#######################################

cynanBotJr = CynanBotJr(
    eventLoop = eventLoop,
    authRepository = authRepository,
    chatBandManager = ChatBandManager(
        timber = timber,
        websocketConnectionServer = websocketConnectionServer
    ),
    timber = timber,
    userIdsRepository = userIdsRepository,
    usersRepository = UsersRepository(
        timeZoneRepository = TimeZoneRepository()
    ),
    websocketConnectionServer = websocketConnectionServer
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBotJr', 'Starting CynanBotJr...')
cynanBotJr.run()
