from project_module.source.models import Bonus, Episode, Eyecatch

OP5 = Bonus('OP5', title='AIZO')
ED5 = Bonus('ED5', title='Song of Dawn')

ECB1 = Eyecatch('B1', title='Blue v1')
ECB2 = Eyecatch('B2', title='Blue v2')
ECY1 = Eyecatch('Y1', title='Yellow v1')
ECY2 = Eyecatch('Y2', title='Yellow v2')

E48 = Episode('48', OP=OP5, ED=ED5, EC1=ECB1, EC2=None, title='Execution')
E49 = Episode('49', OP=OP5, ED=ED5, EC1=ECY1, EC2=None, title='One More Time')
E50 = Episode('50', OP=OP5, ED=ED5, EC1=None, EC2=None, title='About the Culling Game')
E51 = Episode('51', OP=OP5, ED=ED5, EC1=ECY1, EC2=None, title='Perfect Preparation')
E52 = Episode('52', OP=OP5, ED=ED5, EC1=None, EC2=None, title='Fever')
E53 = Episode('53', OP=OP5, ED=ED5, EC1=ECB1, EC2=ECY1, title='Cog')
E54 = Episode('54', OP=OP5, ED=ED5, EC1=ECY1, EC2=None, title='Tokyo Colony No. 1, Part 1')
E55 = Episode('55', OP=OP5, ED=ED5, EC1=None, EC2=None, title='Tokyo Colony No. 1, Part 2')
E56 = Episode('56', OP=OP5, ED=ED5, EC1=ECY1, EC2=None, title='Tokyo Colony No. 1, Part 3')
E57 = Episode('57', OP=OP5, ED=ED5, EC1=ECB2, EC2=ECY2, title='Tokyo Colony No. 1, Part 4')
E58 = Episode('58', OP=OP5, ED=ED5, EC1=ECB2, EC2=ECY1, title='Tokyo Colony No. 1, Part 5')
E59 = Episode('59', OP=None,ED=ED5, EC1=ECB2, EC2=None, title='Sendai Colony')
