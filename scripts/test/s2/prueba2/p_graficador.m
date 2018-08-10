clc
A = csvread('cin_directa.txt');
B = csvread('cin_trayectoria.txt');
A=A(1:250,:); % erase stable data
B=B(1:350,:); % erase stable data

l1=length(A);
l2=length(B);
t1=0.01*[1:l1];
t2=0.01*[1:l2];

%%
close all
clc
figure
subplot(1,2,1);
legend
for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-1))
    hold on
end
legend('show')
title('Posicion con Cinematica Directa')
xlabel('seg')
ylabel('rad')
subplot(1,2,2);
legend
for n=1:7  
    plot (t2,B(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-1))
    hold on
    legend
end
legend('show')
title('Posicion con Trayectoria')
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
    plot (t1,Af(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Velocidad con Cinematica Directa')
legend('show')
xlabel('seg')
ylabel('rad/s')

subplot(1,2,2);
legend
for n=8:14  
    plot (t2,Bf(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Velocidad con Trayectoria')
legend('show')
xlabel('seg')
ylabel('rad/s')