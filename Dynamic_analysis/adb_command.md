<!-- adb_command.md -->

#### list packages and files

list packages [-f] [-d] [-e] [-s] [-3] [-i] [-l] [-u] [-U] [--uid UID] [--user USER_ID] [FILTER]

Prints all packages; optionally only those whose name contains the text in
FILTER. 

Options: 

* -f: see their associated file 
* -d: filter to only show disabled packages 
* -e: filter to only show enabled packages -s: filter to only show system packages 
* -3: filter to only show third party packages -i: see the installer for the packages 
* -l: ignored (used for compatibility with older releases) -U: also show the package UID 
* -u: also include uninstalled packages 
* --uid UID: filter to only show packages with the given UID 
* --user USER_ID: only list packages belonging to the given user

```
adb shell cmd package list packages -f -3
```
#### open apk using monkey
```
adb shell monkey -p your.app.package.name -c android.intent.category.LAUNCHER 1
```
#### stop running an app
```
adb shell am force-stop com.my.app.package
```
#### uninstall app
```
adb uninstall your.app.package.name
```
#### dump lumen data
```
adb pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db output_path
```
#### disable verification
```
adb shell settings put global verifier_verify_adb_installs 0
adb shell settings put global package_verifier_enable 0
```

#### Lumen
package = edu.berkeley.icsi.haystack
```
adb shell pidof edu.berkeley.icsi.haystack
```

#### dump package status
```
adb shell dumpsys package [packagename]
```