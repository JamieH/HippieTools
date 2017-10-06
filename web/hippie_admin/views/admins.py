from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from hippie_ss13.models import Admin, Player


class AdminListView(LoginRequiredMixin, TemplateView):
    template_name = "hippie_admin/admins/list.html"

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        admin_dict = {}

        admins = Admin.objects.all()

        order = ['Host', 'HeadAdmin', 'GameMaster', 'GameAdmin', 'TrialAdmin', 'Mentor', 'Coder', 'Removed']
        order = {key: i for i, key in enumerate(order)}
        ordered_admins = sorted(admins, key=lambda section: order.get(section.rank, 0))

        lookup = []
        for admin in ordered_admins:
            if admin.rank == "Removed" or admin.rank == "Mentor":
                continue
            lookup.append(admin.ckey)

        players = Player.objects.filter(ckey__in=lookup)
        players_dict = {}
        for player in players:
            players_dict[player.ckey] = player

        last_month = datetime.today() - timedelta(days=30)

        for admin in ordered_admins:
            if admin.rank == "Removed" or admin.rank == "Mentor":
                continue
            if admin.ckey in players_dict:
                admin_dict[admin] = {
                    "player": players_dict[admin.ckey],
                    "total_connections": len(players_dict[admin.ckey].get_connections()),
                    "recent_connections": len(players_dict[admin.ckey].get_connections().filter(datetime__gte=last_month))
                }
            else:
                messages.add_message(self.request, messages.WARNING, "{} should be removed from the admins table".format(admin.ckey))

        context['admins'] = admin_dict

        return context
