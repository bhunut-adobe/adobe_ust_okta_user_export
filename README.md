# adobe_ust_okta_user_export
Exporting Okta Users using Adobe User Sync Tool configuration files. Use for troubleshooting purposes


Argument 1 is for the path to connector-okta.yml

Argument 2 is for the path to user-sync-config.yml'

example: user.py /document/connector-okta.yml /document/user-sync-config.yml

The script can also run without any argument. The script will look for configuration files within the same folder.

The export will be in JSON format and output to the console


