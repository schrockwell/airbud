"""The main entry point for the Airbud application server.

See http://localhost:5000/ for the web interface."""

import airbud.gps
import airbud.rf
import airbud.web


airbud.gps.start()
airbud.rf.start()

airbud.web.start()

airbud.gps.stop()
airbud.rf.stop()
