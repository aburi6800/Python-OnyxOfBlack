import pyxel


pyxel.init(128, 128)
pyxel.cls(0)

pyxel.sound(0).set("g 4r  f 4r   e 4r d 4r   b 3a#3d 4d 4", "T", "7", "N", 20)
pyxel.sound(1).set("d 2r  r  r   c#2r r  r   c#2", "S", "7", "F", 20)
pyxel.sound(2).set("a#2r  r  r   g 2r r  r   a#2", "S", "7", "F", 20)
pyxel.sound(3).set("g 2r  r  r   e 2r r  r   e 2", "S", "7", "F", 20)
pyxel.music(0).set([0], [1], [2], [3])

pyxel.playm(0)
pyxel.show()
