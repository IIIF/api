
manifest : resource
resource : probe
probe : access


one:one | one:one

R1
  P1
    A1
R2
  P2
    A2


one:one | one:many 

R1
  P1
    A1
    A2
R2
  P2
    A1
    A2


one:one | many:one

R1
  P1
    A1
R2
  P2
    A1

one:many | one:many

R1
  P1
    A1
    A2
  P2
    A1
    A2  
R2
  P1
    A1
    A2
  P2
    A1
    A2  


one:many | many:one

R1
  P1
    A1
  P2
    A1
R2
  P1
    A1
  P2
    A1
R3
  P1
    A3
  P2
    A3


many:one | one:one

R1
  P1
    A1 
R2
  P1
    A1


many:one | one:many

R1
  P1
    A1 
    A2
R2
  P1
    A1
    A2


many:one | many:one

R1
  P1
    A1
R2
  P1
    A1
R3
  P2
    A1




