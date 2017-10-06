from django.core.management.base import BaseCommand, CommandError
from hippie_banevasion.models import Client
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Find all alt accounts'

    def handle(self, *args, **options):

        clients = Client.objects.all()
        #clients = Client.objects.filter(ckey="Bartels")
        #clients = Client.objects.filter(ckey__in=["SuperbDingaling", "Zeopoi", "ItsMeReuben", "ShroudedCorpse", "Aara"])
        evaders = []
        self.stdout.write("Getting clients")
        for client in tqdm(clients):
            alts = client.get_alts()
            if len(alts) > 0:
                evaders.append(client)

        none_banned = {}
        all_banned = {}
        some_banned = {}

        for evader in evaders:
            ep = evader.get_player()
            banned = ep.is_server_banned()
            alts_none_banned = True
            alts_some_unbanned = False

            alts = evader.get_alts()
            for alt in alts:
                p = alt.get_player()
                if p.is_server_banned():
                    alts_none_banned = False
                elif p.is_banned():
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
                ep = alt.get_player()
                if ep.is_server_banned():
                    self.stdout.write(self.style.ERROR("{}BANNED: {}".format(tabs, alt.ckey)))
                elif ep.is_banned():
                    self.stdout.write(self.style.WARNING("{}JOBBAN: {}".format(tabs, alt.ckey)))
                else:
                    self.stdout.write(self.style.NOTICE("{}{}".format(tabs, alt.ckey)))

            def print_list(d):
                for evader, alts in d.items():
                    print_alt(evader, 1)

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
