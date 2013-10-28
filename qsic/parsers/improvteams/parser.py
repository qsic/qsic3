

class BaseItParser(object):
    """Base Improvteams Parser"""
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        self.fetch_html()
        return self

    def fetch_html(self):
        """Fetch HTML data from Improvteams.com at self.url"""
        pass

    def parse_html(self):
        """This should be implimented by each subclass"""
        pass


class ItPerformerParser(BaseItParser):
    """Parser for performer information from Improvteams"""

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(url)
        self.first_name = None
        self.last_name = None
        self.headshot = None
        self.bio = None
        self.parse_html()

    def parse_html(self):
        """Return self with attributes populated"""
        pass

    def fetch_headshot(self):
        """"""
        pass

# store time as big endian long in a string
s = struct.pack("!L", int(time.time()))
rand_hash = base64.urlsafe_b64encode(s)[:-2]
new_headshot_filename = '%s-%s-%s' % (rand_hash, self.first_name, self.last_name)

if self.headshot:
    self.headshot.delete(save=False)

if player_info.headshot:
    self.headshot.save('%s.jpg' % slugify(new_headshot_filename),
                       File(open(player_info.headshot)))
    os.unlink(player_info.headshot)

class ItTeamParser(BaseItParser):
    """Parse team information from Improvteams"""
    pass