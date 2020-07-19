import localization as lx

P=lx.Project(mode='2D',solver='CCA')


P.add_anchor('anchore_A',(0,76))
P.add_anchor('anchore_B',(50,76))
P.add_anchor('anchore_C',(100,76))

t,label=P.add_target()

t.add_measure('anchore_A',83)
t.add_measure('anchore_B',52)
t.add_measure('anchore_C',62)

P.solve()

# Then the target location is:

print(t.loc)