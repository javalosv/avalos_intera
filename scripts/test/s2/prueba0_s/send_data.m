clear all, close all, clc
p = csvread('data_p.txt');
v = csvread('data_v.txt');
a = csvread('data_a.txt');
y = csvread('data_y.txt');
leg=cell(7,1);

semana=2;
prueba=0;

for n=2:8   
    plot (p(:,1),p(:,n), 'LineWidth',1);
    leg{n-1}=strcat('$q_',num2str(n-2),'$');
    hold on
end
%title('Posición')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('posición(rad)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'PaperPosition', [0 0.1 8 4]); %Position plot at left hand corner with width 5 and height 5.
set(gcf, 'PaperSize', [8.1 4.1]); %Set the paper to have width 5 and height 5.
set(gcf, 'Position', [0 0 600 300]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];


saveas(gcf,strcat('en_posicion_s',num2str(semana),'_p',num2str(prueba),'.pdf'))
%%
figure;
for n=2:8   
    plot (v(:,1),v(:,n), 'LineWidth',1);
    leg{n-1}=strcat('$\dot{q}_',num2str(n-2),'$');
    hold on
end
title('Velocidad')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('velocidad(rad/s)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 800 400]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat('en_velocidad_s',num2str(semana),'_p',num2str(prueba),'.svg'))

%
figure;
for n=2:8   
    plot (a(:,1),a(:,n), 'LineWidth',1);
    leg{n-1}=strcat('$\ddot{q}_',num2str(n-2),'$');
    hold on
end
title('Aceleración')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('aceleración(rad/s^2)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 800 400]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat('en_aceleración_s',num2str(semana),'_p',num2str(prueba),'.svg'))

%
figure;
for n=2:8   
    plot (y(:,1),y(:,n), 'LineWidth',1);
    leg{n-1}=strcat('$q^{(3)}_',num2str(n-2),'$');
    hold on
end
title('Jerk')
grid on
l=legend(leg,'interpreter', 'latex');
legend('Location','best');
l.FontSize = 12;
xlabel('tiempo(s)');
ylabel('jerk(rad/s^3)');
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 800 400]);
set(gcf, 'Color', 'w');

ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat('en_jerk_s',num2str(semana),'_p',num2str(prueba),'.svg'))