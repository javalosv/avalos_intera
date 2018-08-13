clear all, close all, clc
semana='2';prueba='4';tipo='_r';

dir=strcat('prueba',prueba,tipo)
p = csvread(strcat(dir,'/data_p.txt'));
v = csvread(strcat(dir,'/data_v.txt'));
a = csvread(strcat(dir,'/data_a.txt'));
y = csvread(strcat(dir,'/data_y.txt'));

knots= 1:70:701

leg=cell(7,1);
for n=2:8   
    plot (p(:,1),p(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-1}=strcat('$q_',num2str(n-2),'$');
    hold on
end

grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
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


saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_p','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_p','.png'));
close all

figure;
for n=2:8   
    plot (v(:,1),v(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-1}=strcat('$\dot{q}_',num2str(n-2),'$');
    hold on
end

grid on
legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12)
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Velocidad [rad/s]",'FontSize',12.5,'Interpreter','latex')
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 600 300]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');

ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_v','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_v','.png'));
close all
%
figure;
for n=2:8   
    plot (a(:,1),a(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-1}=strcat('$\ddot{q}_',num2str(n-2),'$');
    hold on
end
grid on
legend(leg,'Location','best','interpreter', 'latex','NumColumns',4,'FontSize',12)
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Aceleraci\'on [rad/$s^2$]",'FontSize',12.5,'Interpreter','latex')
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 600 300]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');

ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_a','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_a','.png'));
close all

%
figure;
clc
for n=2:8   
    plot (y(:,1),y(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-1}=strcat('$q^{(3)}_',num2str(n-2),'$');
    hold on
end
grid on
legend(leg,'Location','best','interpreter', 'latex','NumColumns',4,'FontSize',12)
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Jerk [rad/$s^3$]",'FontSize',12.5,'Interpreter','latex')
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

set(gcf, 'Position', [0 0 600 300]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');

ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];

saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_y','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_y','.png'));
close all