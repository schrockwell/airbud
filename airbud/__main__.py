import airbud.gps
import airbud.rf
import airbud.web


airbud.gps.start()
airbud.rf.start()

airbud.web.start()

airbud.gps.stop()
airbud.rf.stop()
