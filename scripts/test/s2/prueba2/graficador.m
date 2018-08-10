clear all, close all, clc
A = csvread('cin_directa.txt');
B = csvread('cin_trayectoria.txt');
% erase stable data
A=A(1:250,:);
B=B(1:350,:); 

l1=length(A);l2=length(B);
t1=0.01*[1:l1];t2=0.01*[1:l2];

ws_v=15;
%% Position A
close all;clc
figure;
leg=cell(7,1);

for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Cinematica Directa');grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;

xlabel('tiempo(s)');
ylabel('posición(rad)');

set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig posicion_A_s2_p3_r.png -r250 -painters

%% Position B
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
set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig posicion_B_s2_p3_r.png -r250 -painters

%% Position A-B
% Posicion A
close all;clc
subplot(1,2,1)
leg=cell(7,1);

for n=1:7   
    plot (t1,A(:,n), 'LineWidth',1);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end

title('Posición-Cinematica Directa');grid on

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
set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig posicion_AB_s2_p3_r.png -r250 -painters
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
    p2=plot (t1,Af(:,n), 'LineWidth',1);
    leg{n-7}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end

title('Velocidad-Cinematica Directa')
grid on

l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);
% -------------------------
set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig velocidad_A_s2_p3_r.png -r250 -painters

%% Velocidad B
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
set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig velocidad_B_s2_p3_r.png -r250 -painters

%% Velocidad A-B
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
title('Velocidad-Control de Trayectoria')
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
set(gcf, 'Position', [0 0 1600 900]);
set(gcf, 'Color', 'w');
export_fig velocidad_AB_s2_p3_r.png -r250 -painters