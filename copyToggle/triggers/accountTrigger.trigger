trigger accountTrigger on Account (before insert) {
    System.debug('Account trigger.');
}