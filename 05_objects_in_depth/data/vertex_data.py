NUMBER_OF_VERTICES = 36

_EXTENT = {"RIGHT" : 0.8,
           "TOP"   : 0.2,
           "MIDDLE": 0.0,
           "FRONT" :-1.25,
           "REAR"  :-1.75}

_EXTENT["LEFT"]   = -_EXTENT["RIGHT"]
_EXTENT["BOTTOM"] = -_EXTENT["TOP"]

#Colors are defined as follows in the original tutorial.
#Don't blame me if BLUE is green and GREEN is blueish-grey.
_COLOR = {"GREEN" : [0.75,0.75,1.0,1.0],
          "BLUE"  : [0.0 ,0.5 ,0.0,1.0],
          "RED"   : [1.0 ,0.0 ,0.0,1.0],
          "GREY"  : [0.8 ,0.8 ,0.8,1.0],
          "BROWN" : [0.5 ,0.5 ,0.0,1.0]}

_POSITIONS = [#Object 1 positions
              _EXTENT["LEFT"], _EXTENT["TOP"],   _EXTENT["REAR"],
              _EXTENT["LEFT"], _EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["RIGHT"],_EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["RIGHT"],_EXTENT["TOP"],   _EXTENT["REAR"],

              _EXTENT["LEFT"], _EXTENT["BOTTOM"],_EXTENT["REAR"],
              _EXTENT["LEFT"], _EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["RIGHT"],_EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["RIGHT"],_EXTENT["BOTTOM"],_EXTENT["REAR"],

              _EXTENT["LEFT"], _EXTENT["TOP"],   _EXTENT["REAR"],
              _EXTENT["LEFT"], _EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["LEFT"], _EXTENT["BOTTOM"],_EXTENT["REAR"],

              _EXTENT["RIGHT"],_EXTENT["TOP"],   _EXTENT["REAR"],
              _EXTENT["RIGHT"],_EXTENT["MIDDLE"],_EXTENT["FRONT"],
              _EXTENT["RIGHT"],_EXTENT["BOTTOM"],_EXTENT["REAR"],

              _EXTENT["LEFT"], _EXTENT["BOTTOM"],_EXTENT["REAR"],
              _EXTENT["LEFT"], _EXTENT["TOP"],   _EXTENT["REAR"],
              _EXTENT["RIGHT"],_EXTENT["TOP"],   _EXTENT["REAR"],
              _EXTENT["RIGHT"],_EXTENT["BOTTOM"],_EXTENT["REAR"],

              #Object 2 positions
              _EXTENT["TOP"],   _EXTENT["RIGHT"],_EXTENT["REAR"],
              _EXTENT["MIDDLE"],_EXTENT["RIGHT"],_EXTENT["FRONT"],
              _EXTENT["MIDDLE"],_EXTENT["LEFT"], _EXTENT["FRONT"],
              _EXTENT["TOP"],   _EXTENT["LEFT"], _EXTENT["REAR"],

              _EXTENT["BOTTOM"],_EXTENT["RIGHT"],_EXTENT["REAR"],
              _EXTENT["MIDDLE"],_EXTENT["RIGHT"],_EXTENT["FRONT"],
              _EXTENT["MIDDLE"],_EXTENT["LEFT"], _EXTENT["FRONT"],
              _EXTENT["BOTTOM"],_EXTENT["LEFT"], _EXTENT["REAR"],

              _EXTENT["TOP"],   _EXTENT["RIGHT"],_EXTENT["REAR"],
              _EXTENT["MIDDLE"],_EXTENT["RIGHT"],_EXTENT["FRONT"],
              _EXTENT["BOTTOM"],_EXTENT["RIGHT"],_EXTENT["REAR"],

              _EXTENT["TOP"],   _EXTENT["LEFT"],_EXTENT["REAR"],
              _EXTENT["MIDDLE"],_EXTENT["LEFT"],_EXTENT["FRONT"],
              _EXTENT["BOTTOM"],_EXTENT["LEFT"],_EXTENT["REAR"],

              _EXTENT["BOTTOM"],_EXTENT["RIGHT"],_EXTENT["REAR"],
              _EXTENT["TOP"],   _EXTENT["RIGHT"],_EXTENT["REAR"],
              _EXTENT["TOP"],   _EXTENT["LEFT"], _EXTENT["REAR"],
              _EXTENT["BOTTOM"],_EXTENT["LEFT"], _EXTENT["REAR"]]

_COLORS = (#Object 1 colors
           _COLOR["GREEN"]*4+
           _COLOR["BLUE" ]*4+
           _COLOR["RED"  ]*3+
           _COLOR["GREY" ]*3+
           _COLOR["BROWN"]*4+

           #Object 2 colors
           _COLOR["RED"  ]*4+
           _COLOR["BROWN"]*4+
           _COLOR["BLUE" ]*3+
           _COLOR["GREEN"]*3+
           _COLOR["GREY" ]*4)

VERTICES = _POSITIONS+_COLORS

INDICES = [ 0, 2, 1,
            3, 2, 0,

            4, 5, 6,
            6, 7, 4,

            8, 9,10,
           11,13,12,

           14,16,15,
           17,16,14]