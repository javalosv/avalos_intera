clear all, close all, clc
semana='2';prueba='4';tipo='_r';
dir=strcat('prueba',prueba,tipo)
file='cin_trayectoria'
A = csvread(strcat(dir,'/',file,'.txt'));
% erase stable data
A=A(1:800,:);
%%
l1=length(A);t1=0.01*[1:l1];
ws_v=15;ws_a=25;ws_j=35;
% Position A
close all;clc
figure
leg=cell(7,1);
for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Posici\'on [rad]",'Interpreter','latex','FontSize',12.5);
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 600 300]);
set(gcf, 'PaperPosition', [0 0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');

ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];


saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba',tipo,'_',file,'_env_p','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba',tipo,'_',file,'_env_p','.png'));
%close all

%% Velocidad A
close all;clc;
figure
legend
%Filtro
Af=A;
f= ones(1, ws_v)/ws_v;

for n=8:14
Af(:,n) = filter(f, 1, A(:,n));
end

for n=8:14   
    plot (t1,Af(:,n), 'LineWidth',1);
    leg{n-7}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end

title('Velocidad-Cinemática Directa')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat('velocidad_A_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))


% Velocidad B
close all;clc;
figure
legend
%Filtro
Bf=B;
f= ones(1, ws_v)/ws_v;

for n=8:14
Bf(:,n) = filter(f, 1, B(:,n));
end

for n=8:14   
    plot (t2,Bf(:,n), 'LineWidth',1);
    leg{n}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end

title('Velocidad-Control de Trayectoria')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat('velocidad_B_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))


% Velocidad A-B
close all;clc;
figure
subplot(1,2,1);
%Filtro

for n=8:14   
    plot (t1,Af(:,n), 'LineWidth',1);
    leg{n-7}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end
title('Velocidad-Cinemática Directa')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

subplot(1,2,2);
for n=8:14   
    plot (t2,Bf(:,n), 'LineWidth',1);
    leg{n-7}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end
title('Velocidad-Control de Trayectoria')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

% -------------------------
set(gcf, 'Position', [0 0 1500 600]);
set(gcf, 'Color', 'w');

saveas(gcf,strcat('velocidad_AB_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))

% Aceleración 
close all;clc
A_A = zeros(l1,7);A_J = zeros(l1,7);
B_A = zeros(l2,7);B_J = zeros(l2,7);

for i=1:7
    for j=1:l1-1
        % Af - Valor A con filtro 
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

f= ones(1, ws_a)/ws_a;
for n=1:7
A_Af(:,n) = filter(f, 1, A_A(:,n));
B_Af(:,n) = filter(f, 1, B_A(:,n));
end

% Aceleracion con filtro aplicado para ambos.
figure ;
for n=1:7  
    plot (t1,A_Af(:,n), 'LineWidth',1)
    leg{n}=strcat('$\ddot{q}_',num2str(n-1),'$');
    hold on
end

title('Aceleración-Cinemática Directa')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^2)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('aceleracion_A_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;


figure;
for n=1:7  
    plot (t2,B_Af(:,n), 'LineWidth',1);
    leg{n}=strcat('$\ddot{q}_',num2str(n-1),'$');
    hold on
end
title('Aceleración-Control de Trayectoria')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^2)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('aceleracion_B_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;

% Aceleration A-B
figure ;
subplot(1,2,1);
for n=1:7  
    plot (t1,A_Af(:,n), 'LineWidth',1)
    leg{n}=strcat('$\ddot{q}_',num2str(n-1),'$');
    hold on
end

title('Aceleración-Cinemática Directa')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^2)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');

subplot(1,2,2);
for n=1:7  
    plot (t2,B_Af(:,n), 'LineWidth',1);
    leg{n}=strcat('$\ddot{q}_',num2str(n-1),'$');
    hold on
end
title('Aceleración-Control de Trayectoria')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^2)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('aceleracion_AB_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;

% Jerk

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

f= ones(1, ws_j)/ws_j;
for n=1:7
A_Jf(:,n) = filter(f, 1, A_J(:,n));
B_Jf(:,n) = filter(f, 1, B_J(:,n));
end


figure 

for n=1:7  
    plot (t1,A_Jf(:,n), 'LineWidth',1)
    leg{n}=strcat('$q^{(3)}_',num2str(n-1),'$');
    hold on
end
  
title('Jerk-Cinemática Directa')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^3)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('jerk_A_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;


figure;
for n=1:7  
    plot (t2,B_Jf(:,n), 'LineWidth',1)
    leg{n}=strcat('$q^{(3)}_',num2str(n-1),'$');
    hold on
end

title('Jerk-Control de Trayectoria')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^3)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('jerk_B_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;

% Jerk A-B

figure 
subplot(1,2,1);
for n=1:7  
    plot (t1,A_Jf(:,n), 'LineWidth',1)
    leg{n}=strcat('$q^{(3)}_',num2str(n-1),'$');
    hold on
end
  
title('Jerk-Control de Trayectoria')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^3)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');

subplot(1,2,2);
for n=1:7  
    plot (t2,B_Jf(:,n), 'LineWidth',1)
    leg{n}=strcat('$q^{(3)}_',num2str(n-1),'$');
    hold on
end

title('Jerk-Cinemática Directa')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^3)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1200 600]);
set(gcf, 'Color', 'w');
saveas(gcf,strcat('jerk_AB_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))
close all;
