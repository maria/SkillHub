import inspect


class Constants(object):
    """A base class which inherited returns the class attributes as dictionary
    items, keys or values. How to define the class:

        class Time(Constants):
            SECOND = 1
            MINUTE = 60 & SECOND
            HOUR = 60 * MINUTE
            DAY = 24 * HOUR

    the attribute name has to have upper case letters and underscores, but
    it shouldn't start with an underscore.
    """

    @classmethod
    def items(cls):
        """Return a list of tuples representing the attributes:
            [(SECOND, 1), (MINUTE, 60 * SECOND), ...]
        """
        return cls._get_class_attributes_from_members().items()

    @classmethod
    def keys(cls):
        """Return a list of the attribute names:
            [SECOND, MINUTE, HOUR, DAY]
        """
        return cls._get_class_attributes_from_members().keys()

    @classmethod
    def values(cls):
        """Return a list of the attribute values:
            [1, 60 * SECOND, 60 * MINUTE, 24 * HOUR]
        """
        return cls._get_class_attributes_from_members().values()

    @classmethod
    def _get_class_attributes_from_members(cls):
        attributes = {}
        members = inspect.getmembers(
            cls, lambda member: not(inspect.isroutine(member)))

        for member in members:
            if not member[0].startswith('_') and member[0].isupper():
                attributes[member[0]] = member[1]

        return attributes


class ProjectTypes(Constants):
    PRACTICE = 'Practice'
    LEARN = 'Learn'


class BadgeTypes(Constants):
    FIRST_CONTRIBUTION = 'first_contrib'
    TEN_CONTRIBUTIONS = 'ten_contrib'
    FIVE_SKILLS = 'five_skills'


# GitHub search query limits
MAX_PROJECTS = 10
MAX_SKILLS = 3
MAX_STARS = 100
MIN_STARS = 10
MIN_FORKS = 10
MAX_FORKS = 50
