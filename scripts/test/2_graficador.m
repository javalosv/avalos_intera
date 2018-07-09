clear all 
close all
clc
P = csvread('save_data_p.txt');
V = csvread('save_data_v.txt');
A = csvread('save_data_a.txt');
JK = csvread('save_data_y.txt');

f1=figure

for n=2:7   
    plot (P(:,1),P(:,n))
    hold on
    legend
end
title('Posicion')


f2=figure
for n=2:7
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
for n=1:6   
    plot (t,D(:,n))
    hold on
    legend
end
title('Posicion')

f4=figure
legend
for n=7:12   
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
for n=2:7   
    plot (P(:,1),P(:,n))
    hold on
    legend
end
title('Posicion')

subplot(1,2,2);
for n=1:6   
    plot (t,D(:,n))
    hold on
    legend
end
title('Posicion')


figure
subplot(1,2,1);
for n=2:7
    plot (V(:,1),V(:,n))
    hold on
    legend
end
title('Velocidad')

subplot(1,2,2);
legend
for n=7:12   
    plot (t,D(:,n))
    hold on
    legend
end
title('Velocidad')


