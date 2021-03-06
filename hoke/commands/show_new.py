from .. import display
from .. import models
from .. import states


def get_command():
    return Command()


class Command(object):
    name = 'new'
    help = ('List new blueprints')

    def add_arguments(self, parser):
        pass

    def execute(self, hoke_db, args):
        bps = self.get_new_bps(hoke_db)
        bps.sort(key=lambda x: x.date_created)
        self.display(bps)

    def get_new_bps(self, hoke_db):
        bps = []
        for raw_bp in hoke_db.list_blueprints():
            bp = models.blueprint_from_raw(raw_bp)
            new_check = states.get_new_check()
            if new_check.check(bp):
                bps.append(bp)
        return bps

    def display(self, bps):
        print "There are {} new blueprints".format(len(bps))
        print
        first = True
        for bp in bps:
            if first:
                first = False
            else:
                print
            print u"{}:".format(bp.title)
            print u"  Owner: {}".format(bp.owner)
            print u"  Assignee: {}".format(bp.assignee)
            print u"  Date Created: {}".format(
                bp.date_created.date().isoformat())
            print u"  URL: {}".format(bp.url)
            print u"  Summary:"
            display.print_summary(bp.summary, prefix='    ')
        print
        print "Displayed {} new blueprints".format(len(bps))
