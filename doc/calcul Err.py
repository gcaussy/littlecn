#!/usr/bin/python3
# -*- coding:Utf-8 -*
mmpp = 0.003150
for lgd in range (1, 3000):
	lgd = lgd / 10						# lgd = déplacement demandé
	nbpf = lgd / mmpp					# nbr de pulses necéssaires (en float)
	nbpi = int(nbpf)					# nbr de pulses (en int)
	lgr = mmpp * nbpi					# lgr = longueur réelle parcourue
	err = lgd - lgr						# erreur entre la demande et le réel
	errmic = int(err * 1000)			# erreur en micron
	print("{:09.4f} {:0.6f} {:011.5f} {:05d} {:09.4f} {:0.4f} {:03d}".format(lgd, mmpp, nbpf, nbpi, lgr, err, errmic))


