global class RefreshApex2 implements Queueable {
    global void execute(QueueableContext context) {
        //Create test records
        List<Contact> contacts = new List<Contact>();
        Contact con = new Contact(LastName = 'Tester');
        contacts.add(con);
        Contact con2 = new Contact(LastName = 'TesterTwo');
        contacts.add(con2);
        insert contacts;
    }
}