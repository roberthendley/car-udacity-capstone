# Application Testing

## Application Testing Environment Variables

The project submission notes include the details of the credentials to be included in a `.env` file to be added to the project root directory. Copy and paste the credentials into the `.env` file prior to running the test scripts. These environment variables will be used by the test scripts to generate valid authentication tokens.


## Automated API Testing

Setup the application for testing by configuring the environment variables that will be used to create the required authorisation tokens.

The application test suite can be run with;
```console
$ python test_full_app.py
$ python test_consultant.py
$ python test_client_mgr.py
```
The test script automatically generates authentication tokens to test the application for users with different permissions.

## User Account Testing

AUTH0 has been configured with a number of user accounts to facilitate the application evaulation process.

Login to the application at the following URL to obtain the tokens needed to test the application endpoints

https://car-project-udacity.au.auth0.com/authorize?audience=car-api.hendley.id.au&response_type=token&client_id=5GiofyrEGQo3QVEZlt357yEi0LqiWHLP&redirect_uri=http://localhost:4200

<table>
    <tr>
        <td>
            email
        </td>
        <td>
            clientmgr@mycompany.com.au
        </td>
    </tr>
    <tr>
        <td>
            password
        </td>
        <td>
            See project submission notes
        </td>
    </tr>
    <tr>
        <td>
        Role
        </td>
        <td>
        Client Manager
        </td>
    </tr><tr>
        <td>
        Permissions
        </td>
        <td>
            <ul>
                <li>create:client-contacts</li>
                <li>create:clients</li>
                <li>delete:client-contacts</li>	
                <li>read:client-contacts</li>
                <li>read:clients</li>
                <li>read:contacts</li>
                <li>read:Reports</li>
                <li>update:client-contacts</li>
                <li>update:clients</li>
            </ul>
        </td>
    </tr>
</table>

<table>
    <tr>
        <td>
            email
        </td>
        <td>
            consultant@mycompany.com.au
        </td>
    </tr>
    <tr>
        <td>
            password
        </td>
        <td>
            See project submission notes
        </td>
    </tr>
    <tr>
        <td>
            Role
        </td>
        <td>
            Consultant
        </td>
    </tr>
    <tr>
        <td>
            Permissions
        </td>
        <td>
            <ul>
                <li>create:client-contacts</li>
                <li>create:Reports</li>
                <li>delete:reports</li>
                <li>read:client-contacts</li>	
                <li>read:clients</li>
                <li>read:contacts</li>
                <li>read:Reports</li>
                <li>update:client-contacts</li>
                <li>update:Reports</li>
            </ul>
        </td>
    </tr>
</table>

<table>
    <tr>
        <td>
            email
        </td>
        <td>
            superadmin@mycompany.com.au
        </td>
    </tr>
    <tr>
        <td>
            password
        </td>
        <td>
            See project submission notes
        </td>
    </tr>
    <tr>
        <td>
            Role
        </td>
        <td>
            Administrator
        </td>
    </tr>
    <tr>
        <td>
            Permissions
        </td>
        <td>
            All Permissions
        </td>
    </tr>
</table>