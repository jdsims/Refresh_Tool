global class RefreshApex1 implements Queueable {
    global void execute(QueueableContext context) {
        // UPDATE USERS TO ADMIN AND FIX EMAIL
        Final String sandboxAdminQuery = 'SELECT Id, Email, ProfileID FROM User WHERE IsActive = true AND CompanyName LIKE \'%System Admin%\'';

        List<User> sandboxAdmins = Database.query(sandboxAdminQuery);

        //Get System Administrator profile
        Profile systemAdminProfile = [SELECT Id FROM Profile Where Name = 'System Administrator' Limit 1];

        //Set all Sandbox Admin Users to System Administrator profiles and fix their emails
        for(User user: sandboxAdmins) {
            user.ProfileId = systemAdminProfile.Id;
            user.email = user.email.replace('@example.com','');
            user.email = user.email.replace('=','@');
        }

        Update (sandboxAdmins);

        //Optionally can chain refresh script execution together.
        //ID jobID = System.enqueueJob(new RefreshApex2());
    }
}