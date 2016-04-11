BuddyUp API and celery workers.

(Cleanup for the below is coming!)

# Get up and running:

To bootstrap the codebase, docker and file-syncing, in one tab run:

```bash
d workon
d bootstrap
```

Then, to kick off the app machines, run

```bash
d workon
d up
```


The first time, run

```
d syncdb
```


## Dev links.

Dev hostnames are all set up - here's the list:

- http://app.bu - BuddyUp App
- http://marketing.bu - Marketing Site
- http://gc.bu - Ground Control
- http://dashboard.bu - School Dashboard


# Running commands in docker

```bash
d bash
```

Will get you in.


# Older Specs


# Other useful commands

```bash
d bash
cd app;
gulp update   # update all libs
gulp blaze    # complile blaze rules
gulp deploy_blaze    # push blaze rules to server
```


# Requirements

We've got lots of dependencies and we try to keep them current.

`gulp check` from inside docker will give you the potential updates.

# Testing on Android.

1. Install all of the above, including the latest SDKs.
2. If you're on Mac OS, install this fix: http://stackoverflow.com/questions/30812770/ant-jar-error-execute-failed-java-io-ioexception-cannot-run-program-aapt
  (my path was `/Applications/android-sdk-tools...`)
3. `cd native/ionic;`
4. Plug in your android phone via USB
5. `ionic run android`


- Remote debugging: https://developer.chrome.com/devtools/docs/remote-debugging .
- Devices link: `chrome://inspect/#devices`

# Background reading

## Ionic

BuddyUp is built on [ionic](http://ionicframework.com).  If you're not familiar with ionic, please read through their high-level docs, and familiarize yourself with the Ionic design patterns before jumping in!

## Deploying

All builds that pass CI on master are deployed.

## Releasing to the app stores.

This is all in Steven's head right now.  We should get it out.

(TODO: Put these notes somewhere organized.)
http://forum.ionicframework.com/t/ionic-toturial-for-building-a-release-apk/15758

Sign Android app

```bash
cd native/ionic/releases/android
keytool -genkey -v -keystore BuddyUp.keystore -alias BuddyUp -keyalg RSA -keysize 2048 -validity 10000

# Enter password (in 1p)
```

## I18N

BuddyUp was fully internationalized.  Every user-facing string should be wrapped in translate tags where possible.

Please read up on angular-gettext here: https://angular-gettext.rocketeer.be/dev-guide/translate/ before adding any content.


## Other XCode notes:

http://stackoverflow.com/questions/12184767/phonegap-cdvviewcontroller-h-file-not-found-when-archiving-for-ios


## Old build for Android (may be out of date.)

```bash
unlock Android phone
cd native/ionic
ionic run android
open Android phone
```

## Build for iPhone
1. unlock iPhone
1. open xCode
1. select buddyup project
1. build buddyup (press 'play' in xCode)

