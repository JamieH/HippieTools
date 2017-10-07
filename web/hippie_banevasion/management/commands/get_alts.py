from django.core.management.base import BaseCommand, CommandError
from hippie_banevasion.models import Client
from tqdm import tqdm
from cProfile import Profile

class Command(BaseCommand):
    help = 'Find all alt accounts'

    def add_arguments(self, parser):
        parser.add_argument('--ckey', dest='ckey')
        parser.add_argument('--profile', action='store_true', default=False, dest='profile')

    def handle(self, *args, **options):
        if options['profile']:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats()
        else:
            self._handle(*args, **options)

    def _handle(self, *args, **options):

        clients = None
        print(options['ckey'])
        if options['ckey'] is not None:
            clients = clients = [Client.objects.get(ckey=options['ckey']),]
        else:
            clients = Client.objects.all()

        #clients = Client.objects.filter(ckey="Bartels")
        #clients = Client.objects.filter(ckey__in=["SuperbDingaling", "Zeopoi", "ItsMeReuben", "ShroudedCorpse", "Aara"])
        evaders = []
        self.stdout.write("Getting clients")

        # Do they have any alts?
        for client in tqdm(clients):
            alts = client.get_alts()
            if len(alts) > 0:
                evaders.append(client)
            else:
                alts = client.get_player().get_alts()
                if len(alts) > 0:
                    evaders.append(client)

        # Nice lists
        none_banned = {}
        all_banned = {}
        some_banned = {}

        # For each evader:
        for evader in evaders:
            ep = evader.get_player()
            banned = ep.is_server_banned()
            alts_none_banned = True
            alts_some_unbanned = False

            def get_player(x):
                return x.get_player()

            # client alts
            client_alts = list(map(get_player, evader.get_alts()))
            # player alts
            player_alts = evader.get_player().get_alts()
            alts = client_alts + list(set(player_alts) - set(client_alts))

            for alt in alts:
                if alt.is_server_banned():
                    alts_none_banned = False
                elif alt.is_banned():
                    alts_none_banned = False
                else:
                    alts_some_unbanned = True

            # if they're not banned and no alts banned
            if not banned and alts_none_banned:
                none_banned[evader] = alts
            # if they're banned but some alts are unbanned
            elif banned and alts_some_unbanned:
                some_banned[evader] = alts
            # if they're not banned but some alts have been banned
            elif not banned and not alts_none_banned:
                some_banned[evader] = alts
            # they're banned and all alts are banned
            else:
                all_banned[evader] = alts

            def print_alt(alt, tab_count=1):
                tabs = "\t" * tab_count
                if alt.is_server_banned():
                    self.stdout.write(self.style.ERROR("{}BANNED: {}".format(tabs, alt.ckey)))
                elif alt.is_banned():
                    self.stdout.write(self.style.WARNING("{}JOBBAN: {}".format(tabs, alt.ckey)))
                else:
                    self.stdout.write(self.style.NOTICE("{}{}".format(tabs, alt.ckey)))

            def print_list(d):
                for evader, alts in d.items():
                    print_alt(evader.get_player(), 1)

                    for alt in alts:
                        print_alt(alt, 2)

                    self.stdout.write("")

        self.stdout.write(self.style.NOTICE("\n\nNO BANS:"))
        print_list(none_banned)

        self.stdout.write(self.style.WARNING("\n\nALL BANS:"))
        print_list(all_banned)

        self.stdout.write(self.style.ERROR("\n\bSOME BANS:"))
        print_list(some_banned)

        self.stdout.write("\n\n{} alts with 0 bans were found.".format(len(none_banned)))
        self.stdout.write("{} alts with all bans were found.".format(len(all_banned)))
        self.stdout.write("{} alts with SOME bans were found.".format(len(some_banned)))
