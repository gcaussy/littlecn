; Coordonnées polaires absolues
G90 X0 Y0		; Point P0
G01 R100 Q0		; Point P1, en ligne droite (G01)
G03 Q30			; Point P2, en arc (G03)
G01 R50 Q30		; Point P3, en ligne droite (G01)
G03 Q60			; Point P4, en arc (G03)
G01 R100 Q60	; Point P5, en ligne droite (G01)
G03 Q90			; Point P6, en arc (G03)
G01 R0 Q90		; Point P0, en ligne droite (G01)
;
; Coordonnées polaires incrémentales
G90 X0 Y0		; Point P0
G91 G01 R100 Q0	; Point P1, en ligne droite (G01)
G03 Q30			; Point P2, en arc (G03)
G01 R-50Q0		; Point P3, en ligne droite (G01)
G03 Q30			; Point P4, en arc (G03)
G01 R50 Q0		; Point P5, en ligne droite (G01)
G03 Q30			; Point P6, en arc (G03)
G01 R-100 Q0	; Point P0, en ligne droite (G01)
;
; Coordonnées cylindriques
R30 Q10 Z100 R20 Q45 Z10 V30 A20
;
; Angle et coordonnées cartésiennes
X10 Y20			; Point P0, point de départ
Q45 X30			; Point P1
Q90 Y60			; Point P2
Q-45 X50		; Point P3
Q-135 Y20		; Point P4
Q180 X10		; Point P0
;
; Définition des zones de travail
G20 K1 X20 Y20
 G21 K1 X100 Y50
;
; Zone de travail personnalisée
G22 K S0		; Invalidation
G22 K S1		; Validation comme zone interdite à l’entrée
G22 K S2		; Validation comme zone interdite à la sortie
;
; Fonction G159
G159 N1		; On applique le premier décalage d’origine. Équivaut à programmer G54
G159 N6		; On applique le sixième décalage d’origine. Équivaut à programmer G59, mais s'applique de façon absolue
G159 N20		; On applique le vingtième décalage d’origine
;
; Présélection de l'origine polaire (G93)
G93 I35 J30	; Présélectionner P3 comme origine polaire.
G90 G01 R25 Q0	; Point P1, en ligne droite (G01).
G03 Q90		; Point P2, en arc (G03).
G01 X0 Y0		; Point P0, en ligne droite (G01)
;
;
