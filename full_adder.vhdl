library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity full_adder is
port (
    A : in std_logic;
    B : in std_logic;
    Ci : in std_logic;
    S : out std_logic;
    Co : out std_logic);
end full_adder;

architecture full_adder_struct of full_adder is
    signal w1,w2,w3,w4 : std_logic;
begin
    w1 <= A xor B;
    S <= w1 xor Ci;
    w2 <= A and B;
    w3 <= A and Ci;
    w4 <= Ci and B;
    Co <= w2 or w3 or w4;
end full_adder_struct;