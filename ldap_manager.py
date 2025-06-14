import getpass
from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE


def connect_ldap():
    ldap_server = input('LDAP server address (e.g., ldap://ad.example.com): ')
    ldap_user = input('Bind DN or username (e.g., user@example.com): ')
    ldap_password = getpass.getpass('Password: ')
    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)
    return conn

def list_spns(conn, user_dn):
    if conn.search(user_dn, '(objectClass=*)', attributes=['servicePrincipalName']):
        entry = conn.entries[0]
        spns = entry['servicePrincipalName'].values if 'servicePrincipalName' in entry else []
        print(f"Current SPNs for {user_dn}:")
        for spn in spns:
            print(f"  - {spn}")
        return spns
    else:
        print(f"Could not retrieve SPNs for {user_dn}. Error: {conn.result}")
        return []

def add_spn(conn, user_dn, spn):
    success = conn.modify(user_dn, {'servicePrincipalName': [(MODIFY_ADD, [spn])]})
    if success:
        print(f"Successfully added SPN '{spn}' to {user_dn}.")
    else:
        print(f"Failed to add SPN. Error: {conn.result}")

def remove_spn(conn, user_dn, spn):
    success = conn.modify(user_dn, {'servicePrincipalName': [(MODIFY_DELETE, [spn])]})
    if success:
        print(f"Successfully removed SPN '{spn}' from {user_dn}.")
    else:
        print(f"Failed to remove SPN. Error: {conn.result}")

def search_user(conn, base_dn, search_filter):
    if conn.search(base_dn, search_filter, attributes=['distinguishedName', 'cn', 'sAMAccountName']):
        print("Search results:")
        for entry in conn.entries:
            print(f"DN: {entry.distinguishedName}, CN: {entry.cn}, sAMAccountName: {entry.sAMAccountName}")
    else:
        print(f"No results found. Error: {conn.result}")

def show_all_attributes(conn, user_dn):
    if conn.search(user_dn, '(objectClass=*)', attributes='*'):
        entry = conn.entries[0]
        print(f"All attributes for {user_dn}:")
        print(entry.entry_to_json())
    else:
        print(f"Could not retrieve attributes. Error: {conn.result}")

def reset_password(conn, user_dn, new_password):
    # For AD, the unicodePwd attribute must be a quoted UTF-16LE string
    pwd = f'"{new_password}"'.encode('utf-16-le')
    success = conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [pwd])]})
    if success:
        print(f"Password reset successful for {user_dn}.")
    else:
        print(f"Failed to reset password. Error: {conn.result}")

def enable_user(conn, user_dn):
    # userAccountControl: 512 = enabled, 514 = disabled
    success = conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [512])]})
    if success:
        print(f"User {user_dn} enabled.")
    else:
        print(f"Failed to enable user. Error: {conn.result}")

def disable_user(conn, user_dn):
    success = conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [514])]})
    if success:
        print(f"User {user_dn} disabled.")
    else:
        print(f"Failed to disable user. Error: {conn.result}")

def create_user(conn, ou_dn, cn, sAMAccountName, password):
    user_dn = f"CN={cn},{ou_dn}"
    attrs = {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        'cn': cn,
        'sAMAccountName': sAMAccountName,
        'userPrincipalName': f"{sAMAccountName}@example.com",
        'unicodePwd': f'"{password}"'.encode('utf-16-le'),
        'userAccountControl': 512
    }
    success = conn.add(user_dn, attributes=attrs)
    if success:
        print(f"User {user_dn} created.")
    else:
        print(f"Failed to create user. Error: {conn.result}")

def main():
    while True:
        print("\nLDAP Management Main Menu:")
        print("1. List current SPNs for a user")
        print("2. Add an SPN to a user")
        print("3. Remove an SPN from a user")
        print("4. Search for user")
        print("5. Show all attributes for user")
        print("6. Reset user password")
        print("7. Enable user account")
        print("8. Disable user account")
        print("9. Create new user")
        print("10. Exit")
        choice = input('Enter your choice (1-10): ')
        if choice == '10':
            break
        # Prompt for server details for each operation
        conn = connect_ldap()
        if choice in ['1', '2', '3', '5', '6', '7', '8']:
            user_dn = input('Distinguished Name (DN) of the user (e.g., CN=User,OU=Users,DC=example,DC=com): ')
        if choice == '1':
            list_spns(conn, user_dn)
        elif choice == '2':
            spn = input('Enter SPN to add: ')
            add_spn(conn, user_dn, spn)
        elif choice == '3':
            spn = input('Enter SPN to remove: ')
            remove_spn(conn, user_dn, spn)
        elif choice == '4':
            base_dn = input('Base DN for search (e.g., DC=example,DC=com): ')
            search_filter = input('LDAP search filter (e.g., (sAMAccountName=username)): ')
            search_user(conn, base_dn, search_filter)
        elif choice == '5':
            show_all_attributes(conn, user_dn)
        elif choice == '6':
            new_password = getpass.getpass('Enter new password: ')
            reset_password(conn, user_dn, new_password)
        elif choice == '7':
            enable_user(conn, user_dn)
        elif choice == '8':
            disable_user(conn, user_dn)
        elif choice == '9':
            ou_dn = input('OU DN for new user (e.g., OU=Users,DC=example,DC=com): ')
            cn = input('CN for new user: ')
            sAMAccountName = input('sAMAccountName for new user: ')
            password = getpass.getpass('Password for new user: ')
            create_user(conn, ou_dn, cn, sAMAccountName, password)
        else:
            print('Invalid choice. Please try again.')
        conn.unbind()

if __name__ == '__main__':
    main()
