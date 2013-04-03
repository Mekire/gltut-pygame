NUMBER_OF_VERTICES = 8

_Z_OFFSET = 1.5

_COLOR = {"GREEN" : [0.0,1.0,0.0,1.0],
          "BLUE"  : [0.0,0.0,1.0,1.0],
          "RED"   : [1.0,0.0,0.0,1.0]}

_POSITIONS = [#Front face positions
              -400.0, 400.0,0.0,
               400.0, 400.0,0.0,
               400.0,-400.0,0.0,
              -400.0,-400.0,0.0,
              #Rear face positions
              -200.0, 600.0,-_Z_OFFSET,
               600.0, 600.0,-_Z_OFFSET,
               600.0,-200.0,-_Z_OFFSET,
              -200.0,-200.0,-_Z_OFFSET]

_COLORS = (#Object 1 colors
           _COLOR["GREEN"]*4+
           _COLOR["RED"  ]*4)

VERTICES = _POSITIONS+_COLORS

INDICES = [0,1,3,
           1,2,3,

           4,5,7,
           5,6,7,]