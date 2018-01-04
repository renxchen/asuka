from Pantheon.Venus.db_units.db_units import *
from Pantheon.Venus.db_units.models import CollPolicyCliRule
from django.forms.models import model_to_dict


def get_all_rule():
    rules = CollPolicyCliRule.objects.filter(**{}).values()
    return rules


if __name__ == "__main__":
    rules = get_all_rule()
    print rules
