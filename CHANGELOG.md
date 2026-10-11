# Changelog: Week 4 (InsecureBankv2 review)

What I tried, in order, including what failed.

## Static analysis
- Ran MobSF v4.5.4 in Docker and scanned InsecureBankv2. Score 28/100, 13 manifest entries (6 High, 7 Warning).
- MobSF's Code Analysis table came back empty, so I did not rely on it alone.
- Reviewed the manifest and 12 declared permissions by hand.
- Read eight source files in MobSF's Java viewer: TrackUserContentProvider, DoLogin, WrongLogin, CryptoClass, LoginActivity, ChangePassword, PostLogin, MyBroadCastReceiver. Found F1 to F4, F7, F9.
- Wrote the scope statement after the static scan had started and before any dynamic testing.

## Emulator setup (took the longest)
- Installed Android Studio and tried a Pixel 6 device. The default image was Android 17 (API 37); I chose an older image instead.
- API 30 was not in the image list, so I used API 33 (Google APIs, x86_64).
- Download failed: C: drive was full. Freed disk space.
- Emulator would not start: `emulator.exe` was 0 bytes because of the earlier full disk. Reinstalled the Android Emulator package in the SDK Manager.
- Next failure: not enough space for the userdata partition. Reduced the virtual device storage and freed more space.
- Emulator started but was slow on a 7.4 GB RAM laptop, with repeated "System UI isn't responding" dialogs. Continued with adb, which does not need the UI.
- First `adb install` failed with a NullPointerException because the emulator had not finished booting. Waited for `sys.boot_completed` = 1, then the install returned Success.

## Dynamic checks
- Launched the app and recorded the permission screen and the "older version of Android" popup.
- `run-as` worked, so the app is debuggable (F8). Read `shared_prefs` and found only `serverip` and `serverport` in plain text (F12).
- First `sqlite3` query failed ("incomplete input") because of Windows quoting. Fixed by wrapping the command in double quotes with the query in single quotes. The `names` table was empty.
- Launched PostLogin and ChangePassword with `am start` without logging in (F5, confirmed).
- Queried the content provider: "No result found" (F6, reachability confirmed).
- Captured logcat during a failed login. Only partly searched, so F3 is not validated.
- Login failed because the Python 2 backend was not set up. Wrote a small local listener (`tools/listener.py`) on port 8888 and observed `POST /login` with the username and password in plain text (F2, partly validated).

## Not done
- Successful login, password-change request, DoTransfer and ViewStatement launch, broadcast receiver trigger, and review of four source files.
