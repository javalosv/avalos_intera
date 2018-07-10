clear all 
close all
clc
P = csvread('save_data_p.txt');
V = csvread('save_data_v.txt');
A = csvread('save_data_a.txt');
JK = csvread('save_data_y.txt');

figure

for n=2:8   
    plot (P(:,1),P(:,n))
    hold on
    legend
end
title('Posicion')


f2=figure
for n=2:8
    plot (V(:,1),V(:,n))
    hold on
    legend
end
title('Velocidad')

%%

D = csvread('save_real_data.txt');
k=length(D);
f3=figure
legend
t=0.01*[1:k];
for n=1:7   
    plot (t,D(:,n))
    hold on
    legend
end
title('Posicion')

f4=figure
legend
for n=8:14   
    plot (t,D(:,n))
    hold on
    legend
end
title('Velocidad')

%%

clear all 
close all
clc
P = csvread('save_data_p.txt');
V = csvread('save_data_v.txt');
A = csvread('save_data_a.txt');
JK = csvread('save_data_y.txt');
D = csvread('save_real_data.txt');
k=length(D);

legend
t=0.01*[1:k];



subplot(1,2,1);
for n=2:8   
    plot (P(:,1),P(:,n))
    hold on
end
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
title('Posicion')

subplot(1,2,2);
for n=1:7   
    plot (t,D(:,n))
    hold on
end
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
title('Posicion Feedback')


figure
subplot(1,2,1);
for n=2:8
    plot (V(:,1),V(:,n))
    hold on
end
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
title('Velocidad')

subplot(1,2,2);
legend
for n=8:14   
    plot (t,D(:,n))
    hold on
end
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
title('Velocidad Feedback')


