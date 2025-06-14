## Usage
1. Run the script:
   ```sh
   python ldap_manager.py
   ```
2. Select an operation from the main menu.
3. Enter the required LDAP server details and user information as prompted.

## Example Operations
- **List SPNs:**
  - Choose "List current SPNs for a user" and provide the user's DN.
- **Add/Remove SPN:**
  - Choose the respective option and provide the user's DN and the SPN value.
- **Search for User:**
  - Enter the base DN and an LDAP search filter (e.g., `(sAMAccountName=username)`).
- **Show All Attributes:**
  - Provide the user's DN to display all LDAP attributes.
- **Reset Password:**
  - Provide the user's DN and a new password (will be securely prompted).
- **Enable/Disable User:**
  - Provide the user's DN to enable or disable the account.
- **Create New User:**
  - Enter the OU DN, CN, sAMAccountName, and password for the new user.

## Notes
- Ensure you have appropriate permissions on the LDAP server to perform these operations.
- For Active Directory, password changes require SSL/TLS and the password must be provided in a specific format (handled by the script).
- The script prompts for sensitive information (like passwords) securely.

## Disclaimer
Use this script responsibly and only on systems you are authorized to manage.
