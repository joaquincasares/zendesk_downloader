import os
import getpass
import ConfigParser
import requests
if requests.__version__.split('.')[0] == '0':
    raise ImportError('requests library must be at least 1.0, current is only '+requests.__version__)
import re


class ZenDesk(object):
    """Class for interacting with ZenDesk."""

    def __init__(self):
        """Constructor for ZenDesk object"""
        self.domain = None
        self.admin_email = None
        self.admin_password = None
        self.download_directory = None
        self.run_open = None
        self.open_program = None

    def authenticate(self):
        configfile = os.path.join(os.path.expanduser('~'), '.zendesk.cfg')
        config = ConfigParser.SafeConfigParser({'download_directory': './',
                                                'run_open': 'False',
                                                'open_program': 'open'})
        if os.path.exists(configfile):
            config.read(configfile)

        self.domain = config.get('ZenDesk', 'domain') if config.has_option('ZenDesk', 'domain') else raw_input('Zendesk Domain: ')
        self.admin_email = config.get('ZenDesk', 'email') if config.has_option('ZenDesk', 'email') else raw_input('Zendesk Email Address: ')
        self.admin_password = config.get('ZenDesk', 'pass') if config.has_option('ZenDesk', 'pass') and config.get('ZenDesk', 'pass') else getpass.getpass()
        self.download_directory = config.get('Downloader', 'download_directory')
        self.run_open = config.getboolean('Downloader', 'run_open')
        self.open_program = config.get('Downloader', 'open_program')

        while True:
            if 'error' in self.get_users_by_page():
                print 'Authentication with "{0}" failed. Please try again...'.format(self.admin_email)
                self.domain = raw_input('Zendesk Domain: ')
                self.admin_email = raw_input('Zendesk Email Address: ')
                self.admin_password = getpass.getpass()
            else:
                print 'Successfully authenticated to ZenDesk!'
                break

    def get_users_by_page(self, page_num=1):
        """Test function for authentication purposes"""
        r = requests.get('https://%s/api/v2/users.json' % self.domain,
                         params={'page': page_num},
                         auth=(self.admin_email, self.admin_password)).json()
        return r

    def get_all_ticket_metadata(self, ticket_id):
        """Get the ticket meta per id"""
        r = requests.get('https://%s/api/v2/tickets/%s.json?include=organizations' % (self.domain, ticket_id),
                         auth=(self.admin_email, self.admin_password)).json()
        return r

    def get_ticket(self, ticket_id):
        """Get the ticket postings per id"""
        r = requests.get('https://%s/api/v2/tickets/%s/audits.json' % (self.domain, ticket_id),
                         auth=(self.admin_email, self.admin_password)).json()
        to_return = r['audits']

        while r['next_page']:
            r = requests.get(r['next_page'], auth=(self.admin_email, self.admin_password)).json()
            to_return = to_return + r['audits']

        return to_return

    def extract_file_information(self, ticket_id):
        """Extract curl'd json data and format into a dictionary with an array of attachments"""
        ticket = self.get_ticket(ticket_id)
        all_ticket_data = self.get_all_ticket_metadata(ticket_id)
        ticket_data = all_ticket_data["ticket"]
        organization_data = all_ticket_data['organizations'][0]
        organization_id = ticket_data["organization_id"]
        organization_name = organization_data.get("name", "Null")
        # Clean up org names so they don't have funny characters
        organization_name = re.sub(r"[^a-zA-Z_0-9]", "", organization_name)
        attachment_list = []
        for audit in ticket:
            time_created = audit['created_at']
            for event in audit['events']:
                if 'attachments' in event:
                    for attachment in event['attachments']:
                        attachment_list.append([attachment['id'], time_created, attachment['file_name'], attachment['content_url']])

        return {
            'ticket_id': str(ticket_id),
            'organization_id': str("{0}_{1}".format(organization_name,organization_id)),
            'attachments': attachment_list
        }