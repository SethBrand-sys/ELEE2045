v1 = 20;
r1 = 10;
r2 = 25;
r3 = 7.5;
r4 = 2.5;


serr2r4 = r2 + r4; 
res234 = ((r3*(serr2r4))/(r3+(serr2r4)));
req = res234 + r1;
totalcurrent = v1 / req;
disp("Total Current: " + totalcurrent);

v2 = totalcurrent * r1;


voltdrop = v1 - v2;
disp("Total Voltage Drop: " + voltdrop);

i3 = voltdrop / r3; 

r24 = r2 + r4; 
i24 = voltdrop / r24;

if (i3 + i24) == totalcurrent
    disp("The current in R1 is about " + totalcurrent + " Amps");
    disp("The current in R2 and in R4 is about " + i24 + " Amps");
    disp("The current in R3is about " + i3 + " Amps");
end


P1 = r1 * (totalcurrent^2);
P2 = r2 * (i24^2);
P3 = r3 * (i3^2);
P4 = r4 * (i24^2);

disp("The power dissipated from R1 is " + P1 + " Watts");
disp("The power dissipated from R2 is " + P2 + " Watts");
disp("The power dissipated from R3 is " + P3 + " Watts");
disp("The power dissipated from R4 is " + P4 + " Watts");

x = ["R1", "R2", "R3", "R4"];
y = [P1, P2, P3, P4];
b = bar(y);