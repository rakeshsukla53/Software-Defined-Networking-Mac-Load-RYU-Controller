

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import learn 
	
def firewall(self):
	def AddRule (switch, srcmac, value=True):
		self.firewall[(switch, srcmac)]=value
		print "Adding Firewall rule in %s: %s" % (switch, srcmac)
		self.policy = parallel([ (match(switch=switch) &
				          match(srcmac=srcmac))
				         for (switch, srcmac)
				         in self.firewall.keys()])
	self.AddRule = AddRule
	
	def initialize():
	#Initialize the firewall
		print "initializing firewall"
		self.firewall = {}

		self.AddRule(1, MAC('00:00:00:00:00:01'))
		self.AddRule(1, MAC('00:00:00:00:00:02'))
	
	initialize()


def main():
	return dynamic(firewall)() >> dynamic(learn)()
	
