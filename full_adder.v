module full_adder (A,B,Ci,S,Co);
input A,B,Ci;
output S,Co;
wire w1,w2,w3,w4;
assign w1 = A ^ B;
assign S = w1 ^ Ci;
assign w2 = A & B;
assign w3 = A & Ci;
assign w4 = Ci & B;
assign Co = w2  w3  w4;
endmodule