# FindMyExport
Little service that export FindMy items to HA/Traccar

## Install

~/Library/LaunchAgents

launchctl load com.jakub.findmytraccar.plist 
launchctl unload com.jakub.findmytraccar.plist

Remember to set permission to full disk access to python3 (system one not from brew)
