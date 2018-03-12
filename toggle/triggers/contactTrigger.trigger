trigger contactTrigger on Contact (after insert) {
    if(Trigger.isAfter && Trigger.isInsert) {
        System.debug('After insert trigger');
    }
}