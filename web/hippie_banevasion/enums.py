from django_enumfield import Enum, Item

SecurityEventEnum = Enum('SecurityEventEnum',
    Item(10, 'possible_replay_attack', "An expired HMAC was used"),
    Item(20, 'useragent', "An incorrect useragent accessed the API"),
    Item(30, 'sentry_ipspoof', "An incorrect IP used the Sentry useragent"),
    Item(40, 'gameip_missmatch', "An incorrect IP accessed the game server API"),
    Item(50, 'no_body', "A request was received with no body"),
    Item(60, 'associated_reverse_engineer', "An account was marked as an RE by association"),
    Item(70, 'alt_detected', "An account was detected as an alternate account"),
    Item(80, 'invalid_data', "Invalid data was sent to the server")
)