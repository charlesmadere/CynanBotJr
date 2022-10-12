import asyncio
import locale

from authRepository import AuthRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.networkClientProvider import NetworkClientProvider
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.userIdsRepository import UserIdsRepository
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


#######################################
## CynanBotJr initialization section ##
#######################################

cynanBotJr = CynanBotJr(
    eventLoop = eventLoop,
    authRepository = authRepository,
    timber = timber,
    usersRepository = UsersRepository(
        timeZoneRepository = TimeZoneRepository()
    ),
    userIdsRepository = userIdsRepository
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBotJr', 'Starting CynanBotJr...')
cynanBotJr.run()
