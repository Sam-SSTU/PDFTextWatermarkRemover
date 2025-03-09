
    tell application "Finder"
        tell disk "PDF-Watermark-Remover"
            open
            set current view of container window to icon view
            set toolbar visible of container window to false
            set statusbar visible of container window to false
            set the bounds of container window to {400, 100, 900, 450}
            set theViewOptions to the icon view options of container window
            set arrangement of theViewOptions to not arranged
            set icon size of theViewOptions to 72
            set background picture of theViewOptions to file ".background:background.png"
            set position of item "PDF-Watermark-Remover.app" of container window to {150, 175}
            set position of item "Applications" of container window to {350, 175}
            update without registering applications
            delay 1
            close
        end tell
    end tell
    