entity full_adder is
port (A,B,Ci,S,Co);
A,B,Ci : std_logic : in std_logic;
S,Co : std_logic : out std_logic;
w1 <= A ^ B;
S <= w1 ^ Ci;
w2 <= A & B;
w3 <= A & Ci;
w4 <= Ci & B;
Co <= w2  w3  w4;
end entity;