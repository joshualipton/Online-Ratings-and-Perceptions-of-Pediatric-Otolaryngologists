class Physician:
    '''
    A Physician will be a row of data and will hold 
    all information pertaining to them in a dictionary
    '''
    def __init__(self) -> None:
        self._id = 0
        self._first_name = ''
        self._last_name = ''
        self._source = ''
        self._residency = '' 
        self._tier = ''
        self._links = {'Healthgrades' : '', 'Vitals' : '', 'RateMDs' : '', 'Yelp' : ''} # Dictionary of links
        self._comments = [] # List of 5-tuples of comments in form (Date, Source, Rating, Comment, Useful)
        self._overall_rating = 0
        self._helpful = 0 # 0 if not helpful 1 if was helpful

    def get_id(self) -> int:
        '''
        Returns ID
        '''
        return self._id

    def set_id(self, id: int) -> None:
        '''
        Sets id
        '''
        self._id = id

    def get_first_name(self) -> str:
        '''
        Returns first name
        '''
        return self._first_name

    def set_first_name(self, fn: str) -> None:
        '''
        Sets first name
        '''
        self._first_name = fn

    def get_last_name(self) -> str:
        '''
        Returns last name
        '''
        return self._last_name

    def set_last_name(self, ln: str) -> None:
        '''
        Sets last name
        '''
        self._last_name = ln

    def get_source(self) -> str:
        '''
        Returns source
        '''
        return self._source

    def set_source(self, source: str) -> None:
        '''
        Sets source
        '''
        self._source = source
    
    def get_residency(self) -> str:
        '''
        Returns residency
        '''
        return self._residency

    def set_residency(self, residency: str) -> None:
        '''
        Sets residency
        '''
        self._residency = residency

    def get_tier(self) -> str:
        '''
        Returns tier
        '''
        return self._tier

    def set_tier(self, tier: str) -> None:
        '''
        Sets tier
        '''
        self._tier = tier

    def get_link(self, website: str) -> str:
        '''
        Returns link based on what website you want
        '''
        return self._links[website]

    def set_links(self, website: str, link: str) -> None:
        '''
        Sets link to a website
        '''
        self._links[website] = link
    
    def get_comments(self) -> 'list[tuple(str, str, str)]':
        '''
        Returns comments in the form (date, rating, comment, useful)
        '''
        return self._comments

    def add_comment(self, comment: 'tuple(str, str, str)') -> None:
        '''
        Adds a comment in the form (date, source, rating, comment)
        '''
        self._comments.append(comment)

    def get_overall_rating(self) -> int:
        '''
        Returns overall rating
        '''
        return self._overall_rating

    def set_overall_rating(self, rating: int) -> None:
        '''
        Sets overall rating
        '''
        self._overall_rating = rating

    def get_helpful(self) -> int:
        '''
        Returns if was helpful
        0 is no 1 is yes
        '''
        return self._helpful

    def set_helpful(self, helpful: int) -> None:
        '''
        Sets if helpful
        0 is no 1 is yes
        '''
        self._helpful = helpful