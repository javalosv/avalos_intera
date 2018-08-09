clc
A = csvread('cin_directa.txt');
B = csvread('cin_trayectoria.txt');
%A=A(1:250,:); % erase stable data
%B=B(1:350,:); % erase stable data

l1=length(A);
l2=length(B);
t1=0.01*[1:l1];
t2=0.01*[1:l2];

%% Comparación de posición
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
%% Comparación de Velocidad
close all
figure
subplot(1,2,1);
legend
% 6 1.5
%Filtro
Af=A;
Bf=B;
ws=20; 
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

%% Comparación de posición y velocidad. 
close all
clc
figure
subplot(2,2,1);
legend
for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-1))
    hold on
end
legend('show')
title('Posicion con Cinematica Directa')
xlabel('seg')
ylabel('rad')
subplot(2,2,2);
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

subplot(2,2,3);
legend


for n=8:14   
    plot (t1,Af(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Velocidad con Cinematica Directa')
legend('show')
xlabel('seg')
ylabel('rad/s')

subplot(2,2,4);
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
%% Acelracion Jerk
clc
close all
A_A = zeros(l1,7);
A_J = zeros(l1,7);
B_A = zeros(l2,7);
B_J = zeros(l2,7);

for i=1:7
    for j=1:l1-1
        A_A(j,i)=(Af(j+1,i+7)-Af(j,i+7))*100;
    end
    A_A(l1,:)=A_A(l1-1,:);
end


for i=1:7
    for j=1:l2-1
        B_A(j,i)=(Bf(j+1,i+7)-Bf(j,i+7))*100;
    end
    B_A(l2,:)=B_A(l2-1,:);
end

ws=15; 
f= ones(1, ws)/ws;
for n=1:7
A_Af(:,n) = filter(f, 1, A_A(:,n));
B_Af(:,n) = filter(f, 1, B_A(:,n));
end


figure 
subplot(1,2,1);
for n=1:7  
    plot (t1,A_Af(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Aceleración con Cinematica Directa')
legend('show')
xlabel('seg')
ylabel('rad/s²')

subplot(1,2,2);
for n=1:7  
    plot (t2,B_Af(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Aceleración con Control de Trayectoria')
legend('show')
xlabel('seg')
ylabel('rad/s²')



for i=1:7
    for j=1:l1-1
        A_J(j,i)=(A_Af(j+1,i)-A_Af(j,i))*100;
    end
    A_J(l1,:)=A_J(l1-1,:);
end


for i=1:7
    for j=1:l2-1
        B_J(j,i)=(B_Af(j+1,i)-B_Af(j,i))*100;
    end
    B_J(l2,:)=B_J(l2-1,:);
end

ws=15; 
f= ones(1, ws)/ws;
for n=1:7
A_Jf(:,n) = filter(f, 1, A_J(:,n));
B_Jf(:,n) = filter(f, 1, B_J(:,n));
end



figure 
subplot(1,2,1);
for n=1:7  
    plot (t1,A_Jf(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Jerk con Cinematica Directa')
legend('show')
xlabel('seg')
ylabel('rad/s²')

subplot(1,2,2);
for n=1:7  
    plot (t2,B_Jf(:,n), 'LineWidth',1,'DisplayName',"\theta"+num2str(n-8))
    hold on
    legend
end
title('Jerk con Control de Trayectoria')
legend('show')
xlabel('seg')
ylabel('rad/s²')

