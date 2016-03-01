import urwid

from tripleodash.sections.base import DashboardSection

LOGO = """
                      ==========~
  OOOO           =====================          ZZZO:
   OOOOOZ     ===========================    +OOOOOO
   ZOOOOOOOO$OOOOOOOO=============OOOOOOOZOOOOOOOOO
    ZOOOOOOOOZ,  ,,=OOO7=======ZOOZ:,  ,,OOOOOOOOO
     OOOOO?           $OOOOOOOOO~           $OOOO?
      OOO         OOO, ,OOOOOOO ,+OO7,        ZOO
     $O7       ,OOOOOOO =OOOOO: OOOOOO         ZO=
    IOO         OOOOOOO  OOOOO ?OOOOOOO        ,OO
   =ZO,         OOOOOOO  OOOOO  OOOOOO,         7OZ
   $OO           ~8OZ~   OOOOO  ,OOOO           ,OO$
  $$ZO,                 7OOOOO=                 IOZ$+
  $$$OO                ,OOOOOOO                 OO$$$
 $$$$OO~              ,OOOOOOOOO               $OZ$$$=
 $$$$$OO7,           :OO$$$$$$$OO,            OOO$$$$$
 $$$$$$OOO         ,OOO$$$$$$$$$OOO,       , OOZ$$$$$$
 $$$$$$$$OOOOZ??OOOOOO$$$$$$$$$$$OOOOO$+?ZOOOO$$$$$$$$
 $$$$$$$$$?=7ZOOOI==ZOO$$$$$$$$ZOZ===7OOOOI=$$$$$$$$$$
 $$$$$$$$$?=============$$$$$$I=============$$$$$$$$$$
 $$$$$$$$$?==============$$$$$==============$$$$$$$$$$
 $$$$$$$$$+===============$$Z===============7$$$$$$$$$
 =$$$$$$$$================+Z================?$$$$$$$$
  $$$$$$$$===================================$$$$$$$$
  ,$$$$$$$===================================$$$$$$$
   $$$$$$$===================================$$$$$$?
    $$$$$$===================================$$$$$$
     Z$$$=====================================$$$Z
      Z$$=====================================$$$
       I?=====================================I,
         ====================================:
           ================================~
             ============================,
                ======================,
                     =============
"""


class About(DashboardSection):

    def __init__(self, clients):
        super(About, self).__init__(clients, "About")

    def widgets(self):
        widgets = [urwid.Text(l) for l in LOGO.splitlines()]
        return super(About, self).widgets() + widgets
