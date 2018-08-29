clear all, close all, clc
semana='6';prueba='7';tipo='_s';

dir=strcat('prueba',prueba,tipo)
p = csvread(strcat(dir,'/0.5_data_p.txt'));
v = csvread(strcat(dir,'/0.5_data_v.txt'));
a = csvread(strcat(dir,'/0.5_data_a.txt'));
y = csvread(strcat(dir,'/0.5_data_y.txt'));
%
%0.8%knots= round(100*[ 0.01,          0.61560236 , 0.9325425,   1.33975512 , 1.92320375 , 2.69886259  ,3.30919542 , 3.6952288  , 4.15342369  ,4.47495072 , 4.73373555  ,5.31977541]);
knots=round(100*[ 0.01,          0.86399493,  1.29226531  ,1.83870673,  2.64116435 , 3.55737892, ...
  4.16490384  ,4.56355755,  5.10095785 , 5.61306328 , 6.0164334,   6.86985952]);
leg=cell(7,1);
for n=2:8   
    plot (p(:,1),p(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-1}=strcat('$q_',num2str(n-2),'$');
    hold on
end

grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12)
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Posici\'on [rad]",'Interpreter','latex','FontSize',12.5);
set(gca,'GridLineStyle','--');set(gca,'GridColor','k');set(gca,'GridAlpha',0.25);

xlim([0 (10+knots(end))/100])
set(gcf, 'Position', [0 0 590 320]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');

ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - 1.5*ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];



saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_p','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_p','.png'));
close all
%
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

xlim([0 (10+knots(end))/100])
set(gcf, 'Position', [0 0 590 320]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');


ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - 1.5*ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
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

xlim([0 (10+knots(end))/100])
set(gcf, 'Position', [0 0 590 320]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');


ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - 1.5*ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
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

xlim([0 (10+knots(end))/100])
set(gcf, 'Position', [0 0 590 320]);
set(gcf, 'PaperPosition', [0.0 0.0 8.1 4.1]); % For pdf generation
set(gcf, 'PaperSize', [8.1 4.1]); 
set(gcf, 'Color', 'w');


ax = gca;outerpos = ax.OuterPosition;ti = ax.TightInset; 
left = outerpos(1) + ti(1);bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - 1.5*ti(1) - ti(3);ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left bottom ax_width ax_height];


saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba_',prueba,'_env_y','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba_',prueba,'_env_y','.png'));
close all