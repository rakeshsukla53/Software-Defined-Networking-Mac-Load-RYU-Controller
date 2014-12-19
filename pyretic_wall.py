
from pyretic.lib.corelib import *
from pyretic.lib.std import *

from pyretic.modules.mac_learner import mac_learner as act_like_switch

import csv, os
policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]

def main():
    # start with a policy that doesn't match any packets
    not_allowed = none
    # and add traffic that isn't allowed
    with open(policy_file, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            not_allowed = not_allowed | union([match(srcmac=MAC(row['mac_0']), dstmac=MAC(row['mac_1'])) | match(srcmac=MAC(row['mac_1']), dstmac=MAC(row['mac_0']))])

    # express allowed traffic in terms of not_allowed - hint use '~'
    allowed = ~not_allowed
#    allowed = if_(not_allowed, drop, passthrough)

    # and only send allowed traffic to the mac learning (act_like_switch) logic
    return allowed >> act_like_switch()
