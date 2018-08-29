clear all, close all, clc
semana='6';prueba='8';tipo='_r';
dir=strcat('prueba',prueba,tipo)
file='directa'
A = csvread(strcat(dir,'/',file,'.txt'));
% erase stable data
%A=A(1:350,:);
knots=[1,832] 
%%
l1=length(A);t1=0.01*[1:l1];
ws_v=25;ws_a=30;ws_j=35;
% Position A
close all;clc;figure
leg=cell(7,1);
for n=1:7   
    plot (t1,A(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n}=strcat('$q_',num2str(n-1),'$');
    hold on
end
grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
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

saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba',tipo,'_',file,'_env_p','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba',tipo,'_',file,'_env_p','.png'));
close all
%
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
    plot (t1,Af(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n-7}=strcat('$\dot{q}_',num2str(n-8),'$');
    hold on
end

grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Velocidad [rad/s]",'Interpreter','latex','FontSize',12.5);
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

saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba',tipo,'_',file,'_env_v','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba',tipo,'_',file,'_env_v','.png'));

% Aceleración 
close all; clc
A_A = zeros(l1,7);A_J = zeros(l1,7);

for i=1:7
    for j=1:l1-1
        % Af - Valor A con filtro 
        A_A(j,i)=(Af(j+1,i+7)-Af(j,i+7))*100;
    end
    A_A(l1,:)=A_A(l1-1,:);
end

f= ones(1, ws_a)/ws_a;
for n=1:7
A_Af(:,n) = filter(f, 1, A_A(:,n));
end

% Aceleracion con filtro aplicado para ambos.
figure ;
for n=1:7  
    plot (t1,A_Af(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    leg{n}=strcat('$\ddot{q}_',num2str(n-1),'$');
    hold on
end

grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Aceleraci\'on [rad/$s^2$]",'Interpreter','latex','FontSize',12.5);
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


saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba',tipo,'_',file,'_env_a','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba',tipo,'_',file,'_env_a','.png'));


% Jerk A
close all
%
for i=1:7
    for j=1:l1-1
        A_J(j,i)=(A_Af(j+1,i)-A_Af(j,i))*100;
    end
    A_J(l1,:)=A_J(l1-1,:);
end
f= ones(1, ws_j)/ws_j;
for n=1:7
A_Jf(:,n) = filter(f, 1, A_J(:,n));
end
figure 

jerk_acc=0;
for n=1:7  
    plot (t1,A_Jf(:,n),'-o', 'LineWidth',1,'MarkerSize',5,'MarkerIndices', knots);
    jerk_acc=jerk_acc+trapz(t1,(A_Jf(:,n)).^2);
    leg{n}=strcat('$q^{(3)}_',num2str(n-1),'$');
    hold on
end
jerk_acc=jerk_acc^0.5
time_acc=t1(end)*6
grid on
dummyh = line(nan, nan, 'Linestyle', 'none', 'Marker', 'none', 'Color', 'none');
l=legend(leg,'interpreter', 'latex','NumColumns',4,'Location','best','FontSize',12);
xlabel('Tiempo [s]','FontSize',12.5,'Interpreter','latex');
ylabel("Jerk [rad/$s^3$]",'Interpreter','latex','FontSize',12.5);
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


saveas(gcf,strcat(dir,'/pdf/s',semana,'_prueba',tipo,'_',file,'_env_y','.pdf'));
saveas(gcf,strcat(dir,'/png/s',semana,'_prueba',tipo,'_',file,'_env_y','.png'));
close all