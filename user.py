import yaml
import os.path
import sys
import okta
import json


def load_config_to_dict(path):
    if os.path.isfile(path):
        file = open(path, "r")
        file_data = file.read()
        yaml_data = yaml.load(file_data)
        return yaml_data
    else:
        raise AssertionError("Unable to find file")
    return None


def connect_okta(config):
    url = "https://" + config['okta_url']
    api_token = config['api_token']
    conn = okta.UserGroupsClient(url, api_token)
    return conn


def find_group(okta_conn, name):
    results = okta_conn.get_groups(query=name)
    for result in results:
        if result.profile.name == name:
            return result
    return None


def format_group_members_json(obj):
    members = []

    for member in obj:
        members.append(
            {
                'id': member.id,
                'profile': member.profile.__dict__
            })
    return json.dumps(members, sort_keys=True,
                      indent=4, separators=(',', ': '))


def main(argv):
    if argv[0]:
        okta_config_file = argv[0]
    else:
        okta_config_file = 'connector-okta.yml'

    if argv[1]:
        ust_config_file = argv[1]
    else:
        ust_config_file = 'user-sync-config.yml'

    if okta_config_file and ust_config_file:
        okta_config = load_config_to_dict(okta_config_file)
        ust_config = load_config_to_dict(ust_config_file)
        okta_conn = connect_okta(okta_config)

        for group in ust_config['directory_users']['groups']:
            group_name = group['directory_group']
            okta_group = find_group(okta_conn, group_name)
            if okta_group:
                group_members = okta_conn.get_group_all_users(gid=okta_group.id)
                print "======== Processing Group: %s =========" % (group_name)
                print format_group_members_json(group_members)
            else:
                print "======== %s NOT FOUND =========" % (group_name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
