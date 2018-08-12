clear all, close all, clc
A = csvread('cin_directa.txt');
B = csvread('cin_trayectoria.txt');
% erase stable data
A=A(1:250,:);
B=B(1:350,:); 

l1=length(A);l2=length(B);
t1=0.01*[1:l1];t2=0.01*[1:l2];
semana=2;
prueba=1;
tipo='s';% simulacion o real
ws_v=15;


% Position A
close all;clc
figure
leg=cell(7,1);

for n=1:7   
    p2=plot (t1,A(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Cinemática Directa')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('posición(rad)');
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

saveas(gcf,strcat('posicion_A_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))

% Position B
close all;clc
figure
leg=cell(7,1);

for n=1:7   
    p2=plot (t2,B(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Control de Trayectoria')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('posición(rad)');
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

saveas(gcf,strcat('posicion_B_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))


%Position A-B
% Posicion A
close all;clc
x=figure
subplot(1,2,1)
leg=cell(7,1);

for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Cinemática Directa');grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;

xlabel('tiempo(s)');
ylabel('posición(rad)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

% Position B
subplot(1,2,2)

for n=1:7   
    p2=plot (t2,B(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Control de Trayectoria')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('posición(rad)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

% -------------------------
set(x, 'Position', [0 0 1500 600]);
set(x, 'Color', 'w');



saveas(gcf,strcat('posicion_AB_s',num2str(semana),'_p',num2str(prueba),'_',tipo,'.svg'))


% Velocidad A
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
    p2=plot (t1,Af(:,n), 'LineWidth',1);
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
    p2=plot (t2,Bf(:,n), 'LineWidth',1);
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
Af=A;
Bf=B;
f= ones(1, ws_v)/ws_v;
for n=8:14
Af(:,n) = filter(f, 1, A(:,n));
Bf(:,n) = filter(f, 1, B(:,n));
end

for n=8:14   
    p2=plot (t1,Af(:,n), 'LineWidth',1);
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
    p2=plot (t2,Bf(:,n), 'LineWidth',1);
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

close all;