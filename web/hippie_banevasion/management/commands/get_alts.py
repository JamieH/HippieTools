from django.core.management.base import BaseCommand, CommandError
from hippie_banevasion.models import Client
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Find all alt accounts'

    def handle(self, *args, **options):

        clients = Client.objects.all()
        #clients = Client.objects.filter(ckey="Bartels")
        evaders = []
        self.stdout.write("Getting clients")
        for client in tqdm(clients):
            alts = client.get_alts()
            if len(alts) > 0:
                evaders.append(client)

        for evader in evaders:
            ep = evader.get_player()
            if ep.is_server_banned():
                self.stdout.write(self.style.ERROR("BANNED: {}".format(evader.ckey)))
            else:
                self.stdout.write(self.style.NOTICE(evader.ckey))
            for alt in evader.get_alts():
                p = alt.get_player()
                if p.is_server_banned():
                    self.stdout.write("\a", ending="")
                    self.stdout.write(self.style.ERROR("\t\t BANNED: {}".format(alt)))
                elif p.is_banned():
                    self.stdout.write("\a", ending="")
                    self.stdout.write(self.style.WARNING("\t\t JOBBAN: {}".format(alt)))
                else:
                    self.stdout.write(self.style.NOTICE("\t\t {}".format(alt)))

        self.stdout.write("\n\n{} alts were found.".format(len(evaders)))
