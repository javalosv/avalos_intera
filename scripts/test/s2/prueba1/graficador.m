clc
A = csvread('cin_directa.txt');
B = csvread('cin_trayectoria.txt');
A=A(1:249,:); % erase stable data
B=B(1:349,:); % erase stable data

l1=length(A);
l2=length(B);
t1=0.01*[1:l1];
t2=0.01*[1:l2];

%%
close all
figure
subplot(1,2,1);
legend
for n=1:7   
    plot (t1,A(:,n))
    hold on
    legend
end
title('Posicion con Cinematica Directa')
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
xlabel('seg')
ylabel('rad')
subplot(1,2,2);
legend
for n=1:7  
    plot (t2,B(:,n))
    hold on
    legend
end
title('Posicion con Trayectoria')
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
xlabel('seg')
ylabel('rad')
%%
close all
figure
subplot(1,2,1);
legend
% 6 1.5
%Filtro
Af=A;
Bf=B;
ws=5; 
f= ones(1, ws)/ws;
for n=8:14
Af(:,n) = filter(f, 1, A(:,n));
Bf(:,n) = filter(f, 1, B(:,n));
end

for n=8:14   
    plot (t1,Af(:,n))
    hold on
    legend
end
title('Velocidad con Cinematica Directa')
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
xlabel('seg')
ylabel('rad/s')

subplot(1,2,2);
legend
for n=8:14  
    plot (t2,Bf(:,n))
    hold on
    legend
end
title('Velocidad con Trayectoria')
legend('\theta 0','\theta 1','\theta 2','\theta 3','\theta 4','\theta 5','\theta 6')
xlabel('seg')
ylabel('rad/s')