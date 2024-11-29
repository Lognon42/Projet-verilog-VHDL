library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity full_adder is
    port (
    input A,B,Ci;
    output S,Co;
    w1 <= A ^ B;
    S <= w1 ^ Ci;
    w2 <= A & B;
    w3 <= A & Ci;
    w4 <= Ci & B;
    Co <= w2  w3  w4;
    endmodule
