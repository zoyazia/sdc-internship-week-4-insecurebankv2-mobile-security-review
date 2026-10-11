# Mobile App Security Review: InsecureBankv2 (Week 4)

SDC Internship, Week 4 Individual Task (Specialist Advanced Build).
Author: Zoya Zia (Member 3)

A security review of **InsecureBankv2**, an intentionally vulnerable Android training app, treated as the mobile product of a fictional Multi-Branch Bottled Water Company. The review follows the OWASP MASTG approach and maps findings to OWASP MASVS categories.

**Authorized lab only.** The target is a deliberately vulnerable training app, tested on my own machine and in an emulator. No real organisation, customer or branch data is involved.

## What this project contains

| Folder / file | Contents |
| --- | --- |
| `report/Week4_Mobile_App_Security_Report.pdf` | Full report: scope, plan, methodology, 12 findings, fixes, risk log, limitations |
| `screenshots/` | Evidence screenshots (the report lists which one supports which finding in Appendix A) |
| `mobsf/MobSF_Report.pdf` | Full MobSF static analysis report |
| `tools/listener.py` | Small local HTTP listener used to observe the login request (not the real backend) |
| `CHANGELOG.md` | What I tried, in order, including what failed |

## Approach

1. **Static analysis:** MobSF v4.5.4 (Docker) scan of the APK, then manual review of the manifest, permissions and eight decompiled source files (MobSF's Code Analysis table was empty).
2. **Dynamic analysis:** Pixel 6 emulator (Android 13, API 33, Google APIs, x86_64) controlled with adb. Checks: permissions at first launch, private storage (`run-as`), exported activities (`am start`), content provider (`content query`), and the login request (local listener on port 8888).
3. **Mapping and fixes:** every finding is mapped to a MASVS category, rated for severity, and the top five have developer-ready fixes.

## Results at a glance

MobSF security score: **28/100**. Manifest analysis: 13 entries (6 High, 7 Warning). **12 findings** in total.

| ID | Finding | MASVS | Severity | Validation |
| --- | --- | --- | --- | --- |
| F1 | Saved credentials recoverable (hardcoded AES key, fixed IV) | CRYPTO, STORAGE | High | Code only |
| F2 | Login and password change over plain HTTP | NETWORK | High | Partly validated (login request seen in cleartext against a stub listener) |
| F3 | Passwords written to logs | STORAGE | Medium | Code only |
| F4 | Exported receiver sends stored password by SMS | PLATFORM | High | Code and manifest only |
| F5 | Post-login screens exported, no authentication check | PLATFORM, AUTH | High | **Confirmed** (PostLogin, ChangePassword) |
| F6 | Exported content provider, no permission | PLATFORM | Medium | Reachability confirmed, table empty |
| F7 | Password change sends no old password or token | AUTH | Medium (potential) | Code only |
| F8 | Configuration weaknesses (debuggable, allowBackup, old SDK) | CODE, RESILIENCE | Medium | debuggable confirmed |
| F9 | Separate developer login path (devadmin) | AUTH | Low (potential) | Code only |
| F10 | Broad permissions | PRIVACY | Low | Permission screen seen |
| F11 | Weak root check, anti-emulator checks | RESILIENCE | Informational | Consistent with code |
| F12 | Server IP and port stored in plain text | STORAGE | Low | **Confirmed** |

## How to reproduce the dynamic checks

Run these from a command prompt with an emulator running and the APK installed (adjust the `adb` path to your SDK).

```
adb install InsecureBankv2.apk
adb shell run-as com.android.insecurebankv2 ls
adb shell run-as com.android.insecurebankv2 cat shared_prefs/com.android.insecurebankv2_preferences.xml
adb shell am start -n com.android.insecurebankv2/.PostLogin
adb shell am start -n com.android.insecurebankv2/.ChangePassword
adb shell content query --uri content://com.android.insecurebankv2.TrackUserContentProvider/trackerusers
```

To observe the login request without the real backend, run `python tools/listener.py`, set the app's server to `10.0.2.2` port `8888`, and press Login. The listener prints the request it receives.

## Limitations

- The lab backend (Python 2) was not set up, so a successful login was never reached. F1, F3, F4, F7 and F9 rest on code and manifest evidence only.
- Only PostLogin and ChangePassword were launched from outside the app. DoTransfer and ViewStatement were not launched, and the broadcast receiver was not triggered.
- Four source files (FilePrefActivity, DoTransfer, ViewStatement, MyWebViewClient) were not reviewed.
- `listener.py` is a stub for observing one request. It is not a replacement for the real backend.

**With more time:** run the backend in an isolated container, validate F1, F3, F4 and F7, and capture real login traffic with a proxy.


